import asyncio


# This is a class that manages the overall ticker for buffs, that we have also allowed the farming timers to run on.
# Every 0.6s, it will process one 'tick' that ticks down buff durations or growth times on plots.
class BuffMgmtCog:
    def __init__(self, bot):
        self.bot = bot
        self.dRockTime = 0
        self.farmingTick = 0

    def tickBuffs(self, entity):
        for buff in entity.buffs:
            buff.onTick()

    def farmingTicks(self):
        self.farmingTick += 1
        if self.farmingTick == 50:
            for player in self.bot.gameManager.allPlayers:
                for plot in player.farmingPlots:
                    plot.tickGrowth()
            self.farmingTick = 0

    def tickPlayers(self):
        for player in self.bot.gameManager.allPlayers:
            self.tickBuffs(player)


    def tickEnemies(self):
        for enemy in self.bot.gameManager.allEnemies:
            self.tickBuffs(enemy)

    def checkDRockSpawn(self):
        self.dRockTime += 1
        if self.dRockTime >= 1000:
            miningCog = self.bot.get_cog('mining')
            miningCog.spawnDragoniteOre()
            self.dRockTime = 0

    async def theLoop(self):
        while True:
            self.tickPlayers()
            self.tickEnemies()
            self.checkDRockSpawn()
            self.farmingTicks()
            await asyncio.sleep(0.6)
