import random
from abc import abstractmethod, ABC

import discord
from discord.ext import commands, tasks
import asyncio


class WoodcuttingSpot:
    def __init__(self):
        self.name = 'Fish'
        self.maxhp = 1
        self.HP = 1
        self.respawnTime = 1
        self.WoodcuttingReq = 1
        self.logID = 0

    @abstractmethod
    def reduceHP(self):
        self.HP -= 1
        return self.HP

    @abstractmethod
    def respawn(self):
        self.HP = self.maxhp


def treeFactory(ID):
    class NormalTree(WoodcuttingSpot, ABC):
        def __init__(self):
            super().__init__()
            self.name = 'Tree'
            self.maxhp = 2
            self.HP = 2
            self.respawnTime = 3
            self.WoodcuttingReq = 1
            self.logID = 1

    class OakTree(WoodcuttingSpot, ABC):
        def __init__(self):
            super().__init__()
            self.name = 'Oak Tree'
            self.maxhp = 5
            self.HP = 5
            self.respawnTime = 3
            self.WoodcuttingReq = 15
            self.logID = 2

    class WillowTree(WoodcuttingSpot, ABC):
        def __init__(self):
            super().__init__()
            self.name = 'Willow Tree'
            self.maxhp = 20
            self.HP = 20
            self.respawnTime = 10
            self.WoodcuttingReq = 30
            self.logID = 3

    class TeakTree(WoodcuttingSpot, ABC):
        def __init__(self):
            super().__init__()
            self.name = 'Teak Tree'
            self.maxhp = 15
            self.HP = 15
            self.respawnTime = 30
            self.WoodcuttingReq = 35
            self.logID = 4

    class MapleTree(WoodcuttingSpot, ABC):
        def __init__(self):
            super().__init__()
            self.name = 'Maple Tree'
            self.maxhp = 30
            self.HP = 30
            self.respawnTime = 15
            self.WoodcuttingReq = 45
            self.logID = 5

    class MahoganyTree(WoodcuttingSpot, ABC):
        def __init__(self):
            super().__init__()
            self.name = 'Mahogany Tree'
            self.maxhp = 20
            self.HP = 20
            self.respawnTime = 30
            self.WoodcuttingReq = 50
            self.logID = 6

    class YewTree(WoodcuttingSpot, ABC):
        def __init__(self):
            super().__init__()
            self.name = 'Yew Tree'
            self.maxhp = 60
            self.HP = 60
            self.respawnTime = 30
            self.WoodcuttingReq = 60
            self.logID = 7

    class MagicTree(WoodcuttingSpot, ABC):
        def __init__(self):
            super().__init__()
            self.name = 'Magic Tree'
            self.maxhp = 60
            self.HP = 60
            self.respawnTime = 60
            self.WoodcuttingReq = 75
            self.logID = 8

    class RedwoodTree(WoodcuttingSpot, ABC):
        def __init__(self):
            super().__init__()
            self.name = 'Redwood Tree'
            self.maxhp = 100
            self.HP = 100
            self.respawnTime = 100
            self.WoodcuttingReq = 90
            self.logID = 9


    if ID == 1: return NormalTree()
    if ID == 2: return OakTree()
    if ID == 3: return WillowTree()
    if ID == 4: return TeakTree()
    if ID == 5: return MapleTree()
    if ID == 6: return MahoganyTree()
    if ID == 7: return YewTree()
    if ID == 8: return MagicTree()
    if ID == 9: return RedwoodTree()
    assert 0, f'Bad ID: {ID}'



def setup(bot):
    bot.add_cog(woodcutting(bot))
    print('Woodcutting Cog Loaded')


class woodcutting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.levelTable = {"normal": 1,
                           "oak": 15,
                           "willow": 30,
                           "teak": 35,
                           "maple": 45,
                           "mahogany": 50,
                           "yew": 60,
                           "magic": 75,
                           "redwood": 90}


    def gemDrop(self, player):
        playerWoodcuttingLv = player.playerMaxWoodcutting
        gems = [91, 91, 91, 91, 91, 92, 92, 92, 92, 93, 93, 93, 94, 94, 95]
        gemGet = random.choice(gems)
        chanceToGet = (1 + int(playerWoodcuttingLv / 4))
        roll = random.randint(0, 100)
        if roll <= chanceToGet:
            count, gemName = player.addToInventory(gemGet, 1)
            if count == -1:
                player.cancelBool = True
                return f'<@!{player.DiscordID}> inventory full!'
            return f'<@!{player.DiscordID}> got a(n) {gemName}!'
        return None

    async def woodcuttingLoop(self, player, tree, ctx):
        player.isBusy = True
        caught = 0
        output = None
        invFull = False
        treeItem = self.bot.gameManager.itemIDToItem(tree.logID)
        embed = discord.Embed(title=f"Woodcutting {tree.name}", description=f"<@!{player.DiscordID}>",
                              color=0x2b8f1e)
        embed.set_thumbnail(url=treeItem.itemEmoj)
        pBar = int((tree.maxhp - tree.HP) / (tree.maxhp) * 10)
        embed.add_field(name=f'Tree HP', value=f'{"🟪" * pBar}{"⬜" * (10 - pBar)}', inline=False)
        embed.add_field(name=f'Exp Gained', value=f'{0}', inline=True)
        embed.add_field(name=f'Logs Gained', value=f'{caught}', inline=True)
        e = await ctx.send(embed=embed)
        while not player.cancelBool:
            # Spot HP -1
            tree.HP -= 1
            # Give player item
            count, treeName = player.addToInventory(tree.logID, 1)
            if count == -1:
                player.cancelBool = True
                invFull = True
            caught += 1
            output = self.gemDrop(player)
            # Give player experience
            baseExp = treeItem.xpForCrafting
            xpGained, leveledUp = player.givePlayerExperience("woodcutting", baseExp)
            if leveledUp:
                await ctx.send(embed=leveledUp, delete_after=300)
            else:
                embed = discord.Embed(title=f"Woodcutting {tree.name}", description=f"<@!{player.DiscordID}>",
                                      color=0x2b8f1e)
                embed.set_thumbnail(url=treeItem.itemEmoj)
                pBar = int((tree.maxhp - tree.HP) / (tree.maxhp) * 10)
                embed.add_field(name=f'Tree HP', value=f'{"🟪" * (10 - pBar)}{"⬜" * pBar}', inline=False)
                embed.add_field(name=f'Exp Gained', value=f'{(caught * xpGained)}', inline=True)
                embed.add_field(name=f'Logs Gained', value=f'{caught}', inline=True)
                if output:
                    embed.add_field(name=f'Bonus Output', value=f'{output}', inline=True)
                    if 'full' in output:
                        invFull = True
                await e.edit(embed=embed)
                await asyncio.sleep(player.skillingRate)
            if tree.HP <= 0:
                await asyncio.sleep(tree.respawnTime)
                tree.respawn()

        embed = discord.Embed(title=f"Finished Woodcutting {tree.name}", description=f"<@!{player.DiscordID}>",
                              color=0x2b8f1e)
        if invFull:
            embed.add_field(name=f'Stopped Early', value=f'Inventory Full!', inline=True)
        embed.add_field(name=f'Logs Gained', value=f'{caught}', inline=False)
        try:
            await e.edit(embed=embed)
        except discord.ClientException:
            print(f'Caught some kind of error, attempting to pass.')
            pass
        player.isBusy = False
        player.cancelBool = False


    @commands.command(aliases=['chopping', 'Woocutting', 'Woodcutting', 'Woodcuting', 'woodcuting', 'wodcuting', 'woodvutting', 'Woodvutting'])
    async def woodcutting(self, ctx, *args):
        player = self.bot.gameManager.getPlayer(ctx.message.author.id)
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
        playerWoodcuttingLv = player.playerMaxWoodcutting
        if args:
            if str(args[0]).upper() in [x.upper() for x in self.levelTable.keys()]:
                input = str(args[0]).upper()
                if input == 'NORMAL':
                    tree = treeFactory(1)
                    if playerWoodcuttingLv >= tree.WoodcuttingReq:
                        await self.woodcuttingLoop(player, tree, ctx)
                    else:
                        r = await ctx.send(f'You do not have the Woodcutting level for this tree!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                if input == 'OAK':
                    tree = treeFactory(2)
                    if playerWoodcuttingLv >= tree.WoodcuttingReq:
                        await self.woodcuttingLoop(player, tree, ctx)
                    else:
                        r = await ctx.send(f'You do not have the Woodcutting level for this tree!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                if input == 'WILLOW':
                    tree = treeFactory(3)
                    if playerWoodcuttingLv >= tree.WoodcuttingReq:
                        await self.woodcuttingLoop(player, tree, ctx)
                    else:
                        r = await ctx.send(f'You do not have the Woodcutting level for this tree!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                if input == 'TEAK':
                    tree = treeFactory(4)
                    if playerWoodcuttingLv >= tree.WoodcuttingReq:
                        await self.woodcuttingLoop(player, tree, ctx)
                    else:
                        r = await ctx.send(f'You do not have the Woodcutting level for this tree!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                if input == 'MAPLE':
                    tree = treeFactory(5)
                    if playerWoodcuttingLv >= tree.WoodcuttingReq:
                        await self.woodcuttingLoop(player, tree, ctx)
                    else:
                        r = await ctx.send(f'You do not have the Woodcutting level for this tree!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                if input == 'MAHOGANY':
                    tree = treeFactory(6)
                    if playerWoodcuttingLv >= tree.WoodcuttingReq:
                        await self.woodcuttingLoop(player, tree, ctx)
                    else:
                        r = await ctx.send(f'You do not have the Woodcutting level for this tree!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                if input == 'YEW':
                    tree = treeFactory(7)
                    if playerWoodcuttingLv >= tree.WoodcuttingReq:
                        await self.woodcuttingLoop(player, tree, ctx)
                    else:
                        r = await ctx.send(f'You do not have the Woodcutting level for this tree!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                if input == 'MAGIC':
                    tree = treeFactory(8)
                    if playerWoodcuttingLv >= tree.WoodcuttingReq:
                        await self.woodcuttingLoop(player, tree, ctx)
                    else:
                        r = await ctx.send(f'You do not have the Woodcutting level for this tree!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                if input == 'REDWOOD':
                    tree = treeFactory(9)
                    if playerWoodcuttingLv >= tree.WoodcuttingReq:
                        await self.woodcuttingLoop(player, tree, ctx)
                    else:
                        r = await ctx.send(f'You do not have the Woodcutting level for this tree!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
            else:
                r = await ctx.send(f'Invalid tree given.')
                await asyncio.sleep(10)
                await r.delete()
                await ctx.message.delete()
        else:
            embed = discord.Embed(title=f"{ctx.message.author.display_name.capitalize()} Woodcutting",
                                  description=f'',
                                  color=0x2b8f1e)
            # Display all available trees to this player, including the dragon tree if one is available.
            avblSpots = ""
            for tree in self.levelTable:
                if playerWoodcuttingLv >= self.levelTable[tree]:
                    avblSpots += f'{tree.capitalize()}\n'
            embed.add_field(name=f'Available Trees:', value=f'{avblSpots}', inline=True)
            r = await ctx.send(embed=embed)
            await asyncio.sleep(60)
            await r.delete()
            await ctx.message.delete()
