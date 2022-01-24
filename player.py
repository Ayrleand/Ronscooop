# Player class who's instances will contain state for each user on the discord server, at all times.
import random
import buffsdebuffs
import discord
import asyncio
from farming import farmFactory


class Player:
    def __init__(self, user, bot):
        print('Created a player')
        self.bot = bot
        self.userDB = self.bot.db.testuserdata.find_one({"Player.Info.DiscordID": user.id})
        # Is, and always will be, a Player
        self.isPlayer = True
        # DiscordID
        self.DiscordID = self.userDB["Player"]["Info"]["DiscordID"]
        # Player Buff List
        self.buffs = []

        # Player Stats and Modifiers
        # General Stats and Modifiers
        self.playerXPRate = self.userDB["Player"]["Modifiers"]["experienceRate"]
        self.playerCurrencyRate = self.userDB["Player"]["Modifiers"]["currencyGainRate"]

        # Combat Stats and Modifiers

        # Hitpoints and Damage Taken Modifier
        self.playerMaxHP = self.userDB["Player"]["Skills"]["maxhp"]["Level"]
        self.playerCurrentHP = int(self.playerMaxHP)
        self.damageTakenMod = 1.0

        # Melee Stats and Damage Dealt Modifier
        self.playerMaxAttack = self.userDB["Player"]["Skills"]["attack"]["Level"]
        self.playerMaxStrength = self.userDB["Player"]["Skills"]["strength"]["Level"]
        self.playerMaxDefence = self.userDB["Player"]["Skills"]["defence"]["Level"]
        self.playerCurrentAttack = int(self.playerMaxAttack)
        self.playerCurrentStrength = int(self.playerMaxStrength)
        self.playerCurrentDefence = int(self.playerMaxDefence)
        self.meleeDamageDealtMod = 1.0

        # Ranged Stats and Damage Dealt Modifier
        self.playerMaxRanged = self.userDB["Player"]["Skills"]["ranged"]["Level"]
        self.playerCurrentRanged = self.playerMaxRanged
        self.rangedDamageDealtMod = 1.0

        # Magic Stats and Damage Dealt Modifier
        self.playerMaxMagic = self.userDB["Player"]["Skills"]["magic"]["Level"]
        self.playerCurrentMagic = self.playerMaxMagic
        self.magicDamageDealtMod = 1.0
        self.infiniteAir = False
        self.infiniteWater = False
        self.infiniteEarth = False
        self.infiniteFire = False

        # Prayer Stats and Drain Modifier
        self.playerMaxPrayer = self.userDB["Player"]["Skills"]["prayer"]["Level"]
        self.playerCurrentPrayer = int(self.playerMaxPrayer)
        self.prayerDrainMod = 1.0

        # General Combat Modifiers
        self.playerCombatStyle = "attack"
        self.playerAtkSpeedMod = 0
        self.playerAttackDelay = 0
        self.playerEatDelay = 0

        # Auto Eating
        self.playerFood = self.userDB["Player"]["Info"]["food"]
        self.autoEatModifier = 1

        # Skilling Stats and Modifiers
        self.skillingRate = self.userDB["Player"]["Modifiers"]["skillingRate"]
        # Mining Stats and Modifiers
        self.playerMaxMining = self.userDB["Player"]["Skills"]["mining"]["Level"]
        self.playerCurrentMining = int(self.playerMaxMining)
        # Fishing Stats and Modifiers
        self.playerMaxFishing = self.userDB["Player"]["Skills"]["fishing"]["Level"]
        self.playerCurrentFishing = int(self.playerMaxFishing)
        # Woodcutting State and Modifiers
        self.playerMaxWoodcutting = self.userDB["Player"]["Skills"]["woodcutting"]["Level"]
        self.playerCurrentWoodcutting = int(self.playerMaxWoodcutting)
        # Farming Stats and Modifiers
        self.playerMaxFarming = self.userDB["Player"]["Skills"]["farming"]["Level"]
        self.playerCurrentFarming = int(self.playerMaxFarming)
        self.playerMaxFarmingPlots = self.userDB["Player"]["Info"]["maxplots"]
        self.farmingPlots = []

        # Smithing Stats and Modifiers
        self.playerMaxSmithing = self.userDB["Player"]["Skills"]["smithing"]["Level"]
        self.playerCurrentSmithing = int(self.playerMaxSmithing)
        # Crafting Stats and Modifiers
        self.playerMaxCrafting = self.userDB["Player"]["Skills"]["crafting"]["Level"]
        self.playerCurrentCrafting = int(self.playerMaxCrafting)
        # Fletching Stats and Modifiers
        self.playerMaxFletching = self.userDB["Player"]["Skills"]["fletching"]["Level"]
        self.playerCurrentFletching = int(self.playerMaxFletching)
        # Cooking Stats and Modifiers
        self.playerMaxCooking = self.userDB["Player"]["Skills"]["cooking"]["Level"]
        self.playerCurrentCooking = int(self.playerMaxCooking)

        # Default Player Equipment Stats
        self.playerEquipment = self.userDB["Player"]["Equipment"]
        self.playerAttackSpeed = 4
        self.playerMeleeAtk = 0
        self.playerMeleeStr = 0
        self.playerMeleeDef = 0
        self.playerRangeAtk = 0
        self.playerRangeStr = 0
        self.playerRangeDef = 0
        self.playerMageAtk = 0
        self.playerMageStr = 0
        self.playerMageDef = 0

        # Update equipment stats
        self.refComStatsFromEquips()

        # Flags for canceling out of activities or keeping users in one at a time.
        self.cancelBool = False
        self.inCombat = False
        self.isBusy = False

        # Player Inventory
        # The expected format of this is a simple dict of "items id":"item quantity"
        self.playerScrip = self.userDB["Player"]["Info"]["Currency"]
        self.playerInventory = self.userDB["Player"]["Inventory"]
        self.playerMaxInventory = self.userDB["Player"]["Info"]["inventorySize"]

        # Other player information
        self.playerDuelWins = self.userDB["Player"]["Info"]["Wins"]
        self.playerDuelLosses = self.userDB["Player"]["Info"]["Losses"]

        # Build player's farming plots from DB
        # This has to be down here because it relies on the inventory being init
        self.buildPlots()
        self.playerPets = []
        self.readPets()

    def readPets(self):
        for pet in self.userDB["Player"]["Pets"]:
            self.playerPets.append(pet)

    def getPets(self):
        return self.playerPets

    def addPet(self, petname):
        petname = petname.upper()
        if petname not in self.playerPets and petname in ['BUDCHEST', 'LIBCHEST', 'BITCHEST', 'CHUDCHEST',
                                                          'SPOOKYCHEST', 'DEBATCHEST',
                                                          'ELONCHEST', 'WEEBCHEST', 'TANKCHEST', 'COPCHEST']:
            self.playerPets.append(petname)
            u = self.bot.db.testuserdata.update_one({"Player.Info.DiscordID": self.DiscordID},
                                                    {"$set": {f'Player.Pets.{petname}': 1}})
            return f'Added {petname} to <@!{self.DiscordID}>.'
        else:
            return f'Something went wrong, either player already has that pet or pet name not recognized!'

    def changeAttackDelay(self, amount):
        self.playerAttackDelay += amount
        return self.playerAttackDelay

    def changeEatDelay(self, amount):
        self.playerEatDelay += amount
        return self.playerEatDelay

    def changeMaxInvt(self, amount: int):
        self.playerMaxInventory += amount
        self.bot.db.testuserdata.update_one({"Player.Info.DiscordID": self.DiscordID},
                                            {"$set": {f'Player.Info.inventorySize': self.playerMaxInventory}})
        return self.playerMaxInventory

    def changeSkillingRate(self, amount: float):
        self.skillingRate = amount
        self.bot.db.testuserdata.update_one({"Player.Info.DiscordID": self.DiscordID},
                                            {"$set": {f'Player.Modifiers.skillingRate': self.skillingRate}})
        return self.skillingRate

    def expandFarm(self):
        self.playerMaxFarmingPlots += 1
        self.bot.db.testuserdata.update_one({"Player.Info.DiscordID": self.DiscordID},
                                            {"$set": {f'Player.Info.maxplots': self.playerMaxFarmingPlots}})
        return self.playerMaxFarmingPlots

    def addFarmingPlot(self, plot):
        if len(self.farmingPlots) >= self.playerMaxFarmingPlots:
            return f'Player farming plots are already full!'
        seedID = plot.plotID
        if str(seedID) not in self.playerInventory.keys():
            return f'Player does not have that seed.'
        self.addToInventory(seedID, -1)
        if str(seedID) in self.userDB["Player"]["farm"]:
            currentPlots = self.userDB["Player"]["farm"][f'{seedID}']
            u = self.bot.db.testuserdata.update_one({"Player.Info.DiscordID": self.DiscordID},
                                                    {"$set": {f'Player.farm.{seedID}': currentPlots + 1}})
            print(f'If you can see this, {self.DiscordID} saved {u.modified_count} additional {plot.plotName} plot')
        else:
            u = self.bot.db.testuserdata.update_one({"Player.Info.DiscordID": self.DiscordID},
                                                    {"$set": {f'Player.farm.{seedID}': 1}})
            print(f'If you can see this, {self.DiscordID} saved {u.modified_count} new {plot.plotName} plot')
        self.farmingPlots.append(plot)
        self.refreshPlayerDB(self.DiscordID)
        return f'Planted new {plot.plotName} plot, come back to harvest in ~{plot.growTime * 30}s'

    def remFarmingPlot(self, plot):
        self.farmingPlots.remove(plot)
        if str(plot.plotID) in self.userDB["Player"]["farm"]:
            currentPlots = self.userDB["Player"]["farm"][f'{plot.plotID}']
            newPlots = currentPlots - 1
            u = self.bot.db.testuserdata.update_one({"Player.Info.DiscordID": self.DiscordID},
                                                    {"$set": {f'Player.farm.{plot.plotID}': newPlots}})
            if newPlots <= 0:
                nupD = self.bot.db.testuserdata.update_one({"Player.Info.DiscordID": self.DiscordID},
                                                           {"$unset": {f'Player.farm.{plot.plotID}': ""}})
        else:
            print(f'This user did not have that plot in their DB, if you can see this something is odd.')

    def buildPlots(self):
        for plotID in self.userDB["Player"]["farm"]:
            number = self.userDB["Player"]["farm"][f'{plotID}']
            for i in range(number):
                plot = farmFactory(int(plotID), self)
                self.farmingPlots.append(plot)

    def onDeath(self):
        self.cancelBool = True
        lostScrip = int(self.playerScrip / 3)
        self.playerScrip -= lostScrip
        self.playerCurrentHP = self.playerMaxHP
        print(f'{self.DiscordID} has died! Lost {lostScrip}')
        return lostScrip

    def calculateAttackOnEnemy(self, enemy):
        # This should leave room for special attacks
        # Special attacks will likely require several non-DB player variables.
        # player.specialAttackID to grab logic from within player object
        # player.specialAttackCD to put a limit on special attack repetition.
        # player.specialAttackChance to determine when a special attack happens.
        # An equipment stat can be caught to make the changes to variables necessary.
        # Each special attack is its own function within Player
        if self.playerCombatStyle in ['attack', 'strength', 'defence']:
            damage, text = self.playerMelee(enemy)
        elif self.playerCombatStyle == 'ranged':
            damage, text = self.playerRange(enemy)
        elif self.playerCombatStyle == 'magic':
            damage, text = self.playerMage(enemy)
        return damage, text

    def playerRange(self, enemy):
        ammoID = self.playerEquipment["ammo"]
        arrowIDs = [134, 135, 136, 137, 138, 139, 140]
        if str(ammoID) not in self.playerInventory or ammoID not in arrowIDs:  # This should actually check what ammo we have and make sure its arrows
            self.cancelBool = True
            return 0, f'<@!{self.DiscordID}> doesnt have enough arrows!'
        self.addToInventory(ammoID, -1)
        swingRoll = random.random()
        atkMRoll = (self.playerCurrentRanged + 11) * (self.playerRangeAtk + 64)
        defMRoll = (enemy.enemyMaxDefence + 9) * (enemy.enemyEquipRangeDef + 64)
        rangedStr = (self.playerCurrentRanged + 8)
        maxHit = int(round((rangedStr * (self.playerRangeStr + 64)) / 640) + 1)
        hitDamage = random.randint(0, maxHit)
        atkRoll = random.randint(1, atkMRoll)
        defRoll = random.randint(1, defMRoll)
        if atkRoll > defRoll:
            hitChance = 1 - ((defRoll + 2) / (2 * (atkRoll + 1)))
        else:
            hitChance = atkRoll / (2 * (defRoll + 1))
        if swingRoll < hitChance:
            return hitDamage, f'<@!{self.DiscordID}> shoots {enemy.enemyName} for {hitDamage}'
        else:
            return 0, f'<@!{self.DiscordID}> fires and misses!'

    def playerMage(self, enemy):
        ammoID = self.playerEquipment["ammo"]
        runeIDs = [207, 208, 209, 210, 211]
        if str(ammoID) not in self.playerInventory or ammoID not in runeIDs:  # This should actually check what ammo we have and make sure its runes
            self.cancelBool = True
            return f'<@!{self.DiscordID}> is out of runes!'
        self.addToInventory(ammoID, -1)
        swingRoll = random.random()
        atkMRoll = (self.playerCurrentMagic + 11) * (self.playerMageAtk + 64)
        defMRoll = (enemy.enemyMaxMagic + int(enemy.enemyMaxDefence / 5) + 9) * (enemy.enemyEquipMageDef + 64)
        mageStr = (self.playerCurrentMagic + 8)
        maxHit = int(round((mageStr * (self.playerMageStr + 64)) / 640) + 1)
        hitDamage = random.randint(0, maxHit)
        atkRoll = random.randint(1, atkMRoll)
        defRoll = random.randint(1, defMRoll)
        if atkRoll > defRoll:
            hitChance = 1 - ((defRoll + 2) / (2 * (atkRoll + 1)))
        else:
            hitChance = atkRoll / (2 * (defRoll + 1))
        if swingRoll < hitChance:
            return hitDamage, f'<@!{self.DiscordID}> blasts {enemy.enemyName} for {hitDamage}'
        else:
            return 0, f'<@!{self.DiscordID}> fails to hit with their spell!'

    def playerMelee(self, enemy):
        swingRoll = random.random()
        atkMRoll = (self.playerCurrentAttack + 11) * (self.playerMeleeAtk + 64)  # 768
        defMRoll = (enemy.enemyMaxDefence + 9) * (enemy.enemyEquipMeleeDef + 64)
        maxHit = int(round(((self.playerCurrentStrength * (self.playerMeleeStr + 64)) + 320) / 640))  #
        hitDamage = random.randint(0, maxHit)
        atkRoll = random.randint(1, atkMRoll)
        defRoll = random.randint(1, defMRoll)
        if atkRoll > defRoll:
            hitChance = 1 - ((defRoll + 2) / (2 * (atkRoll + 1)))
        else:
            hitChance = atkRoll / (2 * (defRoll + 1))
        if swingRoll < hitChance:
            return hitDamage, f'<@!{self.DiscordID}> swings and hits {enemy.enemyName} for {hitDamage}'
        else:
            return 0, f'<@!{self.DiscordID}> swings and misses!'

    def applyBuffDebuff(self, modifier: buffsdebuffs.Buff):
        if modifier not in self.buffs:
            self.buffs.append(modifier)
            # Put it in there
        else:
            pass

    def readBuffs(self):
        pBuffs = {}
        for buff in self.buffs:
            pBuffs[f'{buff.name}'] = f'{buff.duration}'
        return pBuffs

    def hitpointsDisplay(self):
        return int((self.playerCurrentHP) / (self.playerMaxHP) * 20)

    def getAttackSpeed(self):
        return self.playerAttackSpeed + self.playerAtkSpeedMod

    def getSkill(self, skill):
        self.refreshPlayerDB(self.DiscordID)
        skill = skill.lower()
        currentEXP = int(self.userDB["Player"]["Skills"][f'{skill}']["Experience"])
        currentLevel = int(self.userDB["Player"]["Skills"][f'{skill}']["Level"])
        currentNexLevel = int(self.userDB["Player"]["Skills"][f'{skill}']["nextLevel"])
        return currentEXP, currentLevel, currentNexLevel

    def levelFromXP(self, pxp):
        lv = 1
        for level, xp in self.bot.gameManager.expTable.items():
            if pxp >= xp:
                lv = int(level)
        if lv:
            return lv

    def buildLevelUpEmbed(self, skill, newLevel):
        embed = discord.Embed(title=f'',
                              description=f"**Congratulations, <@!{self.DiscordID}>, you just advanced a {skill.capitalize()} level! \n"
                                          f"Your {skill.capitalize()} level is now {newLevel}**", color=0xd25151)
        embed.set_thumbnail(url='https://media2.giphy.com/media/hqIaXesRGpP44/giphy.gif')
        return embed

    def givePlayerExperience(self, skill, amount):
        skill = skill.lower()
        currentEXP = int(self.userDB["Player"]["Skills"][f'{skill}']["Experience"])
        currentLevel = int(self.userDB["Player"]["Skills"][f'{skill}']["Level"])
        currentNexLevel = int(self.userDB["Player"]["Skills"][f'{skill}']["nextLevel"])
        xpGained = int(amount * self.playerXPRate)
        newExp = currentEXP + xpGained
        self.bot.db.testuserdata.update_one({"Player.Info.DiscordID": self.DiscordID},
                                            {"$set": {f'Player.Skills.{skill}.Experience': newExp}})
        embed = None
        if newExp >= currentNexLevel and currentLevel < 99:
            newLevel = self.levelFromXP(newExp)
            newNextExp = self.bot.gameManager.expTable[newLevel + 1]

            self.bot.db.testuserdata.update_one({"Player.Info.DiscordID": self.DiscordID},
                                                {"$set": {f'Player.Skills.{skill}.Level': newLevel}})
            self.bot.db.testuserdata.update_one({"Player.Info.DiscordID": self.DiscordID},
                                                {"$set": {f'Player.Skills.{skill}.nextLevel': newNextExp}})
            self.refreshPlayerDB(self.DiscordID)
            self.updatePlayerStatsFromDB()
            embed = self.buildLevelUpEmbed(skill, newLevel)
            print(f'{self.DiscordID} is now level {newLevel} {skill}!')
            return xpGained, embed  # User leveled up
        self.refreshPlayerDB(self.DiscordID)
        return xpGained, embed  # User did not level up

    def refreshPlayerDB(self, ID):
        self.userDB = self.bot.db.testuserdata.find_one({"Player.Info.DiscordID": ID})

    def updatePlayerStatsFromDB(self):
        self.playerMaxHP = self.userDB["Player"]["Skills"]["maxhp"]["Level"]
        self.playerMaxAttack = self.userDB["Player"]["Skills"]["attack"]["Level"]
        self.playerMaxStrength = self.userDB["Player"]["Skills"]["strength"]["Level"]
        self.playerMaxDefence = self.userDB["Player"]["Skills"]["defence"]["Level"]
        self.playerMaxMining = self.userDB["Player"]["Skills"]["mining"]["Level"]
        self.playerMaxFishing = self.userDB["Player"]["Skills"]["fishing"]["Level"]
        self.playerMaxFarming = self.userDB["Player"]["Skills"]["farming"]["Level"]
        self.playerMaxWoodcutting = self.userDB["Player"]["Skills"]["woodcutting"]["Level"]
        self.playerMaxSmithing = self.userDB["Player"]["Skills"]["smithing"]["Level"]
        self.playerMaxPrayer = self.userDB["Player"]["Skills"]["prayer"]["Level"]
        self.playerCurrentHP = int(self.playerMaxHP)
        self.playerCurrentAttack = int(self.playerMaxAttack)
        self.playerCurrentStrength = int(self.playerMaxStrength)
        self.playerCurrentDefence = int(self.playerMaxDefence)
        self.playerCurrentMining = int(self.playerMaxMining)
        self.playerCurrentFishing = int(self.playerMaxFishing)
        self.playerCurrentFarming = int(self.playerMaxFarming)
        self.playerCurrentWoodcutting = int(self.playerMaxWoodcutting)
        self.playerCurrentSmithing = int(self.playerMaxSmithing)
        self.playerCurrentPrayer = int(self.playerMaxPrayer)
        # Skills added after these
        self.playerMaxRanged = self.userDB["Player"]["Skills"]["ranged"]["Level"]
        self.playerCurrentRanged = self.playerMaxRanged
        self.playerMaxMagic = self.userDB["Player"]["Skills"]["magic"]["Level"]
        self.playerCurrentMagic = self.playerMaxMagic
        self.playerMaxCrafting = self.userDB["Player"]["Skills"]["crafting"]["Level"]
        self.playerCurrentCrafting = self.playerMaxCrafting
        self.playerMaxFletching = self.userDB["Player"]["Skills"]["fletching"]["Level"]
        self.playerCurrentFletching = self.playerMaxFletching
        self.playerMaxCooking = self.userDB["Player"]["Skills"]["cooking"]["Level"]
        self.playerCurrentCooking = int(self.playerMaxCooking)

    def overhealPlayer(self, value: int):
        self.playerCurrentHP = min((self.playerCurrentHP + int(value)), self.playerMaxHP + 22)

    def changePlayerHP(self, value: int):
        self.playerCurrentHP = min((self.playerCurrentHP + int(value)), self.playerMaxHP)

        if value < 0:
            # Value < 0 indicates the player is taking damage.
            # First thing up, are we dead?
            if self.playerCurrentHP <= 0:
                return ''
            if self.autoEatCheck():
                itemID = self.playerFood
                item = self.bot.gameManager.itemIDToItem(itemID)
                if item:
                    m = item.use(owner=self, target=self)
                    if m:
                        return m
                    return f'<@!{self.DiscordID}> eats some {item.itemName}, regaining {item.magnitude} HP!'
                else:
                    pass
            return ''

        return ''

    def autoEatCheck(self):
        return self.playerCurrentHP <= int(self.playerMaxHP / 3)

    def changeFood(self, itemID):
        self.playerFood = int(itemID)
        dbid = {"Player.Info.DiscordID": self.DiscordID}
        data = {"$set": {f'Player.Info.food': itemID}}
        upD = self.bot.db.testuserdata.update_one(dbid, data)
        if upD.modified_count > 0:
            print(f'Made {upD.modified_count} DB changes to {self.DiscordID} for changing food!')

    def addToInventory(self, itemid, count):
        item = self.bot.gameManager.itemIDToItem(itemid)
        if str(item.ID) in self.playerInventory:
            # Find that item in the DB, and update itemQuant += the itemQuant from our item parameter
            currentQuant = int(self.playerInventory[str(item.ID)])
            newAmt = currentQuant + count
            dbid = {"Player.Info.DiscordID": self.DiscordID}
            data = {"$set": {f'Player.Inventory.{item.ID}': newAmt}}
            upD = self.bot.db.testuserdata.update_one(dbid, data)
            if newAmt <= 0:
                nupD = self.bot.db.testuserdata.update_one({"Player.Info.DiscordID": self.DiscordID},
                                                           {"$unset": {f'Player.Inventory.{item.ID}': ""}})
                print(
                    f'Made {nupD.modified_count} changes to {self.DiscordID}, removed {item.itemName} because they had {newAmt}.')
            self.refreshPlayerDB(self.DiscordID)
            self.playerInventory = self.userDB["Player"]["Inventory"]
            return count, item.itemName

        else:
            if len(self.playerInventory) >= self.playerMaxInventory:
                print(f'Attempted to give {self.DiscordID} {count} {item.itemName}, but their inventory was full!')
                self.cancelBool = True
                count = -1
                return count, item.itemName

            # Add this item to Player Inventory
            urp = self.bot.db.testuserdata.update_one({"Player.Info.DiscordID": self.DiscordID},
                                                      {"$set": {f'Player.Inventory.{item.ID}': count}})
            print(f'Gave {self.DiscordID} {count} {item.itemName}, made {urp.modified_count} changes.')
            self.refreshPlayerDB(self.DiscordID)
            self.playerInventory = self.userDB["Player"]["Inventory"]
            return count, item.itemName

    def checkInventory(self, item):
        if str(item.ID) in self.playerInventory:
            return True
        else:
            return False

    def checkScrip(self):
        return self.playerScrip

    def changeScrip(self, amount):
        self.playerScrip += amount
        dbid = {"Player.Info.DiscordID": self.DiscordID}
        data = {"$set": {f'Player.Info.Currency': self.playerScrip}}
        upD = self.bot.db.testuserdata.update_one(dbid, data)
        print(f'Made {upD.modified_count} changes as part of giving {self.DiscordID} {amount} Scrip.')
        return self.playerScrip

    def checkStat(self, stat, number: int):
        self.refreshPlayerDB(self.DiscordID)
        if self.userDB["Player"]["Skills"][f'{stat.lower()}']["Level"] >= number:
            return True
        else:
            return False

    def refComStatsFromEquips(self):
        meleeAtk = 0
        meleeStr = 0
        meleeDef = 0
        rangeAtk = 0
        rangeStr = 0
        rangeDef = 0
        mageAtk = 0
        mageStr = 0
        mageDef = 0

        for slot in self.playerEquipment:
            item = self.bot.gameManager.itemIDToItem(self.playerEquipment[f'{slot}'])
            if item:
                if "style" in item.equipmentStats:
                    if item.equipmentStats["style"] == 'attack' and self.playerCombatStyle in ['attack', 'strength',
                                                                                               'defence']:
                        pass
                    self.playerCombatStyle = item.equipmentStats["style"]
                if "skillingRate" in item.equipmentStats:
                    self.changeSkillingRate(item.equipmentStats["skillingRate"])
                if "atkSpeed" in item.equipmentStats:
                    self.playerAttackSpeed = item.equipmentStats["atkSpeed"]
                if "meleeAtk" in item.equipmentStats:
                    meleeAtk += item.equipmentStats["meleeAtk"]
                if "meleeStr" in item.equipmentStats:
                    meleeStr += item.equipmentStats["meleeStr"]
                if "meleeDef" in item.equipmentStats:
                    meleeDef += item.equipmentStats["meleeDef"]
                if "rangeAtk" in item.equipmentStats:
                    rangeAtk += item.equipmentStats["rangeAtk"]
                if "rangeStr" in item.equipmentStats:
                    rangeStr += item.equipmentStats["rangeStr"]
                if "rangeDef" in item.equipmentStats:
                    rangeDef += item.equipmentStats["rangeDef"]
                if "mageAtk" in item.equipmentStats:
                    mageAtk += item.equipmentStats["mageAtk"]
                if "mageStr" in item.equipmentStats:
                    mageStr += item.equipmentStats["mageStr"]
                if "mageDef" in item.equipmentStats:
                    mageDef += item.equipmentStats["mageDef"]
        self.playerMeleeAtk = meleeAtk
        self.playerMeleeStr = meleeStr
        self.playerMeleeDef = meleeDef
        self.playerRangeAtk = rangeAtk
        self.playerRangeStr = rangeStr
        self.playerRangeDef = rangeDef
        self.playerMageAtk = mageAtk
        self.playerMageStr = mageStr
        self.playerMageDef = mageDef

    def saveEquips(self):
        for slot in self.playerEquipment:
            dbid = {"Player.Info.DiscordID": self.DiscordID}
            data = {"$set": {f'Player.Equipment.{slot}': self.playerEquipment[slot]}}
            upD = self.bot.db.testuserdata.update_one(dbid, data)
            if upD.modified_count > 0:
                print(f'Made {upD.modified_count} DB changes to {self.DiscordID} as part of saving equips.')

    def equipItem(self, item):
        if len(item.equipmentSlots) > 1 and len(self.playerInventory) >= self.playerMaxInventory-1:
            return f'Equipping this item would return 2 items to your inventory, and you do not have enough space for that!'

        if self.checkInventory(item):
            try:
                if item.equipmentStats:
                    if item.equipmentReqs:
                        for k, v in item.equipmentReqs.items():
                            if self.checkStat(k, v):
                                pass
                            else:
                                print(f'If you can see this, {self.DiscordID} does not have {v} {k}.')
                                return f'You do not have {v} {k}, you do not meet the requirements to equip this item.'
                    eslots = item.equipmentSlots
                    for slots in self.playerEquipment:
                        if slots in eslots:
                            if self.playerEquipment[f'{slots}'] != 0:
                                self.addToInventory(self.playerEquipment[f'{slots}'], 1)
                                self.playerEquipment[f'{slots}'] = 0
                            if slots == "ohand":
                                mhandID = self.playerEquipment["mhand"]
                                if mhandID != 0:
                                    mhandItem = self.bot.gameManager.itemIDToItem(mhandID)
                                    if len(mhandItem.equipmentSlots) > 1:
                                        self.addToInventory(self.playerEquipment["mhand"], 1)
                                        self.playerEquipment["mhand"] = 0

                    equipLoc = item.equipmentSlots[0]
                    for slots in self.playerEquipment:
                        if equipLoc == slots:
                            self.playerEquipment[f'{slots}'] = item.ID
                    self.addToInventory(item.ID, -1)
                    self.refComStatsFromEquips()
                    if self.playerEquipment['mhand'] == 0:
                        self.playerCombatStyle = 'attack'
                    self.saveEquips()
                    return f'<@!{self.DiscordID}> successfully equips {item.itemName}'
            except AttributeError:
                print(f'Bad item.')
        else:
            return f'Player does not have that item to equip!'

    def getSkills(self):
        # Returns a dictionary where keys are the name of a skill, and values are a string containing the
        # current skill level over the max skill level.
        return {
            "MaxHP": f'{self.playerCurrentHP} / {self.playerMaxHP}',
            "Attack": f'{self.playerCurrentAttack} / {self.playerMaxAttack}',
            "Strength": f'{self.playerCurrentStrength} / {self.playerMaxStrength}',
            "Defence": f'{self.playerCurrentDefence} / {self.playerMaxDefence}',
            "Ranged": f'{self.playerCurrentRanged} / {self.playerMaxRanged}',
            "Magic": f'{self.playerCurrentMagic} / {self.playerMaxMagic}',
            "Mining": f'{self.playerCurrentMining} / {self.playerMaxMining}',
            "Fishing": f'{self.playerCurrentFishing} / {self.playerMaxFishing}',
            "Woodcutting": f'{self.playerCurrentWoodcutting} / {self.playerMaxWoodcutting}',
            "Farming": f'{self.playerCurrentFarming} / {self.playerMaxFarming}',
            "Smithing": f'{self.playerCurrentSmithing} / {self.playerMaxSmithing}',
            "Prayer": f'{self.playerCurrentPrayer} / {self.playerMaxPrayer}',
            "Crafting": f'{self.playerCurrentCrafting} / {self.playerMaxCrafting}',
            "Fletching": f'{self.playerCurrentFletching} / {self.playerMaxFletching}',
            "Cooking": f'{self.playerCurrentCooking} / {self.playerMaxCooking}'
        }

    def checkCompost(self):
        if '111' in self.playerInventory:
            return True
        else:
            return False
