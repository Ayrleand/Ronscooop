import random
from abc import abstractmethod, ABC

import discord
from discord.ext import commands, tasks
import asyncio


# 1 bar
# Goes until cancelled or bot resets

class MiningRock:
    def __init__(self):
        self.name = 'Rock'
        self.maxhp = 1
        self.HP = 1
        self.respawnTime = 1
        self.miningReq = 1
        self.oreID = 0

    @abstractmethod
    def reduceHP(self):
        self.HP -= 1
        return self.HP

    @abstractmethod
    def respawn(self):
        self.HP = self.maxhp


def rockFactory(ID):
    class CopperRock(MiningRock, ABC):
        def __init__(self):
            super().__init__()
            self.name = 'Copper Rock'
            self.miningReq = 1
            self.oreID = 16

    class TinRock(MiningRock, ABC):
        def __init__(self):
            super().__init__()
            self.name = 'Tin Rock'
            self.miningReq = 1
            self.oreID = 17

    class IronRock(MiningRock, ABC):
        def __init__(self):
            super().__init__()
            self.name = 'Iron Rock'
            self.maxhp = 5
            self.HP = 5
            self.respawnTime = 3
            self.miningReq = 15
            self.oreID = 18

    class SilverRock(MiningRock, ABC):
        def __init__(self):
            super().__init__()
            self.name = 'Silver Rock'
            self.maxhp = 10
            self.HP = 10
            self.respawnTime = 10
            self.miningReq = 20
            self.oreID = 20

    class CoalRock(MiningRock, ABC):
        def __init__(self):
            super().__init__()
            self.name = 'Coal Rock'
            self.maxhp = 30
            self.HP = 30
            self.respawnTime = 15
            self.miningReq = 30
            self.oreID = 19

    class GoldRock(MiningRock, ABC):
        def __init__(self):
            super().__init__()
            self.name = 'Gold Rock'
            self.maxhp = 10
            self.HP = 10
            self.respawnTime = 30
            self.miningReq = 40
            self.oreID = 21

    class MithrilRock(MiningRock, ABC):
        def __init__(self):
            super().__init__()
            self.name = 'Mithril Rock'
            self.maxhp = 20
            self.HP = 20
            self.respawnTime = 20
            self.miningReq = 50
            self.oreID = 22

    class AdamantiteRock(MiningRock, ABC):
        def __init__(self):
            super().__init__()
            self.name = 'Adamantite Rock'
            self.maxhp = 20
            self.HP = 20
            self.respawnTime = 30
            self.miningReq = 60
            self.oreID = 23

    class RuniteRock(MiningRock, ABC):
        def __init__(self):
            super().__init__()
            self.name = 'Runite Rock'
            self.maxhp = 20
            self.HP = 20
            self.respawnTime = 30
            self.miningReq = 70
            self.oreID = 24

    class DragoniteRock(MiningRock, ABC):
        def __init__(self):
            super().__init__()
            self.name = 'Dragonite Rock'
            self.maxhp = 20
            self.HP = 20
            self.respawnTime = 60
            self.miningReq = 85
            self.oreID = 25

    if ID == 1: return CopperRock()
    if ID == 2: return TinRock()
    if ID == 3: return IronRock()
    if ID == 4: return SilverRock()
    if ID == 5: return CoalRock()
    if ID == 6: return GoldRock()
    if ID == 7: return MithrilRock()
    if ID == 8: return AdamantiteRock()
    if ID == 9: return RuniteRock()
    if ID == 10: return DragoniteRock()
    assert 0, f'Bad ID: {ID}'



def setup(bot):
    bot.add_cog(mining(bot))
    print('Mining Cog Loaded')


class mining(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dragoniteSpawn = []
        self.levelTable = {"copper": 1,
                           "tin": 1,
                           "iron": 15,
                           "silver": 20,
                           "coal": 30,
                           "gold": 40,
                           "mithril": 50,
                           "adamantite": 60,
                           "runite": 70,
                           "dragonite": 85}

    def gemDrop(self, player):
        playerMiningLv = player.playerMaxMining
        gems = [91, 91, 91, 91, 91, 92, 92, 92, 92, 93, 93, 93, 94, 94, 95]
        gemGet = random.choice(gems)
        chanceToGet = (5 + int(playerMiningLv / 4))
        roll = random.randint(0, 100)
        if roll <= chanceToGet:
            count, gemName = player.addToInventory(gemGet, 1)
            if count == -1:
                player.cancelBool = True
                return f'<@!{player.DiscordID}> inventory full!'
            return f'<@!{player.DiscordID}> got a(n) {gemName}!'
        return None

    def spawnDragoniteOre(self):
        rock = rockFactory(10)
        if len(self.dragoniteSpawn) <= 5:
            self.dragoniteSpawn.append(rock)

    async def miningLoop(self, player, rock, ctx):
        player.isBusy = True
        mined = 0
        output = None
        invFull = False
        oreItem = self.bot.gameManager.itemIDToItem(rock.oreID)
        embed = discord.Embed(title=f"Mining {rock.name}", description=f"<@!{player.DiscordID}>",
                              color=0x7f592f)
        embed.set_thumbnail(url=oreItem.itemEmoj)
        pBar = int((rock.maxhp - rock.HP) / (rock.maxhp) * 10)
        embed.add_field(name=f'Rock HP', value=f'{"🟪" * pBar}{"⬜" * (10 - pBar)}', inline=False)
        embed.add_field(name=f'Exp Gained', value=f'{0}', inline=True)
        embed.add_field(name=f'Ore Gained', value=f'{mined}', inline=True)
        e = await ctx.send(embed=embed)
        while not player.cancelBool:
            # Rock HP -1
            rock.HP -= 1
            # Give player item
            count, oreName = player.addToInventory(rock.oreID, 1)
            if count == -1:
                player.cancelBool = True
                invFull = True
            mined += 1
            output = self.gemDrop(player)
            # Give player experience
            baseExp = oreItem.xpForCrafting
            xpGained, leveledUp = player.givePlayerExperience("mining", baseExp)
            if leveledUp:
                await ctx.send(embed=leveledUp, delete_after=300)
            else:
                embed = discord.Embed(title=f"Mining {rock.name}", description=f"<@!{player.DiscordID}>",
                                      color=0x7f592f)
                embed.set_thumbnail(url=oreItem.itemEmoj)
                pBar = int((rock.maxhp - rock.HP) / (rock.maxhp) * 10)
                embed.add_field(name=f'Rock HP', value=f'{"🟪" * (10 - pBar)}{"⬜" * pBar}', inline=False)
                embed.add_field(name=f'Exp Gained', value=f'{(mined * xpGained)}', inline=True)
                embed.add_field(name=f'Ore Gained', value=f'{mined}', inline=True)
                if output:
                    embed.add_field(name=f'Bonus Output', value=f'{output}', inline=True)
                    if 'full' in output:
                        invFull = True
                await e.edit(embed=embed)
                await asyncio.sleep(player.skillingRate)
            if rock.HP <= 0:
                await asyncio.sleep(rock.respawnTime)
                rock.respawn()

        embed = discord.Embed(title=f"Finished mining {rock.name}", description=f"<@!{player.DiscordID}>",
                              color=0x7f592f)
        if invFull:
            embed.add_field(name=f'Stopped Early', value=f'Inventory Full!', inline=True)
        embed.add_field(name=f'Ore Gained', value=f'{mined}', inline=False)
        try:
            await e.edit(embed=embed)
        except discord.ClientException:
            print(f'Caught some kind of error, attempting to pass.')
            pass
        player.isBusy = False
        player.cancelBool = False


    @commands.command(aliases=['Mining', 'minign', 'Minign', 'Mine', 'mine', 'minnig', 'Minnig'])
    async def mining(self, ctx, *args):
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
        playerMiningLv = player.playerMaxMining
        if args:
            if str(args[0]).upper() in ['COPPER', 'TIN', 'IRON', 'SILVER', 'COAL', 'GOLD', 'MITHRIL', 'ADAMANTITE',
                                        'RUNITE', 'DRAGONITE']:
                input = str(args[0]).upper()
                if input == 'COPPER':
                    rock = rockFactory(1)
                    if playerMiningLv >= rock.miningReq:
                        await self.miningLoop(player, rock, ctx)
                    else:
                        r = await ctx.send(f'You do not have the mining level for this rock!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                if input == 'TIN':
                    rock = rockFactory(2)
                    if playerMiningLv >= rock.miningReq:
                        await self.miningLoop(player, rock, ctx)
                    else:
                        r = await ctx.send(f'You do not have the mining level for this rock!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                if input == 'IRON':
                    rock = rockFactory(3)
                    if playerMiningLv >= rock.miningReq:
                        await self.miningLoop(player, rock, ctx)
                    else:
                        r = await ctx.send(f'You do not have the mining level for this rock!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                if input == 'SILVER':
                    rock = rockFactory(4)
                    if playerMiningLv >= rock.miningReq:
                        await self.miningLoop(player, rock, ctx)
                    else:
                        r = await ctx.send(f'You do not have the mining level for this rock!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                if input == 'COAL':
                    rock = rockFactory(5)
                    if playerMiningLv >= rock.miningReq:
                        await self.miningLoop(player, rock, ctx)
                    else:
                        r = await ctx.send(f'You do not have the mining level for this rock!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                if input == 'GOLD':
                    rock = rockFactory(6)
                    if playerMiningLv >= rock.miningReq:
                        await self.miningLoop(player, rock, ctx)
                    else:
                        r = await ctx.send(f'You do not have the mining level for this rock!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                if input == 'MITHRIL':
                    rock = rockFactory(7)
                    if playerMiningLv >= rock.miningReq:
                        await self.miningLoop(player, rock, ctx)
                    else:
                        r = await ctx.send(f'You do not have the mining level for this rock!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                if input == 'ADAMANTITE':
                    rock = rockFactory(8)
                    if playerMiningLv >= rock.miningReq:
                        await self.miningLoop(player, rock, ctx)
                    else:
                        r = await ctx.send(f'You do not have the mining level for this rock!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                if input == 'RUNITE':
                    rock = rockFactory(9)
                    if playerMiningLv >= rock.miningReq:
                        await self.miningLoop(player, rock, ctx)
                    else:
                        r = await ctx.send(f'You do not have the mining level for this rock!')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
                if input == 'DRAGONITE':
                    if len(self.dragoniteSpawn) > 0:
                        rock = self.dragoniteSpawn[0]
                        self.dragoniteSpawn.remove(rock)
                        if playerMiningLv >= rock.miningReq:
                            await self.miningLoop(player, rock, ctx)
                        else:
                            r = await ctx.send(f'You do not have the mining level for this rock!')
                            await asyncio.sleep(10)
                            await r.delete()
                            await ctx.message.delete()
                    else:
                        r = await ctx.send(
                            f'You could not find a dragonite ore vein to mine! They are rare, after all.')
                        await asyncio.sleep(10)
                        await r.delete()
                        await ctx.message.delete()
            else:
                r = await ctx.send(f'Invalid rock given.')
                await asyncio.sleep(10)
                await r.delete()
                await ctx.message.delete()
        else:
            embed = discord.Embed(title=f"{ctx.message.author.display_name.capitalize()} Mining",
                                  description=f'',
                                  color=0x7f592f)
            # Display all available rocks to this player, including the dragon rock if one is available.
            avblRocks = ""
            for rock in self.levelTable:
                if playerMiningLv >= self.levelTable[rock]:
                    if rock == 'dragonite':
                        if len(self.dragoniteSpawn) > 0:
                            avblRocks += f'{len(self.dragoniteSpawn)} dragonite ore is available!\n'
                        else:
                            avblRocks += f'No dragonite for now...\n'
                    avblRocks += f'{rock.capitalize()}\n'
            embed.add_field(name=f'Available Rocks:', value=f'{avblRocks}', inline=True)
            r = await ctx.send(embed=embed)
            await asyncio.sleep(60)
            await r.delete()
            await ctx.message.delete()
