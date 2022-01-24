import random
import discord
from discord.ext import commands, tasks
import asyncio


def setup(bot):
    bot.add_cog(smithingCog(bot))
    print('Smithing Cog Loaded')


class smithingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.levelTable = {
            "bronze": {
                26: 1,
                141: 1,
                35: 1,
                38: 3,
                84: 5,
                39: 3,
                36: 6,
                37: 8,
                40: 9,
                41: 10
            },
            "iron": {
                27: 10,
                142: 10,
                42: 15,
                85: 15,
                43: 20,
                44: 24,
                45: 13,
                46: 10,
                47: 26,
                48: 28
            },
            "silver": {
                29:20
            },
            "steel": {
                28: 25,  # Bar
                143: 25,  # Arrowtips
                49: 30,  # Scimitar
                86: 30,  # Shield
                50: 35,  # Battleaxe
                51: 39,  # 2H Sword
                52: 28,  # Helmet
                53: 25,  # Boots
                54: 41,  # Legs
                55: 43  # Body
            },
            "gold": {
                30: 35
            },
            "mithril": {
                31: 45,
                144: 45,
                56: 50,
                87: 50,
                57: 55,
                58: 59,
                59: 48,
                60: 45,
                61: 61,
                62: 63
            },
            "adamant": {
                32: 55,
                145: 55,
                88: 60,
                63: 60,
                64: 65,
                65: 69,
                66: 58,
                67: 55,
                68: 71,
                69: 73
            },
            "rune": {
                33: 65,
                146: 65,
                89: 70,
                70: 70,
                71: 75,
                72: 79,
                73: 68,
                74: 65,
                75: 81,
                76: 83
            },
            "dragon": {
                34: 80,
                147: 80,
                90: 82,
                77: 82,
                78: 85,
                79: 88,
                80: 80,
                81: 80,
                82: 88,
                83: 90
            }
        }

    @commands.command(aliases=['Smithing', 'simthing', 'Simthing', 'smihting', 'Smihting', 'smithnig', 'Smithnig'])
    async def smithing(self, ctx, *args):
        player = self.bot.gameManager.getPlayer(ctx.message.author.id)
        smithingLv = player.playerCurrentSmithing
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
                    if smithingLv >= levelReq:
                        # Item ID is in the level table, its a smithable.
                        item = self.bot.gameManager.itemIDToItem(itemID)
                        if len(player.playerInventory) >= player.playerMaxInventory:
                            r = await ctx.send(f'Your inventory is full!')
                            await asyncio.sleep(20)
                            await r.delete()
                            await ctx.message.delete()
                            return
                        await self.smithingLoop(player, item, count, ctx)

                    else:
                        r = await ctx.send(
                            f'You do not meet the smithing level requirement of {levelReq} to make this item!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                else:
                    r = await ctx.send(f'Item is not in the smithing leveling table.')
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
                    if smithingLv >= levelReq:
                        # Item ID is in the level table, its a smithable.
                        item = self.bot.gameManager.itemIDToItem(itemID)
                        if len(player.playerInventory) >= player.playerMaxInventory:
                            r = await ctx.send(f'Your inventory is full!')
                            await asyncio.sleep(10)
                            await r.delete()
                            await ctx.message.delete()
                            return
                        await self.smithingLoop(player, item, count, ctx)
                    else:
                        r = await ctx.send(f'You do not meet the smithing level requirement to make this item!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                        return
                else:
                    r = await ctx.send(f'Item is not in the smithing leveling table.')
                    await asyncio.sleep(10)
                    await r.delete()
                    await ctx.message.delete()
                    return
        else:
            embed = discord.Embed(title=f"{ctx.message.author.display_name.capitalize()} Smithing", description="",
                                  color=0xd25151)
            embed.add_field(name=f'Tier', value=f'!show [itemname] to see components.', inline=False)
            embed.set_thumbnail(url='https://oldschool.runescape.wiki/images/Smithing.png?46893')
            for tier in self.levelTable:
                maxForTier = max(self.levelTable[tier].values())
                minForTier = min(self.levelTable[tier].values())
                if smithingLv >= maxForTier:
                    embed.add_field(name=f'{tier.capitalize()}', value=f'All {tier} items smithable!', inline=False)
                elif smithingLv < minForTier:
                    pass
                else:
                    m = ''
                    for item in self.levelTable[tier]:
                        ex = self.bot.gameManager.itemIDToItem(item)
                        if smithingLv >= self.levelTable[tier][item]:
                            m += f'{ex.itemName}: Lv. {self.levelTable[tier][item]} Smithing\n'
                        elif smithingLv+10>=self.levelTable[tier][item]:
                            m += f'~~{ex.itemName}: Lv. {self.levelTable[tier][item]} Smithing~~\n'

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

    async def smithingLoop(self, player, item, count, ctx):
        output15 = [141, 142, 143, 144, 145, 146, 147]
        produced = 0
        player.isBusy = True
        totalAmt = count
        embed = discord.Embed(title=f"Smithing {item.itemName}", description=f"<@!{player.DiscordID}>",
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
                        embed = discord.Embed(title=f"Smithing {item.itemName}", description=f"<@!{player.DiscordID}>",
                                              color=0xd25151)
                        embed.add_field(name=f'Results', value=f'Crafted {produced} {item.itemName}',
                                        inline=True)
                        embed.add_field(name=f'**Stopped**', value=f'Ran out of a resource.',
                                        inline=False)
                        await e.edit(embed=embed)
                        player.isBusy = False
                        return f'Player does not have enough {id} for crafting {item.itemName}'

                else:
                    embed = discord.Embed(title=f"Smithing {item.itemName}", description=f"<@!{player.DiscordID}>",
                                          color=0xd25151)
                    embed.add_field(name=f'Results', value=f'Crafted {produced} {item.itemName}', inline=True)
                    embed.add_field(name=f'**Stopped**', value=f'Ran out of a resource.',
                                    inline=False)
                    await e.edit(embed=embed)
                    player.isBusy = False
                    return f'Player does not have {id} needed to craft {item.itemName}'

            # Give the player a crafted item
            if item.ID in output15:
                player.addToInventory(item.ID, 15)
                produced += 15
            else:
                player.addToInventory(item.ID, 1)
                produced += 1
            count -= 1
            baseExp = item.xpForCrafting
            xpGained, leveledUp = player.givePlayerExperience("smithing", baseExp)
            if leveledUp:
                await ctx.send(embed=leveledUp, delete_after=300)
            else:
                embed = discord.Embed(title=f"Smithing {item.itemName}", description=f"<@!{player.DiscordID}>",
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
        embed = discord.Embed(title=f"Smithing {item.itemName}", description=f"<@!{player.DiscordID}>",
                              color=0xd25151)
        embed.add_field(name=f'Results', value=f'Crafted {produced} {item.itemName}', inline=True)
        try:
            await e.edit(embed=embed)
        except discord.ClientException:
            print(f'Caught some kind of error, attempting to pass.')
            pass
        await ctx.message.delete()
        player.cancelBool = False
        player.isBusy = False
