import random
from abc import abstractmethod, ABC
import discord
from discord.ext import commands, tasks
import asyncio


# The Farming cog, where player state involving farming is interacted with.
# Farming is where players take seeds, put them into a farming plot, and after a certain period of time, they get crops

# Players can !harvest to automatically harvest all of their harvestable crops
# In the future, perhaps we could add an upgrade for plots to automatically harvest, for less exp or crops.

class FilledPlot:
    def __init__(self, owner):
        self.plotID = 0
        self.plotName = ""
        self.growTime = 0
        self.cropID = 0
        self.harvestable = False
        self.maxHarvestNum = 0
        self.xpPerHarvest = 0
        self.farmingReq = 1
        self.onCreate(owner)

    @abstractmethod
    def onCreate(self, owner):
        self.owner = owner

    @abstractmethod
    def tickGrowth(self):
        self.growTime -= 1
        if self.growTime <= 0:
            self.harvestable = True
        return self.growTime

    @abstractmethod
    async def harvest(self, ctx):
        if self.harvestable == True:
            minHarv = int(self.maxHarvestNum * 0.8)
            harvest = random.randint(minHarv, self.maxHarvestNum)
            if self.owner.checkCompost():
                self.owner.addToInventory(111, -1)
                harvest = int(harvest * 1.5)
            count, cropName = self.owner.addToInventory(self.cropID, harvest)
            if count == -1:
                # Player inventory is full.
                return f'Your inventory is full!'
            # TODO: Add Compost Handling here by adding a function to player
            baseExp = self.xpPerHarvest * harvest
            xpGained, leveledUp = self.owner.givePlayerExperience("farming", baseExp)
            if leveledUp:
                await ctx.send(embed=leveledUp, delete_after=300)
            self.owner.remFarmingPlot(self)
            return f'<@!{self.owner.DiscordID}> harvests {harvest} {self.plotName}(s), gaining {xpGained} Farming Experience!'

        else:
            return f'That is not harvestable yet!'


def farmFactory(ID, owner):
    class PotatoPlot(FilledPlot, ABC):
        def __init__(self, owner):
            super().__init__(owner)
            self.plotID = 96
            self.plotName = "Potato"
            self.growTime = 80
            self.cropID = 104
            self.harvestable = False
            self.maxHarvestNum = 10
            self.xpPerHarvest = 8

    class OnionPlot(FilledPlot, ABC):
        def __init__(self, owner):
            super().__init__(owner)
            self.plotID = 97
            self.plotName = "Onion"
            self.growTime = 80
            self.cropID = 105
            self.harvestable = False
            self.maxHarvestNum = 10
            self.xpPerHarvest = 11
            self.farmingReq = 5

    class CabbagePlot(FilledPlot, ABC):
        def __init__(self, owner):
            super().__init__(owner)
            self.plotID = 98
            self.plotName = "Cabbage"
            self.growTime = 80
            self.cropID = 106
            self.harvestable = False
            self.maxHarvestNum = 10
            self.xpPerHarvest = 12
            self.farmingReq = 7

    class TomatoPlot(FilledPlot, ABC):
        def __init__(self, owner):
            super().__init__(owner)
            self.plotID = 99
            self.plotName = "Tomato"
            self.growTime = 80
            self.cropID = 250
            self.harvestable = False
            self.maxHarvestNum = 10
            self.xpPerHarvest = 15
            self.farmingReq = 10

    class CornPlot(FilledPlot, ABC):
        def __init__(self, owner):
            super().__init__(owner)
            self.plotID = 100
            self.plotName = "Corn"
            self.growTime = 80
            self.cropID = 107
            self.harvestable = False
            self.maxHarvestNum = 10
            self.xpPerHarvest = 19
            self.farmingReq = 20

    class StrawberryPlot(FilledPlot, ABC):
        def __init__(self, owner):
            super().__init__(owner)
            self.plotID = 101
            self.plotName = "Strawberry"
            self.growTime = 120
            self.cropID = 108
            self.harvestable = False
            self.maxHarvestNum = 10
            self.xpPerHarvest = 29
            self.farmingReq = 31

    class WatermelonPlot(FilledPlot, ABC):
        def __init__(self, owner):
            super().__init__(owner)
            self.plotID = 102
            self.plotName = "Watermelon"
            self.growTime = 160
            self.cropID = 109
            self.harvestable = False
            self.maxHarvestNum = 10
            self.xpPerHarvest = 29
            self.farmingReq = 47

    class SnapeGrassPlot(FilledPlot, ABC):
        def __init__(self, owner):
            super().__init__(owner)
            self.plotID = 103
            self.plotName = "Snape Grass"
            self.growTime = 30
            self.cropID = 110
            self.harvestable = False
            self.maxHarvestNum = 10
            self.xpPerHarvest = 82
            self.farmingReq = 61

    class OakPlot(FilledPlot, ABC):
        def __init__(self, owner):
            super().__init__(owner)
            self.plotID = 112
            self.plotName = "Oak Tree"
            self.growTime = 400
            self.cropID = 2
            self.harvestable = False
            self.maxHarvestNum = 250
            self.xpPerHarvest = 2
            self.farmingReq = 15

    class WillowPlot(FilledPlot, ABC):
        def __init__(self, owner):
            super().__init__(owner)
            self.plotID = 113
            self.plotName = "Willow Tree"
            self.growTime = 560
            self.cropID = 3
            self.harvestable = False
            self.maxHarvestNum = 250
            self.xpPerHarvest = 6
            self.farmingReq = 30

    class MaplePlot(FilledPlot, ABC):
        def __init__(self, owner):
            super().__init__(owner)
            self.plotID = 114
            self.plotName = "Maple Tree"
            self.growTime = 640
            self.cropID = 5
            self.harvestable = False
            self.maxHarvestNum = 250
            self.xpPerHarvest = 14
            self.farmingReq = 45

    class YewPlot(FilledPlot, ABC):
        def __init__(self, owner):
            super().__init__(owner)
            self.plotID = 115
            self.plotName = "Yew Tree"
            self.growTime = 800
            self.cropID = 7
            self.harvestable = False
            self.maxHarvestNum = 250
            self.xpPerHarvest = 28
            self.farmingReq = 60

    class MagicPlot(FilledPlot, ABC):
        def __init__(self, owner):
            super().__init__(owner)
            self.plotID = 116
            self.plotName = "Magic Tree"
            self.growTime = 960
            self.cropID = 8
            self.harvestable = False
            self.maxHarvestNum = 250
            self.xpPerHarvest = 55
            self.farmingReq = 75

    if ID == 96: return PotatoPlot(owner)
    if ID == 97: return OnionPlot(owner)
    if ID == 98: return CabbagePlot(owner)
    if ID == 99: return TomatoPlot(owner)
    if ID == 100: return CornPlot(owner)
    if ID == 101: return StrawberryPlot(owner)
    if ID == 102: return WatermelonPlot(owner)
    if ID == 103: return SnapeGrassPlot(owner)
    if ID == 112: return OakPlot(owner)
    if ID == 113: return WillowPlot(owner)
    if ID == 114: return MaplePlot(owner)
    if ID == 115: return YewPlot(owner)
    if ID == 116: return MagicPlot(owner)
    assert 0, f'Bad ID: {ID}'


def setup(bot):
    bot.add_cog(farming(bot))
    print('Farming Cog Loaded')


class farming(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.seedIDs = [96, 97, 98, 99, 100, 101, 102, 103, 112, 113, 114, 115, 116]

    @commands.command(name='checkPlots', aliases=['farm', 'checkFarm', 'checkfarm', 'checkplots', 'plots', 'CheckPlots', 'Farm'])
    async def checkPlots(self, ctx, *args):
        player = self.bot.gameManager.getPlayer(ctx.message.author.id)
        farmMessage = "Plots: \n"
        embed = discord.Embed(title=f"{ctx.message.author.display_name.capitalize()}'s Farm",
                              description=f"<@!{player.DiscordID}>",
                              color=0x3fab47)
        embed.set_thumbnail(url='https://oldschool.runescape.wiki/images/Farming_icon.png?558fa')
        for plot in player.farmingPlots:
            if plot.harvestable:
                embed.add_field(name=f'{plot.plotName}', value=f'🪴', inline=True)
            else:
                embed.add_field(name=f'{plot.plotName}', value=f'🌱 ({plot.growTime * 30}s)', inline=True)
        await ctx.send(embed=embed, delete_after=60)
        await asyncio.sleep(10)
        await ctx.message.delete()

    @commands.command(name='plant', aliases=['sow', 'grow', 'till', 'Plant', 'plnta', 'palnt', 'Palnt'])
    async def plant(self, ctx, *args):
        player = self.bot.gameManager.getPlayer(ctx.message.author.id)
        avblSeeds = [x for x in player.playerInventory.keys() if int(x) in self.seedIDs]
        if not args:
            await ctx.send(f'Please provide a seed name or ID to plant! Available options: {avblSeeds}',
                           delete_after=10)
            await asyncio.sleep(10)
            await ctx.message.delete()
        else:
            seed = self.bot.gameManager.inputToItem(args[0])
            try:
                amount = int(args[1])
            except IndexError:
                amount = 1
            if str(seed.ID) in avblSeeds:
                # Adding a plot and ticking the plot are both things that have DB need
                # So maybe they should be handled by the player?
                plot = farmFactory(seed.ID, player)
                if plot.farmingReq <= player.playerMaxFarming:
                    for i in range(amount):
                        m = player.addFarmingPlot(plot)
                        await ctx.send(f'{m}', delete_after=15)
                    await asyncio.sleep(10)
                    await ctx.message.delete()
                else:
                    await ctx.send(f'You do not have the {plot.farmingReq} farming level to do that!', delete_after=20)
                    await asyncio.sleep(10)
                    await ctx.message.delete()

            else:
                await ctx.send(f'Either you dont have that seed, or that is not a seed.', delete_after=20)
                await asyncio.sleep(10)
                await ctx.message.delete()

    @commands.command(name='harvest', aliases=['pick', 'kkona', 'Harvest', 'Pick', 'hravest', 'harvset', 'Hravest', 'Harvset'])
    async def harvest(self, ctx, *args):
        player = self.bot.gameManager.getPlayer(ctx.message.author.id)
        harvested = 0
        for plot in player.farmingPlots[:]:
            if plot.harvestable:
                message = await plot.harvest(ctx)
                harvested += 1
                await ctx.send(message, delete_after=30)
        await ctx.send(f'Harvested {harvested} plants!', delete_after=30)
        await asyncio.sleep(10)
        await ctx.message.delete()

    @commands.command(name='upgradeFarm', aliases=['morefarm', 'moreFarm', 'expandFarm', 'expandfarm', 'buyPlot', 'UpgradeFarm'])
    async def upgradeFarm(self, ctx, *args):
        player = self.bot.gameManager.getPlayer(ctx.message.author.id)
        playerFarmingLv = player.playerMaxFarming
        playerPlots = player.playerMaxFarmingPlots
        cost = (playerPlots + 1)*10000
        if int(playerFarmingLv / playerPlots) >= 1:
            message = await ctx.send(
                f'{ctx.message.author.display_name.capitalize()} has a farm size of {player.playerMaxFarmingPlots}.\n'
                f'Would you like to spend {cost} Scrip to increase this by one?')
            await message.add_reaction('\N{THUMBS UP SIGN}')

            def reactUserCheck(reaction, user):
                return user == ctx.message.author and str(reaction.emoji) in '\N{THUMBS UP SIGN}'

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=reactUserCheck)
            except asyncio.TimeoutError:
                await message.edit(content=f'Request timed out!')
                await asyncio.sleep(10)
                await message.delete()
                await ctx.message.delete()
                return
            if player.playerScrip >= cost:
                a = player.expandFarm()
                player.changeScrip(-cost)
                await message.edit(
                    content=f'Expanded your farm! {ctx.message.author.display_name} now has an farm size of {a}!')
                await asyncio.sleep(10)
                await message.delete()
                await ctx.message.delete()
            else:
                await message.edit(content=f'Sorry, you don\'t have {cost} Scrip to spend!')
                await asyncio.sleep(10)
                await message.delete()
                await ctx.message.delete()
        else:
            await ctx.send(f'You are already at your current maximum farm size!', delete_after=10)
            await asyncio.sleep(10)
            await ctx.message.delete()