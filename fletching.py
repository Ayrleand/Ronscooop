import random
import discord
from discord.ext import commands, tasks
import asyncio


def setup(bot):
    bot.add_cog(fletching(bot))
    print('Fletching Cog Loaded')


class fletching(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.levelTable = {
            # Arrow shafts, headless arrows, bronze arrows
            148:1,
            149:1,
            134:1,
            # Arrows
            135:15,
            136:30,
            137:45,
            138:60,
            139:70,
            140:80,
            # Bows
            127:5,
            128:20,
            129:35,
            130:50,
            131:60,
            132:70,
            133:85
        }

    @commands.command(aliases=['Fletcing', 'Fletching', 'feltching', 'fletch', 'Fletch', 'flethcing', 'fletvhing', 'Fletvhing'])
    async def fletching(self, ctx, *args):
        player = self.bot.gameManager.getPlayer(ctx.message.author.id)
        fletchingLv = player.playerCurrentFletching
        if player.inCombat:
            await ctx.send(f'You are currently in combat! Now is not the time!', delete_after=10)
            await ctx.message.delete()
            return
        if player.isBusy:
            await ctx.send(f'You are busy doing something else at the moment! !cancel if you do not know what.', delete_after=10)
            await ctx.message.delete()
            return
        if not args:
            embed = discord.Embed(title=f"{ctx.message.author.display_name.capitalize()} Fletching", description="", color=0xd25151)
            embed.set_thumbnail(url='https://oldschool.runescape.wiki/images/Fletching.png?ef869')
            m = ""
            for recipe in self.levelTable:
                if fletchingLv >= self.levelTable[recipe]:
                    ex = self.bot.gameManager.itemIDToItem(int(recipe))
                    m += f'{ex.itemName}, requires level {self.levelTable[recipe]}\n'
                elif (fletchingLv+10)>=self.levelTable[recipe]:
                    ex = self.bot.gameManager.itemIDToItem(int(recipe))
                    m += f'~~{ex.itemName}, requires level {self.levelTable[recipe]}~~\n'
            embed.add_field(name=f'Available', value=f'{m}', inline=False)
            await ctx.send(embed=embed, delete_after=30)
            await ctx.message.delete()
        else:
            item = self.bot.gameManager.inputToItem(args[0])
            if item:
                try:
                    count = abs(int(args[1]))
                except IndexError:
                    count = 1
                levelReq = self.levelTable[item.ID]
                if fletchingLv >= levelReq:
                    if len(player.playerInventory) >= player.playerMaxInventory:
                        await ctx.send(f'Your inventory is full!', delete_after=10)
                        await ctx.message.delete()
                        return
                    await self.fletchingLoop(player, item, count, ctx)
                else:
                    await ctx.send(f'You do not have the {levelReq} Fletching required for this!')
                    await ctx.message.delete()
            else:
                await ctx.send(f'Could not find that item!', delete_after=10)
                await ctx.message.delete()

    async def fletchingLoop(self, player, item, count, ctx):
        output15 = [134, 135, 136, 137, 138, 139, 140, 148, 149]
        player.isBusy = True
        totalAmt = count
        produced = 0
        embed = discord.Embed(title=f"Fletching {item.itemName}", description=f"<@!{player.DiscordID}>",
                              color=0xd25151)
        embed.set_thumbnail(url=item.itemEmoj)
        embed.add_field(name=f'Total', value=f'{totalAmt}', inline=True)
        embed.add_field(name=f'Remaining', value=f'{count}', inline=True)
        embed.add_field(name=f'Completed', value=f'0', inline=True)

        pBar = int((totalAmt - count) / (totalAmt) * 10)
        embed.add_field(name=f'Progress', value=f'{"🟪" * pBar}{"⬜" * (10 - pBar)}', inline=False)
        e = await ctx.send(embed=embed)
        while count > 0 and not player.cancelBool:
            for ID in item.craftingComponents:
                compItem = self.bot.gameManager.itemIDToItem(int(ID))
                if player.checkInventory(compItem):
                    needed = item.craftingComponents[f'{ID}']
                    if player.playerInventory[f'{ID}'] >= needed:
                        player.addToInventory(int(ID), -needed)
                    else:
                        embed = discord.Embed(title=f"Fletching {item.itemName}", description=f"<@!{player.DiscordID}>",
                                              color=0xd25151)
                        embed.add_field(name=f'Results', value=f'Fletched {produced} {item.itemName}',
                                        inline=True)
                        embed.add_field(name=f'**Stopped**', value=f'Ran out of a resource.',
                                        inline=False)
                        await e.edit(embed=embed)
                        player.isBusy = False
                        return f'Player does not have enough {compItem.itemName} for crafting {item.itemName}'
                else:
                    embed = discord.Embed(title=f"Fletching {item.itemName}", description=f"<@!{player.DiscordID}>",
                                          color=0xd25151)
                    embed.add_field(name=f'Results', value=f'Fletched {produced} {item.itemName}',
                                    inline=True)
                    embed.add_field(name=f'**Stopped**', value=f'Ran out of an ingredient.',
                                    inline=False)
                    await e.edit(embed=embed)
                    player.isBusy = False
                    return f'Player does not have {compItem.itemName} for crafting {item.itemName}'
            # At this point, we have removed all of the ingredients from the player
            # So lets give them what they are here for.
            if item.ID in output15:
                player.addToInventory(item.ID, 15)
                produced += 15
            else:
                player.addToInventory(item.ID, 1)
                produced += 1
            count -= 1
            baseExp = item.xpForCrafting
            xpGained, leveledUp = player.givePlayerExperience("fletching", baseExp)
            if leveledUp:
                await ctx.send(embed=leveledUp, delete_after=300)
            else:
                embed = discord.Embed(title=f"Fletching {item.itemName}", description=f"<@!{player.DiscordID}>",
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
        embed = discord.Embed(title=f"Fletching {item.itemName}", description=f"<@!{player.DiscordID}>",
                              color=0xd25151)
        embed.add_field(name=f'Results', value=f'Fletched {produced} {item.itemName}', inline=True)
        try:
            await e.edit(embed=embed)
        except discord.ClientException:
            print(f'Caught some kind of error, attempting to pass.')
            pass
        player.cancelBool = False
        player.isBusy = False





