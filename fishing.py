import random
from abc import abstractmethod, ABC

import discord
from discord.ext import commands, tasks
import asyncio


class FishingSpot:
    def __init__(self):
        self.name = 'Fish'
        self.maxhp = 1
        self.HP = 1
        self.respawnTime = 1
        self.FishingReq = 1
        self.fishID = 0

    @abstractmethod
    def reduceHP(self):
        self.HP -= 1
        return self.HP

    @abstractmethod
    def respawn(self):
        self.HP = self.maxhp


def fishFactory(ID):
    class ShrimpSpot(FishingSpot, ABC):
        def __init__(self):
            super().__init__()
            self.name = 'Shrimp Spot'
            self.maxhp = 5
            self.HP = 5
            self.respawnTime = 3
            self.FishingReq = 1
            self.fishID = 10

    class SardineSpot(FishingSpot, ABC):
        def __init__(self):
            super().__init__()
            self.name = 'Sardine Spot'
            self.maxhp = 5
            self.HP = 5
            self.respawnTime = 3
            self.FishingReq = 5
            self.fishID = 11

    class TroutSpot(FishingSpot, ABC):
        def __init__(self):
            super().__init__()
            self.name = 'Trout Spot'
            self.maxhp = 20
            self.HP = 20
            self.respawnTime = 10
            self.FishingReq = 20
            self.fishID = 12

    class SalmonSpot(FishingSpot, ABC):
        def __init__(self):
            super().__init__()
            self.name = 'Salmon Spot'
            self.maxhp = 20
            self.HP = 20
            self.respawnTime = 10
            self.FishingReq = 30
            self.fishID = 13

    class LobsterSpot(FishingSpot, ABC):
        def __init__(self):
            super().__init__()
            self.name = 'Lobster Spot'
            self.maxhp = 30
            self.HP = 30
            self.respawnTime = 15
            self.FishingReq = 40
            self.fishID = 14

    class SwordfishSpot(FishingSpot, ABC):
        def __init__(self):
            super().__init__()
            self.name = 'Swordfish Spot'
            self.maxhp = 30
            self.HP = 30
            self.respawnTime = 15
            self.FishingReq = 50
            self.fishID = 15

    class TunaSpot(FishingSpot, ABC):
        def __init__(self):
            super().__init__()
            self.name = 'Tuna Spot'
            self.maxhp = 30
            self.HP = 30
            self.respawnTime = 15
            self.FishingReq = 35
            self.fishID = 251

    class KarambwanSpot(FishingSpot, ABC):
        def __init__(self):
            super().__init__()
            self.name = 'Karambam Spot'
            self.maxhp = 5
            self.HP = 5
            self.respawnTime = 2
            self.FishingReq = 65
            self.fishID = 252

    class SharkSpot(FishingSpot, ABC):
        def __init__(self):
            super().__init__()
            self.name = 'Shark Spot'
            self.maxhp = 60
            self.HP = 60
            self.respawnTime = 30
            self.FishingReq = 76
            self.fishID = 253

    class MantaSpot(FishingSpot, ABC):
        def __init__(self):
            super().__init__()
            self.name = 'Manta Ray Spot'
            self.maxhp = 30
            self.HP = 30
            self.respawnTime = 15
            self.FishingReq = 81
            self.fishID = 254

    class AnglerSpot(FishingSpot, ABC):
        def __init__(self):
            super().__init__()
            self.name = 'Anglerfish Spot'
            self.maxhp = 5
            self.HP = 5
            self.respawnTime = 15
            self.FishingReq = 90
            self.fishID = 255


    if ID == 1: return ShrimpSpot()
    if ID == 2: return SardineSpot()
    if ID == 3: return TroutSpot()
    if ID == 4: return SalmonSpot()
    if ID == 5: return LobsterSpot()
    if ID == 6: return SwordfishSpot()
    if ID == 7: return TunaSpot()
    if ID == 8: return KarambwanSpot()
    if ID == 9: return SharkSpot()
    if ID == 10: return MantaSpot()
    if ID == 11: return AnglerSpot()
    assert 0, f'Bad ID: {ID}'



def setup(bot):
    bot.add_cog(fishing(bot))
    print('Fishing Cog Loaded')


class fishing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.levelTable = {"shrimp": 1,
                           "sardine": 5,
                           "trout": 20,
                           "salmon": 30,
                           "tuna": 35,
                           "lobster": 40,
                           "swordfish": 50,
                           "karambwan": 65,
                           "shark": 76,
                           "mantaray": 81,
                           "anglerfish": 90}


    def gemDrop(self, player):
        playerFishingLv = player.playerMaxFishing
        gems = [91, 91, 91, 91, 91, 92, 92, 92, 92, 93, 93, 93, 94, 94, 95]
        gemGet = random.choice(gems)
        chanceToGet = (1 + int(playerFishingLv / 4))
        roll = random.randint(0, 100)
        if roll <= chanceToGet:
            count, gemName = player.addToInventory(gemGet, 1)
            if count == -1:
                player.cancelBool = True
                return f'<@!{player.DiscordID}> inventory full!'
            return f'<@!{player.DiscordID}> got a(n) {gemName}!'
        return None

    async def fishingLoop(self, player, fish, ctx):
        player.isBusy = True
        caught = 0
        output = None
        invFull = False
        fishItem = self.bot.gameManager.itemIDToItem(fish.fishID)
        embed = discord.Embed(title=f"Fishing {fish.name}", description=f"<@!{player.DiscordID}>",
                              color=0x56b3d2)
        embed.set_thumbnail(url=fishItem.itemEmoj)
        pBar = int((fish.maxhp - fish.HP) / (fish.maxhp) * 10)
        embed.add_field(name=f'Spots HP', value=f'{"🟪" * pBar}{"⬜" * (10 - pBar)}', inline=False)
        embed.add_field(name=f'Exp Gained', value=f'{0}', inline=True)
        embed.add_field(name=f'Fish Gained', value=f'{caught}', inline=True)
        e = await ctx.send(embed=embed)
        while not player.cancelBool:
            # Spot HP -1
            fish.HP -= 1
            # Give player item
            count, fishName = player.addToInventory(fish.fishID, 1)
            if count == -1:
                player.cancelBool = True
                invFull = True
            caught += 1
            output = self.gemDrop(player)
            # Give player experience
            baseExp = fishItem.xpForCrafting
            xpGained, leveledUp = player.givePlayerExperience("fishing", baseExp)
            if leveledUp:
                await ctx.send(embed=leveledUp, delete_after=300)
            else:
                embed = discord.Embed(title=f"Fishing {fish.name}", description=f"<@!{player.DiscordID}>",
                                      color=0x56b3d2)
                embed.set_thumbnail(url=fishItem.itemEmoj)
                pBar = int((fish.maxhp - fish.HP) / (fish.maxhp) * 10)
                embed.add_field(name=f'Spots HP', value=f'{"🟪" * (10 - pBar)}{"⬜" * pBar}', inline=False)
                embed.add_field(name=f'Exp Gained', value=f'{(caught * xpGained)}', inline=True)
                embed.add_field(name=f'Fish Gained', value=f'{caught}', inline=True)
                if output:
                    embed.add_field(name=f'Bonus Output', value=f'{output}', inline=True)
                    if 'full' in output:
                        invFull = True
                await e.edit(embed=embed)
                await asyncio.sleep(player.skillingRate)
            if fish.HP <= 0:
                await asyncio.sleep(fish.respawnTime)
                fish.respawn()

        embed = discord.Embed(title=f"Finished Fishing {fish.name}", description=f"<@!{player.DiscordID}>",
                              color=0x56b3d2)
        if invFull:
            embed.add_field(name=f'Stopped Early', value=f'Inventory Full!', inline=True)
        embed.add_field(name=f'Fish Gained', value=f'{caught}', inline=False)
        try:
            await e.edit(embed=embed)
        except discord.ClientException:
            print(f'Caught some kind of error, attempting to pass.')
            pass
        player.isBusy = False
        player.cancelBool = False


    @commands.command(aliases=['Fishing', 'fshing', 'Fshing', 'Fish', 'fish', 'Fihsing', 'fihsing', 'fihs'])
    async def fishing(self, ctx, *args):
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
        playerFishingLv = player.playerMaxFishing
        if args:
            if str(args[0]).upper() in [x.upper() for x in self.levelTable.keys()]:
                input = str(args[0]).upper()
                if input == 'SHRIMP':
                    fish = fishFactory(1)
                    if playerFishingLv >= fish.FishingReq:
                        await self.fishingLoop(player, fish, ctx)
                    else:
                        r = await ctx.send(f'You do not have the Fishing level for this fish!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                if input == 'SARDINE':
                    fish = fishFactory(2)
                    if playerFishingLv >= fish.FishingReq:
                        await self.fishingLoop(player, fish, ctx)
                    else:
                        r = await ctx.send(f'You do not have the Fishing level for this fish!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                if input == 'TROUT':
                    fish = fishFactory(3)
                    if playerFishingLv >= fish.FishingReq:
                        await self.fishingLoop(player, fish, ctx)
                    else:
                        r = await ctx.send(f'You do not have the Fishing level for this fish!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                if input == 'SALMON':
                    fish = fishFactory(4)
                    if playerFishingLv >= fish.FishingReq:
                        await self.fishingLoop(player, fish, ctx)
                    else:
                        r = await ctx.send(f'You do not have the Fishing level for this fish!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                if input == 'LOBSTER':
                    fish = fishFactory(5)
                    if playerFishingLv >= fish.FishingReq:
                        await self.fishingLoop(player, fish, ctx)
                    else:
                        r = await ctx.send(f'You do not have the Fishing level for this fish!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                if input == 'SWORDFISH':
                    fish = fishFactory(6)
                    if playerFishingLv >= fish.FishingReq:
                        await self.fishingLoop(player, fish, ctx)
                    else:
                        r = await ctx.send(f'You do not have the Fishing level for this fish!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                if input == 'TUNA':
                    fish = fishFactory(7)
                    if playerFishingLv >= fish.FishingReq:
                        await self.fishingLoop(player, fish, ctx)
                    else:
                        r = await ctx.send(f'You do not have the Fishing level for this fish!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                if input == 'KARAMBWAN':
                    fish = fishFactory(8)
                    if playerFishingLv >= fish.FishingReq:
                        await self.fishingLoop(player, fish, ctx)
                    else:
                        r = await ctx.send(f'You do not have the Fishing level for this fish!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                if input == 'SHARK':
                    fish = fishFactory(9)
                    if playerFishingLv >= fish.FishingReq:
                        await self.fishingLoop(player, fish, ctx)
                    else:
                        r = await ctx.send(f'You do not have the Fishing level for this fish!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                if input == 'MANTARAY':
                    fish = fishFactory(10)
                    if playerFishingLv >= fish.FishingReq:
                        await self.fishingLoop(player, fish, ctx)
                    else:
                        r = await ctx.send(f'You do not have the Fishing level for this fish!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                if input == 'ANGLERFISH':
                    fish = fishFactory(11)
                    if playerFishingLv >= fish.FishingReq:
                        await self.fishingLoop(player, fish, ctx)
                    else:
                        r = await ctx.send(f'You do not have the Fishing level for this fish!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
            else:
                r = await ctx.send(f'Invalid fish given.')
                await asyncio.sleep(10)
                await r.delete()
                await ctx.message.delete()
        else:
            embed = discord.Embed(title=f"{ctx.message.author.display_name.capitalize()} Fishing",
                                  description=f'',
                                  color=0x56b3d2)
            # Display all available fishs to this player, including the dragon fish if one is available.
            avblSpots = ""
            for fish in self.levelTable:
                if playerFishingLv >= self.levelTable[fish]:
                    avblSpots += f'{fish.capitalize()}\n'
            embed.add_field(name=f'Available Spots:', value=f'{avblSpots}', inline=True)
            r = await ctx.send(embed=embed)
            await asyncio.sleep(60)
            await r.delete()
            await ctx.message.delete()
