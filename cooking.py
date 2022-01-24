import random
import discord
from discord.ext import commands, tasks
import asyncio


def setup(bot):
    bot.add_cog(cooking(bot))
    print('Cooking Cog Loaded')


class cooking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.levelTable = {
            # Fish
            256: 1,
            249: 1,
            257: 5,
            270: 5,
            258: 15,
            271: 20,
            259: 25,
            260: 30,
            272: 30,
            261: 40,
            262: 45,
            263: 50,
            273: 50,
            264: 60,
            274: 70,
            265: 75,
            266: 85,
            275: 90
            # Combines
        }

    @commands.command(aliases=['Cooking', 'vooking', 'Vooking', 'coking', 'voking'])
    async def cooking(self, ctx, *args):
        player = self.bot.gameManager.getPlayer(ctx.message.author.id)
        cookingLv = player.playerCurrentCooking
        if player.inCombat:
            await ctx.send(f'You are currently in combat! Now is not the time!', delete_after=10)
            await ctx.message.delete()
            return
        if player.isBusy:
            await ctx.send(f'You are busy doing something else at the moment! !cancel if you do not know what.', delete_after=10)
            await ctx.message.delete()
            return
        if not args:
            embed = discord.Embed(title=f"{ctx.message.author.display_name.capitalize()} Cooking", description="", color=0xd25151)
            embed.set_thumbnail(url='https://oldschool.runescape.wiki/images/Cooking.png?093de')
            m = ""
            for recipe in self.levelTable:
                if cookingLv >= self.levelTable[recipe]:
                    ex = self.bot.gameManager.itemIDToItem(int(recipe))
                    m += f'{ex.itemName}, requires level {self.levelTable[recipe]}\n'
                elif (cookingLv+10)>=self.levelTable[recipe]:
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
                try:
                    levelReq = self.levelTable[item.ID]
                except KeyError:
                    await ctx.send(f'That item is not in the cooking level up table!', delete_after=10)
                    return
                if cookingLv >= levelReq:
                    if len(player.playerInventory) >= player.playerMaxInventory:
                        await ctx.send(f'Your inventory is full!', delete_after=10)
                        await ctx.message.delete()
                        return
                    await self.cookingLoop(player, item, count, ctx)
                else:
                    await ctx.send(f'You do not have the {levelReq} Cooking required for this!')
                    await ctx.message.delete()
            else:
                await ctx.send(f'Could not find that item!', delete_after=10)
                await ctx.message.delete()

    async def cookingLoop(self, player, item, count, ctx):
        player.isBusy = True
        totalAmt = count
        embed = discord.Embed(title=f"Cooking {item.itemName}", description=f"<@!{player.DiscordID}>",
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
                        embed = discord.Embed(title=f"Cooking {item.itemName}", description=f"<@!{player.DiscordID}>",
                                              color=0xd25151)
                        embed.add_field(name=f'Results', value=f'Crafted {totalAmt - count} {item.itemName}',
                                        inline=True)
                        embed.add_field(name=f'**Stopped**', value=f'Ran out of a resource.',
                                        inline=False)
                        await e.edit(embed=embed)
                        player.isBusy = False
                        return f'Player does not have enough {compItem.itemName} for crafting {item.itemName}'
                else:
                    embed = discord.Embed(title=f"Cooking {item.itemName}", description=f"<@!{player.DiscordID}>",
                                          color=0xd25151)
                    embed.add_field(name=f'Results', value=f'Crafted {totalAmt - count} {item.itemName}',
                                    inline=True)
                    embed.add_field(name=f'**Stopped**', value=f'Ran out of an ingredient.',
                                    inline=False)
                    await e.edit(embed=embed)
                    player.isBusy = False
                    return f'Player does not have {compItem.itemName} for crafting {item.itemName}'
            # At this point, we have removed all of the ingredients from the player
            # So lets give them what they are here for.
            player.addToInventory(item.ID, 1)
            count -= 1
            baseExp = item.xpForCrafting
            xpGained, leveledUp = player.givePlayerExperience("cooking", baseExp)
            if leveledUp:
                await ctx.send(embed=leveledUp, delete_after=300)
            else:
                embed = discord.Embed(title=f"Cooking {item.itemName}", description=f"<@!{player.DiscordID}>",
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
        embed = discord.Embed(title=f"Cooking {item.itemName}", description=f"<@!{player.DiscordID}>",
                              color=0xd25151)
        embed.add_field(name=f'Results', value=f'Cooked {totalAmt - count} {item.itemName}', inline=True)
        try:
            await e.edit(embed=embed)
        except discord.ClientException:
            print(f'Caught some kind of error, attempting to pass.')
            pass
        player.cancelBool = False
        player.isBusy = False





