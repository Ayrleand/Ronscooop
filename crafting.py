import random
import discord
from discord.ext import commands, tasks
import asyncio


def setup(bot):
    bot.add_cog(crafting(bot))
    print('Crafting Cog Loaded')


class crafting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.levelTable = {
            "Jewelry": {
                178: 10,
                179: 5,
                180: 20,
                181: 30,
                182: 40,
                183: 30,
                184: 35,
                185: 40,
                186: 50,
                187: 60,
                188: 50,
                189: 55,
                190: 60,
                191: 65,
                192: 70},
            "Leather": {
                155: 1,
                162: 1,
                161: 7,
                160: 9,
                163: 11,
                164: 14,
                165: 18},
            "Green DHide": {
                156: 40,
                166: 42,
                167: 44,
                168: 47},
            "Blue DHide": {
                157: 50,
                169: 52,
                170: 54,
                171: 57},
            "Red DHide": {
                158: 60,
                172: 62,
                173: 64,
                174: 67},
            "Black DHide": {
                159: 70,
                175: 72,
                176: 74,
                177: 77},
            "Other": {
                268: 80}
        }

    @commands.command(aliases=['Crafting', 'carfting', 'Carfting', 'vrafting', 'Vrafting'])
    async def crafting(self, ctx, *args):
        player = self.bot.gameManager.getPlayer(ctx.message.author.id)
        craftingLv = player.playerCurrentCrafting
        if player.inCombat:
            r = await ctx.send(f'You\'re in the middle of fighting something, is now really the time?')
            await asyncio.sleep(15)
            await r.delete()
            await ctx.message.delete()
            return
        if player.isBusy:
            r = await ctx.send(f'You\'re busy doing something else! If you do not know what, use !cancel to reset')
            await asyncio.sleep(10)
            await r.delete()
            await ctx.message.delete()
            return
        if args:
            if args[0].isdigit():
                count = 1
                itemID = int(args[0])
                try:
                    if args[1].isdigit():
                        count = abs(int(args[1]))
                except IndexError:
                    pass
                levelReq = self.recursive_lookup(itemID, self.levelTable)
                if levelReq:
                    # matItem = levelReq
                    if craftingLv >= levelReq:
                        # Item ID is in the level table, its a craftable.
                        item = self.bot.gameManager.itemIDToItem(itemID)
                        if len(player.playerInventory) >= player.playerMaxInventory:
                            r = await ctx.send(f'Your inventory is full!')
                            await asyncio.sleep(20)
                            await r.delete()
                            await ctx.message.delete()
                            return
                        await self.craftingLoop(player, item, count, ctx)

                    else:
                        r = await ctx.send(
                            f'You do not meet the crafting level requirement of {levelReq} to make this item!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                else:
                    r = await ctx.send(f'Item is not in the crafting leveling table.')
                    await asyncio.sleep(10)
                    await r.delete()
                    await ctx.message.delete()
                    return
            else:
                count = 1
                try:
                    if args[1].isdigit():
                        count = int(args[1])
                except IndexError:
                    pass
                itemID = self.bot.gameManager.itemNameToID(args[0])
                levelReq = self.recursive_lookup(itemID, self.levelTable)
                if levelReq:
                    if craftingLv >= levelReq:
                        # Item ID is in the level table, its a craftable.
                        item = self.bot.gameManager.itemIDToItem(itemID)
                        if len(player.playerInventory) >= player.playerMaxInventory:
                            r = await ctx.send(f'Your inventory is full!')
                            await asyncio.sleep(10)
                            await r.delete()
                            await ctx.message.delete()
                            return
                        await self.craftingLoop(player, item, count, ctx)
                        await ctx.message.delete()
                    else:
                        r = await ctx.send(f'You do not meet the crafting level requirement to make this item!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                        return
                else:
                    r = await ctx.send(f'Item is not in the crafting leveling table.')
                    await asyncio.sleep(10)
                    await r.delete()
                    await ctx.message.delete()
                    return
        else:
            embed = discord.Embed(title=f"{ctx.message.author.display_name.capitalize()} Crafting", description="", color=0xd25151)
            embed.add_field(name=f'Tier', value=f'!show [itemname] to see crafting components.', inline=False)
            embed.set_thumbnail(url='https://oldschool.runescape.wiki/images/Crafting.png?46893')
            for tier in self.levelTable:
                maxForTier = max(self.levelTable[tier].values())
                minForTier = min(self.levelTable[tier].values())
                if craftingLv >= maxForTier:
                    embed.add_field(name=f'{tier.capitalize()}', value=f'All {tier} items craftable!', inline=False)
                elif craftingLv < minForTier:
                    pass
                else:
                    m = ''
                    for item in self.levelTable[tier]:
                        if craftingLv >= self.levelTable[tier][item]:
                            ex = self.bot.gameManager.itemIDToItem(item)
                            m += f'{ex.itemName}: Lv. {self.levelTable[tier][item]} Crafting\n'

                    embed.add_field(name=f'{tier.capitalize()}', value=f'{m}', inline=True)
            r = await ctx.send(embed=embed)
            await asyncio.sleep(60)
            await r.delete()
            await ctx.message.delete()

    def recursive_lookup(self, k, d):
        if k in d:
            return d[k]
        for v in d.values():
            if isinstance(v, dict):
                if self.recursive_lookup(k, v):
                    return self.recursive_lookup(k, v)
        return None

    async def craftingLoop(self, player, item, count, ctx):
        player.isBusy = True
        totalAmt = count
        embed = discord.Embed(title=f"Crafting {item.itemName}", description=f"<@!{player.DiscordID}>",
                              color=0xd25151)
        embed.set_thumbnail(url=item.itemEmoj)
        embed.add_field(name=f'Total', value=f'{totalAmt}', inline=True)
        embed.add_field(name=f'Remaining', value=f'{count}', inline=True)
        embed.add_field(name=f'Completed', value=f'0', inline=True)
        pBar = int((totalAmt - count) / (totalAmt) * 10)
        embed.add_field(name=f'Progress', value=f'{"🟪" * pBar}{"⬜" * (10 - pBar)}', inline=False)
        e = await ctx.send(embed=embed)
        while count > 0 and not player.cancelBool:
            # Check item crafting components
            for id in item.craftingComponents:
                # Check player inventory for enough of those components
                exItem = self.bot.gameManager.itemIDToItem(int(id))
                if player.checkInventory(exItem):
                    needed = item.craftingComponents[f'{id}']
                    if player.playerInventory[f'{id}'] >= needed:
                        # Remove them from the player's inventory
                        player.addToInventory(int(id), -needed)

                    else:
                        embed = discord.Embed(title=f"Crafting {item.itemName}", description=f"<@!{player.DiscordID}>",
                                              color=0xd25151)
                        embed.add_field(name=f'Results', value=f'Crafted {totalAmt - count} {item.itemName}',
                                        inline=True)
                        embed.add_field(name=f'**Stopped**', value=f'Ran out of a resource.',
                                        inline=False)
                        await e.edit(embed=embed)
                        player.isBusy = False
                        return f'Player does not have enough {id} for crafting {item.itemName}'

                else:
                    embed = discord.Embed(title=f"Crafting {item.itemName}", description=f"<@!{player.DiscordID}>",
                                          color=0xd25151)
                    embed.add_field(name=f'Results', value=f'Crafted {totalAmt - count} {item.itemName}', inline=True)
                    embed.add_field(name=f'**Stopped**', value=f'Ran out of a resource.',
                                    inline=False)
                    await e.edit(embed=embed)
                    player.isBusy = False
                    return f'Player does not have {id} needed to craft {item.itemName}'

            # Give the player a crafted item
            player.addToInventory(item.ID, 1)
            count -= 1
            baseExp = item.xpForCrafting
            xpGained, leveledUp = player.givePlayerExperience("crafting", baseExp)
            if leveledUp:
                await ctx.send(embed=leveledUp, delete_after=300)
            else:
                embed = discord.Embed(title=f"Crafting {item.itemName}", description=f"<@!{player.DiscordID}>",
                                      color=0xd25151)
                embed.set_thumbnail(url=item.itemEmoj)
                embed.add_field(name=f'Total', value=f'{totalAmt}', inline=True)
                embed.add_field(name=f'Remaining', value=f'{count}', inline=True)
                embed.add_field(name=f'Completed', value=f'{totalAmt - count}', inline=True)
                pBar = int((totalAmt - count) / (totalAmt) * 10)
                embed.add_field(name=f'Progress', value=f'{"🟪" * pBar}{"⬜" * (10 - pBar)}', inline=False)
                embed.add_field(name=f'Exp Gained', value=f'{(totalAmt - count) * xpGained}', inline=True)
                await e.edit(embed=embed)
                await asyncio.sleep(3)
        embed = discord.Embed(title=f"Crafting {item.itemName}", description=f"<@!{player.DiscordID}>",
                              color=0xd25151)
        embed.add_field(name=f'Results', value=f'Crafted {totalAmt - count} {item.itemName}', inline=True)
        try:
            await e.edit(embed=embed)
        except discord.ClientException:
            print(f'Caught some kind of error, attempting to pass.')
            pass
        player.cancelBool = False
        player.isBusy = False
