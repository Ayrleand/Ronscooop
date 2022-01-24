import random
import discord
import asyncio
from abc import abstractmethod, ABC
import buffsdebuffs


class Enemy:
    def __init__(self):
        self.enemyID = 0
        self.enemyName = ""
        self.enemyMaxHP = 1
        self.enemyCurrentHP = self.enemyMaxHP
        self.enemyMaxAttack = 1
        self.enemyMaxStrength = 1
        self.enemyMaxDefence = 1
        self.enemyMaxRange = 1
        self.enemyMaxMagic = 1
        self.enemyEquipMeleeAtk = 0
        self.enemyEquipRangeAtk = 0
        self.enemyEquipMageAtk = 0
        self.enemyEquipMeleeDef = 0
        self.enemyEquipRangeDef = 0
        self.enemyEquipMageDef = 0
        self.enemyMaxHit = 1
        self.buffs = []
        self.enemyDropTable = []
        self.enemyAlwaysDrop = (239, 1)
        self.enemyAtkSpeed = 4
        self.enemyImgURL = ""
        self.enemyAtkSpdMod = 0
        self.numDrops = 1
        self.enemyDesc = "\u200b"

    @abstractmethod
    def readBuffs(self):
        eBuffs = {}
        for buff in self.buffs:
            eBuffs[f'{buff.name}'] = f'{buff.duration}'
        return eBuffs

    @abstractmethod
    def changeEnemyHP(self, amount):
        self.enemyCurrentHP += amount

    @abstractmethod
    def applyBuffDebuff(self, modifier: buffsdebuffs.Buff):
        if modifier not in self.buffs:
            self.buffs.append(modifier)
            # Put it in there
        else:
            print(f'Found that buff in your buffs already!')

    @abstractmethod
    def hitpointsDisplay(self):
        return int((self.enemyCurrentHP) / (self.enemyMaxHP) * 20)

    @abstractmethod
    def getEnemyAtkSpeed(self):
        return self.enemyAtkSpeed + self.enemyAtkSpdMod

    @abstractmethod
    def handleLoot(self, player):
        embed = discord.Embed(title=f'Loot from {self.enemyName}',
                              description=f"<@!{player.DiscordID}>", color=0xd25151)
        embed.set_thumbnail(url=self.enemyImgURL)
        dropID, count = self.enemyAlwaysDrop
        count = random.randint(1, count)
        c, i = player.addToInventory(dropID, count)
        if c < 0:
            embed.add_field(name=f'{i}', value=f'Player inventory full!', inline=True)
        else:
            print(f'{player.DiscordID} gains {c} {i} from killing {self.enemyName}.')
            embed.add_field(name=f'{i}', value=f'{c}', inline=True)

        ID, count = random.choices(self.enemyDropTable, cum_weights=(50, 83, 99, 100), k=1)[0]
        count = random.randint(1, count)
        c, v = player.addToInventory(ID, count)
        if c < 0:
            embed.add_field(name=f'{v}', value=f'Player inventory full!', inline=True)
        else:
            print(f'{player.DiscordID} gains {c} {v} from killing {self.enemyName}.')
            embed.add_field(name=f'{v}', value=f'{c}', inline=True)
        return embed


    @abstractmethod
    # This can be overwritten for various effects, but should return something usable.
    def calculateAttackOnPlayer(self, player):
        dmg, text = self.meleeAttack(player)
        return dmg, text

    @abstractmethod
    def meleeAttack(self, player):
        swingRoll = random.random()
        atkMRoll = (self.enemyMaxAttack + 8) * (self.enemyEquipMeleeAtk + 64)
        defMRoll = (player.playerCurrentDefence + 11) * (player.playerMeleeDef + 64)
        maxHit = self.enemyMaxHit
        hitDamage = random.randint(0, maxHit)
        atkRoll = random.randint(1, atkMRoll)
        defRoll = random.randint(1, defMRoll)
        if atkRoll > defRoll:
            hitChance = 1 - ((defRoll + 2) / (2 * (atkRoll + 1)))
        else:
            hitChance = atkRoll / (2 * (defRoll + 1))
        if swingRoll < hitChance:
            return hitDamage, f'{self.enemyName} hits <@!{player.DiscordID}> for {hitDamage}!'
        else:
            return 0, f'{self.enemyName} swings and misses!'

    @abstractmethod
    def mageAttack(self, player):
        swingRoll = random.random()
        atkMRoll = (self.enemyMaxMagic + 11) * (self.enemyEquipMageAtk + 64)
        defMRoll = (player.playerCurrentMagic) * (player.playerMageDef + 64)
        mageStr = (self.enemyMaxMagic + 8)
        maxHit = self.enemyMaxHit
        hitDamage = random.randint(0, maxHit)
        atkRoll = random.randint(1, atkMRoll)
        try:
            defRoll = random.randint(1, defMRoll)
        except ValueError:
            defRoll = 1

        if atkRoll > defRoll:
            hitChance = 1 - ((defRoll + 2) / (2 * (atkRoll + 1)))
        else:
            hitChance = atkRoll / (2 * (defRoll + 1))
        if swingRoll < hitChance:
            return hitDamage, f'{self.enemyName} blasts <@!{player.DiscordID}> for {hitDamage}'
        else:
            return 0, f'{self.enemyName} fizzles their spell!'

    @abstractmethod
    def rangeAttack(self, player):
        swingRoll = random.random()
        atkMRoll = (self.enemyMaxRange + 11) * (self.enemyEquipRangeAtk + 64)
        defMRoll = (player.playerCurrentDefence) * (player.playerRangeDef + 64)
        rangedStr = (self.enemyMaxRange + 8)
        maxHit = self.enemyMaxHit
        hitDamage = random.randint(0, maxHit)
        atkRoll = random.randint(1, atkMRoll)
        defRoll = random.randint(1, defMRoll)
        if atkRoll > defRoll:
            hitChance = 1 - ((defRoll + 2) / (2 * (atkRoll + 1)))
        else:
            hitChance = atkRoll / (2 * (defRoll + 1))
        if swingRoll < hitChance:
            return hitDamage, f'{self.enemyName} shoots <@!{player.DiscordID}> for {hitDamage}'
        else:
            return 0, f'{self.enemyName} fires and misses!'


def enemyFactory(ID):
    # ENEMY CLASS DEFINITIONS
    class Plant(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 1
            self.enemyName = 'Plant'
            self.enemyMaxHP = 2
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(104, 3), (96, 5), (104, 5), (104, 20)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Plant_built.png/250px-Plant_built.png?919de'
            self.enemyDesc = 'Its a potato plant.'
            self.enemyEquipMeleeAtk = -47
            self.enemyEquipMeleeDef = -42
            self.enemyEquipRangeDef = -42
            self.enemyEquipMageDef = -42

    class Bandit(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 2
            self.enemyName = 'Bandit'
            self.enemyMaxHP = 5
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyEquipMeleeAtk = 10
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(149, 15), (126, 3), (16, 10), (18, 10)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Bandit.png/160px-Bandit.png?4ee9f'
            self.enemyDesc = 'In America.'

    class BuffRat(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 3
            self.enemyName = 'Buff Rat'
            self.enemyMaxHP = 10
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(215, 1), (39, 1), (40, 1), (41, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Giant_rat.png/250px-Giant_rat.png?9bf29'
            self.enemyDesc = 'He sure can buff.'

        def calculateAttackOnPlayer(self, player):
            choices = [0, 1]
            choice = random.choices(choices, cum_weights=(10, 90), k=1)[0]
            if choice == 0:
                dmg = 0
                buff = buffsdebuffs.buffFactory(1, self)
                self.applyBuffDebuff(buff)
                text = f'{self.enemyName} speeds up!'
                return dmg, text
            else:
                dmg, text = self.meleeAttack(player)
                return dmg, text

    class Cow(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 4
            self.enemyName = 'Cow'
            self.enemyMaxHP = 5
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(150, 1), (150, 2), (239, 5), (150, 10)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Cow_%28Zanaris%29.png/200px-Cow_%28Zanaris%29.png?c5f91'
            self.enemyDesc = 'Converts grass to beef.'
            self.enemyEquipMeleeAtk = -15
            self.enemyEquipMeleeDef = -21
            self.enemyEquipRangeDef = -21
            self.enemyEquipMageDef = -21

    class Goblin(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 5
            self.enemyName = 'Goblin'
            self.enemyMaxHP = 5
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(141, 15), (16, 5), (207, 5), (42, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Goblin.png/150px-Goblin.png?3e49a'
            self.enemyDesc = 'Orange or blue?'
            self.enemyEquipMeleeAtk = -10
            self.enemyEquipMeleeDef = -15
            self.enemyEquipRangeDef = -15
            self.enemyEquipMageDef = -15

    class GoblinMiner(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 6
            self.enemyName = 'Goblin Miner'
            self.enemyMaxHP = 5
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(17, 5), (16, 8), (18, 5), (18, 10)]
            self.enemyImgURL = 'https://runescape.wiki/images/thumb/Cave_goblin_miner.png/150px-Cave_goblin_miner.png?dfd1e'
            self.enemyDesc = 'The kind that mines.'
            self.enemyEquipMeleeAtk = -10
            self.enemyEquipMeleeDef = -10
            self.enemyEquipRangeDef = -10
            self.enemyEquipMageDef = -10

    class Chicken(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 7
            self.enemyName = 'Chicken'
            self.enemyMaxHP = 3
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(125, 25), (125, 35), (125, 50), (125, 100)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Chicken_%281%29.png/800px-Chicken_%281%29.png?a7258'
            self.enemyDesc = 'Cluck cluck,'
            self.enemyEquipMeleeAtk = -47
            self.enemyEquipMeleeDef = -42
            self.enemyEquipRangeDef = -42
            self.enemyEquipMageDef = -42

    class Farmer(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 8
            self.enemyName = 'Farmer'
            self.enemyMaxHP = 10
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(96, 5), (97, 3), (98, 1), (111, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Farmer.png/150px-Farmer.png?1e65e'
            self.enemyDesc = 'KKoner'
            self.enemyEquipMeleeAtk = 5
            self.enemyMaxAttack = 3
            self.enemyMaxHit = 2
            self.enemyMaxDefence = 8
            self.enemyAtkSpeed = 6

    class BigFarmer(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 9
            self.enemyName = 'Big Farmer'
            self.enemyMaxHP = 20
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(99, 5), (100, 3), (111, 1), (101, 3)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Farmer.png/150px-Farmer.png?1e65e'
            self.enemyDesc = 'Bigger and tougher.'
            self.enemyEquipMeleeAtk = 10
            self.enemyMaxAttack = 8
            self.enemyMaxHit = 3
            self.enemyMaxDefence = 8
            self.enemyAtkSpeed = 6

    class MasterFarmer(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 10
            self.enemyName = 'Master Farmer'
            self.enemyMaxHP = 30
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(101, 5), (102, 3), (111, 1), (103, 3)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Master_Farmer.png/130px-Master_Farmer.png?c21af'
            self.enemyDesc = 'Absolutely tired of people stealing from him.'
            self.enemyEquipMeleeAtk = 45
            self.enemyMaxAttack = 45
            self.enemyMaxHit = 6
            self.enemyMaxDefence = 45
            self.enemyAtkSpeed = 6

    class Skelington(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 11
            self.enemyName = 'Skelington'
            self.enemyMaxHP = 24
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(48, 1), (142, 15), (54, 1), (28, 10)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Skeleton_%282%29.png/90px-Skeleton_%282%29.png?78571'
            self.enemyDesc = 'Spooky scary.'
            self.enemyEquipMeleeAtk = 5
            self.enemyMaxAttack = 17
            self.enemyMaxHit = 4
            self.enemyMaxDefence = 17

    class Zombo(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 12
            self.enemyName = 'Zombo'
            self.enemyMaxHP = 22
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(47, 1), (93, 3), (55, 1), (28, 10)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Zombie_%28Level_13%29.png/150px-Zombie_%28Level_13%29.png?d5c22'
            self.enemyDesc = 'Animated undead. No, like he is moving. Oh, nevermind.'
            self.enemyEquipMeleeAtk = 5
            self.enemyMaxAttack = 8
            self.enemyMaxHit = 3
            self.enemyMaxDefence = 10

    class SpookyGhost(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 13
            self.enemyName = 'Spooky Ghost'
            self.enemyMaxHP = 25
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(92, 3), (94, 3), (61, 1), (207, 10)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Ghost.png/100px-Ghost.png?997b9'
            self.enemyDesc = 'OooooOOOOoooo'
            self.enemyEquipMeleeAtk = 5
            self.enemyMaxAttack = 13
            self.enemyMaxHit = 3
            self.enemyMaxDefence = 18
            self.enemyEquipMageDef = -5

    class Crab(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 14
            self.enemyName = 'Crab'
            self.enemyMaxHP = 18
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(43, 1), (229, 1), (112, 1), (251, 30)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Crab.png/220px-Crab.png?e81ce'
            self.enemyDesc = 'Crab.'
            self.enemyMaxAttack = 17
            self.enemyMaxHit = 3
            self.enemyMaxDefence = 22

    class BigCrab(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 15
            self.enemyName = 'Big Crab'
            self.enemyMaxHP = 40
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(50, 1), (99, 5), (113, 1), (14, 30)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Rock_crab_%28exposed%29.png/200px-Rock_crab_%28exposed%29.png?7d2f4'
            self.enemyDesc = 'Like the crab, but bigger.'
            self.enemyMaxAttack = 17
            self.enemyMaxHit = 5
            self.enemyMaxDefence = 22

    class GiantEnemyCrab(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 16
            self.enemyName = 'Giant Enemy Crab'
            self.enemyMaxHP = 200
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(95, 5), (251, 30), (14, 200), (119, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/King_Sand_Crab.png/250px-King_Sand_Crab.png?97237'
            self.enemyDesc = 'Based on a famous battle that took place in ancient Japan.'
            self.enemyMaxAttack = 50
            self.enemyMaxHit = 8
            self.enemyMaxDefence = 100


    class HillGiant(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 17
            self.enemyName = 'Hill Giant'
            self.enemyMaxHP = 35
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(135, 30), (97, 5), (111, 1), (208, 10)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Hill_Giant.png/150px-Hill_Giant.png?d162a'
            self.enemyDesc = 'No safespots here, human.'
            self.enemyMaxAttack = 18
            self.enemyMaxHit = 4
            self.enemyMaxDefence = 26
            self.enemyEquipMeleeAtk = 18
            self.enemyEquipMeleeStr = 16
            self.enemyAtkSpeed = 6

    class MossGiant(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 18
            self.enemyName = 'Moss Giant'
            self.enemyMaxHP = 60
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (240, 1)
            self.enemyDropTable = [(102, 5), (103, 5), (208, 10), (115, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Moss_giant_%28level_42%2C_2%29.png/72px-Moss_giant_%28level_42%2C_2%29.png?9e3bc'
            self.enemyDesc = 'That beard seems to have a life of its own.'
            self.enemyMaxAttack = 30
            self.enemyMaxHit = 5
            self.enemyMaxDefence = 30
            self.enemyEquipMeleeAtk = 33
            self.enemyEquipMeleeStr = 31
            self.enemyAtkSpeed = 6

    class Squire(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 19
            self.enemyName = 'Squire'
            self.enemyMaxHP = 42
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(27, 3), (19, 3), (258, 1), (181, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Squire.png/120px-Squire.png?e4d3a'
            self.enemyDesc = 'A knight hopeful.'
            self.enemyMaxAttack = 25
            self.enemyMaxHit = 4
            self.enemyMaxDefence = 26
            self.enemyEquipMeleeAtk = 18
            self.enemyEquipMeleeStr = 16
            self.enemyEquipMeleeDef = 75
            self.enemyEquipMageDef = -11
            self.enemyEquipRangeDef = 72
            self.enemyAtkSpeed = 5

    class RangedGoblin(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 20
            self.enemyName = 'Ranged Goblin'
            self.enemyMaxHP = 10
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(134, 5), (96, 5), (218, 1), (128, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Goblin_%28level_12%2C_banner%29.png/114px-Goblin_%28level_12%2C_banner%29.png?2f44f'
            self.enemyDesc = 'A goblin that has managed to find a ranged weapon.'
            self.enemyMaxRange = 5
            self.enemyMaxDefence = 5
            self.enemyMaxHit = 2

        def calculateAttackOnPlayer(self, player):
            dmg, text = self.rangeAttack(player)
            return dmg, text

    class SteelKnight(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 21
            self.enemyName = 'Steel Knight'
            self.enemyMaxHP = 15
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(53, 2), (52, 2), (54, 2), (55, 5)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/White_Knight.png/120px-White_Knight.png?8b8e4'
            self.enemyDesc = 'Shining white, ready to save.'
            self.enemyMaxDefence = 10
            self.enemyMaxAttack = 10
            self.enemyMaxHit = 3

    class Tentacle(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 22
            self.enemyName = 'Tentacle'
            self.enemyMaxHP = 25
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(18, 5), (227, 1), (11, 5), (19, 10)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Tentacle_%28Temple_Trekking%29.png/130px-Tentacle_%28Temple_Trekking%29.png?ac1f3'
            self.enemyDesc = 'It is probably best that we cant see the rest of it.'
            self.enemyMaxDefence = 5
            self.enemyMaxAttack = 10
            self.enemyEquipMeleeAtk = 5
            self.enemyMaxHit = 3

    class RiverTroll(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 23
            self.enemyName = 'River Troll'
            self.enemyMaxHP = 15
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(26, 3), (27, 3), (230, 1), (112, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/River_troll.png/200px-River_troll.png?4db1d'
            self.enemyDesc = 'A particularly ugly form of troll.'
            self.enemyMaxDefence = 15
            self.enemyMaxAttack = 15
            self.enemyMaxHit = 3

    class Entrepeneur(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 24
            self.enemyName = 'Entrepeneur'
            self.enemyMaxHP = 20
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(126, 30), (126, 50), (126, 75), (239, 100)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Highwayman.png/150px-Highwayman.png?fa329'
            self.enemyDesc = 'Exploits new players by underpaying them for their labor.'
            self.enemyMaxDefence = 10
            self.enemyMaxAttack = 20
            self.enemyMaxHit = 4

    class Bat(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 25
            self.enemyName = 'Bat'
            self.enemyMaxHP = 10
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(239, 3), (42, 1), (86, 1), (50, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/Tz-Kih.png?31e87'
            self.enemyDesc = 'Wait, is it on fire?'
            self.enemyMaxDefence = 15
            self.enemyMaxAttack = 20
            self.enemyMaxHit = 5

    class BlackKnight(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 26
            self.enemyName = 'Black Knight'
            self.enemyMaxHP = 20
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(19, 5), (18, 10), (55, 1), (51, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Black_Knight.png/150px-Black_Knight.png?822e1'
            self.enemyDesc = 'A knight in full dark armor.'
            self.enemyMaxDefence = 20
            self.enemyMaxAttack = 20
            self.enemyEquipMeleeAtk = 10
            self.enemyMaxHit = 4

    class FrozenArcher(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 27
            self.enemyName = 'Frozen Archer'
            self.enemyMaxHP = 30
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(136, 15), (149, 50), (221, 1), (239, 5)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Ice_giant.png/271px-Ice_giant.png?20915'
            self.enemyDesc = 'A being of pure frozen ice, wielding a bow.'
            self.enemyMaxDefence = 1
            self.enemyMaxRange = 40
            self.enemyEquipRangeAtk = 10
            self.enemyMaxHit = 7

        def calculateAttackOnPlayer(self, player):
            dmg, text = self.rangeAttack(player)
            return dmg, text

    class Terrorbird(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 28
            self.enemyName = 'Terrorbird'
            self.enemyMaxHP = 28
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(13, 3), (20, 1), (5, 3), (125, 50)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Terrorbird.png/260px-Terrorbird.png?74e5c'
            self.enemyDesc = 'Vicious looking thing, could probably win wars with enough of them.'
            self.enemyMaxDefence = 24
            self.enemyMaxAttack = 22
            self.enemyMaxHit = 4
            self.enemyMaxMagic = 20

    class Mummy(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 29
            self.enemyName = 'Mummy'
            self.enemyMaxHP = 27
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(97, 5), (99, 5), (30, 3), (120, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Mummy_%28level_84%2C_4%29.png/70px-Mummy_%28level_84%2C_4%29.png?3b5dc'
            self.enemyDesc = 'A long undead being, now risen to exact vengeance. On whom? Who knows. '
            self.enemyMaxDefence = 27
            self.enemyMaxAttack = 22
            self.enemyMaxHit = 5

    class DarkWizard(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 30
            self.enemyName = 'Dark Wizard'
            self.enemyMaxHP = 30
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(207, 5), (228, 1), (207, 10), (208, 5)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Dark_wizard.png/120px-Dark_wizard.png?027c3'
            self.enemyDesc = 'A novice wizard, has fun picking on new players trying to get around.'
            self.enemyMaxDefence = 20
            self.enemyMaxMagic = 40
            self.enemyEquipMageAtk = 20
            self.enemyMaxHit = 11

        def calculateAttackOnPlayer(self, player):
            dmg, text = self.mageAttack(player)
            return dmg, text

    class MithrilKnight(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 31
            self.enemyName = 'Mithril Knight'
            self.enemyMaxHP = 25
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(60, 2), (59, 2), (61, 2), (62, 2)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Mithril_armour_set_%28lg%29_equipped.png/130px-Mithril_armour_set_%28lg%29_equipped.png?ae850'
            self.enemyDesc = 'A knight in mithril armor.'
            self.enemyMaxDefence = 30
            self.enemyMaxAttack = 30
            self.enemyEquipMeleeAtk = 10
            self.enemyMaxHit = 5
            self.enemyMaxMagic = 10

    class Pirate(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 32
            self.enemyName = 'Pirate'
            self.enemyMaxHP = 40
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(49, 1), (56, 1), (239, 5), (63, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Pirate_%28Port_Sarim%29.png/120px-Pirate_%28Port_Sarim%29.png?31918'
            self.enemyDesc = 'A green pirate. Well he looks kinda tan, but he is also green.'
            self.enemyMaxDefence = 20
            self.enemyMaxAttack = 40
            self.enemyEquipMeleeAtk = 30
            self.enemyMaxHit = 4

    class Bear(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 33
            self.enemyName = 'Bear'
            self.enemyMaxHP = 30
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(13, 3), (99, 5), (91, 3), (259, 10)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Grizzly_bear_cub_%28level_36%29.png/260px-Grizzly_bear_cub_%28level_36%29.png?805b8'
            self.enemyDesc = 'Caution: Is currently bearing arms.'
            self.enemyMaxDefence = 30
            self.enemyMaxAttack = 30
            self.enemyEquipMeleeAtk = 33
            self.enemyMaxHit = 7

    class BigZombo(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 34
            self.enemyName = 'Big Zombo'
            self.enemyMaxHP = 30
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(48, 2), (55, 2), (99, 5), (239, 5)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Zombie_%28Level_56%29.png/150px-Zombie_%28Level_56%29.png?9fe6f'
            self.enemyDesc = 'A much larger than average zombie... somehow.'
            self.enemyMaxDefence = 30
            self.enemyMaxAttack = 30
            self.enemyMaxHit = 5

    class GreenRiverTroll(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 35
            self.enemyName = 'Green River Troll'
            self.enemyMaxHP = 35
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(28, 3), (50, 2), (31, 3), (57, 2)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Sea_troll_%28lv_87%29.png/150px-Sea_troll_%28lv_87%29.png?26e4d'
            self.enemyDesc = 'Tougher, meaner, still exceptionally ugly.'
            self.enemyMaxDefence = 35
            self.enemyMaxAttack = 35
            self.enemyEquipMeleeAtk = 20
            self.enemyMaxHit = 4

    class MommaChicken(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 36
            self.enemyName = 'Momma Chicken'
            self.enemyMaxHP = 50
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(125, 100), (125, 150), (125, 200), (239, 30)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Sea_troll_%28lv_87%29.png/150px-Sea_troll_%28lv_87%29.png?26e4d'
            self.enemyDesc = 'Tougher, meaner, still exceptionally ugly.'
            self.enemyMaxDefence = 30
            self.enemyMaxAttack = 30
            self.enemyMaxHit = 5

    class Defiler(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 37
            self.enemyName = 'Defiler'
            self.enemyMaxHP = 37
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(136, 30), (233, 1), (136, 50), (129, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/Defiler_%28Level_33%29.png?bdc9b'
            self.enemyDesc = 'A strange, twisted monster of unknown origins.'
            self.enemyMaxDefence = 37
            self.enemyMaxMagic = 15
            self.enemyMaxRange = 50
            self.enemyEquipRangeAtk = 30
            self.enemyMaxHit = 9

        def calculateAttackOnPlayer(self, player):
            dmg, text = self.rangeAttack(player)
            return dmg, text

    class Zombom(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 38
            self.enemyName = 'Zombom'
            self.enemyMaxHP = 50
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(207, 30), (207, 50), (218, 1), (243, 1)]
            self.enemyImgURL = 'https://static.wikia.nocookie.net/neoquest/images/f/fc/Zombom.gif/revision/latest/scale-to-width-down/200?cb=20100409011439'
            self.enemyDesc = 'Oh no, not again.'
            self.enemyMaxDefence = 40
            self.enemyMaxMagic = 50
            self.enemyMaxHit = 17

        def calculateAttackOnPlayer(self, player):
            choices = [0, 1]
            choice = random.choices(choices, cum_weights=(10, 90), k=1)[0]
            if choice == 0:
                dmg = 0
                buff = buffsdebuffs.buffFactory(1, self)
                self.applyBuffDebuff(buff)
                text = f'{self.enemyName} speeds up!'
                return dmg, text
            else:
                dmg, text = self.mageAttack(player)
                return dmg, text

    class Sandraker(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 39
            self.enemyName = 'Sandraker'
            self.enemyMaxHP = 40
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(136, 30), (137, 15), (224, 1), (193, 1)]
            self.enemyImgURL = 'https://michaeljohnladera.files.wordpress.com/2013/03/diamond-sword-soldier.png'
            self.enemyDesc = '[VGTG] I am the greatest!'
            self.enemyMaxDefence = 20
            self.enemyMaxRange = 60
            self.enemyMaxMagic = 10
            self.enemyEquipRangeAtk = 30
            self.enemyMaxHit = 8

        def calculateAttackOnPlayer(self, player):
            choices = [0, 1]
            choice = random.choices(choices, cum_weights=(25, 100), k=1)[0]
            if choice == 0:
                return 10, f'{self.enemyName} dings <@!{player.DiscordID}> for 10 with a Blue Plate Special!'
            else:
                dmg, text = self.rangeAttack(player)
                return dmg, text

    class BigBat(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 40
            self.enemyName = 'Big Bat'
            self.enemyMaxHP = 20
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(239, 5), (49, 1), (86, 1), (57, 2)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Giant_bat_%28Brine_Rat_Cavern%29.png/250px-Giant_bat_%28Brine_Rat_Cavern%29.png?7d5e4'
            self.enemyDesc = 'At least its not on fire!'
            self.enemyMaxDefence = 30
            self.enemyMaxAttack = 40
            self.enemyMaxHit = 8

    class Brawler(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 41
            self.enemyName = 'Brawler'
            self.enemyMaxHP = 54
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(30, 3), (98, 3), (216, 1), (119, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/Brawler_%28level_51%29.png?d0fae'
            self.enemyDesc = 'An absolute unit.'
            self.enemyMaxDefence = 42
            self.enemyMaxAttack = 42
            self.enemyEquipMeleeAtk = 30
            self.enemyMaxHit = 6

    class Spider(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 42
            self.enemyName = 'Spider'
            self.enemyMaxHP = 25
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(98, 5), (239, 5), (92, 3), (93, 3)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Spider_%28Morytania%29.png/200px-Spider_%28Morytania%29.png?d7b58'
            self.enemyDesc = 'Theres some kind of rule somewhere that every game needs a spider enemy.'
            self.enemyMaxDefence = 50
            self.enemyMaxAttack = 50
            self.enemyMaxHit = 7

        def calculateAttackOnPlayer(self, player):
            choices = [0, 1]
            choice = random.choices(choices, cum_weights=(40, 100), k=1)[0]
            if choice == 0:
                dmg = random.randint(1,self.enemyMaxHit)
                buff = buffsdebuffs.buffFactory(3, player)
                player.applyBuffDebuff(buff)
                text = f'{self.enemyName} bites <@!{player.DiscordID}> for {dmg}, applying a slight poison!'
                return dmg, text
            else:
                dmg, text = self.meleeAttack(player)
                return dmg, text

    class Mushroom(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 43
            self.enemyName = 'Mushroom'
            self.enemyMaxHP = 40
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(31, 5), (22, 5), (20, 5), (197, 1)]
            self.enemyImgURL = 'https://i.pinimg.com/originals/3d/3e/54/3d3e5430e68ec00727f5f2f89d71d668.gif'
            self.enemyDesc = 'Do not be fooled by their adorable appearance.'
            self.enemyMaxDefence = 55
            self.enemyMaxAttack = 45
            self.enemyMaxHit = 18
            self.enemyEquipMeleeAtk = 30

    class Vampire(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 44
            self.enemyName = 'Vampire'
            self.enemyMaxHP = 50
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(137, 30), (232, 1), (94, 3), (130, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Vampyre_Juvinate_%28Meiyerditch%2C_female%29.png/100px-Vampyre_Juvinate_%28Meiyerditch%2C_female%29.png?a21cc'
            self.enemyDesc = 'Pale, ghastly, and not to be invited indoors.'
            self.enemyMaxDefence = 40
            self.enemyMaxRange = 70
            self.enemyMaxHit = 10
            self.enemyEquipRangeAtk = 10

        def calculateAttackOnPlayer(self, player):
            dmg, text = self.rangeAttack(player)
            return dmg, text

    class GreatWizard(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 45
            self.enemyName = 'Great Wizard'
            self.enemyMaxHP = 60
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 2)
            self.enemyDropTable = [(207, 30), (208, 30), (231, 1), (193, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Infernal_Mage.png/150px-Infernal_Mage.png?f3e68'
            self.enemyDesc = 'Honestly just looks like an okay wizard to me, but alright.'
            self.enemyMaxDefence = 20
            self.enemyMaxMagic = 75
            self.enemyMaxHit = 16
            self.enemyEquipMageAtk = 30

        def calculateAttackOnPlayer(self, player):
            dmg, text = self.mageAttack(player)
            return dmg, text

    class StrangeExperiment(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 46
            self.enemyName = 'Strange Experiment'
            self.enemyMaxHP = 55
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 2)
            self.enemyDropTable = [(19, 10), (60, 1), (21, 5), (74, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Experiment_%28level_25%29.png/110px-Experiment_%28level_25%29.png?ad1f8'
            self.enemyDesc = 'Absolutely horrifying... who made this?'
            self.enemyMaxDefence = 55
            self.enemyMaxAttack = 30
            self.enemyMaxHit = 8
            self.enemyEquipMeleeAtk = 40

    class FrozenMammoth(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 47
            self.enemyName = 'Frozen Mammoth'
            self.enemyMaxHP = 70
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 2)
            self.enemyDropTable = [(99, 5), (100, 5), (219, 1), (94, 5)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Mammoth.png/230px-Mammoth.png?956ac'
            self.enemyDesc = 'A massive, elephantine monster.'
            self.enemyMaxDefence = 60
            self.enemyMaxAttack = 20
            self.enemyMaxHit = 14
            self.enemyEquipMeleeAtk = 20
            self.enemyAtkSpeed = 5

        def calculateAttackOnPlayer(self, player):
            choices = [0, 1]
            choice = random.choices(choices, cum_weights=(30, 100), k=1)[0]
            if choice == 0:
                dmg = random.randint(1,self.enemyMaxHit)
                buff = buffsdebuffs.buffFactory(4, player)
                player.applyBuffDebuff(buff)
                text = f'{self.enemyName} smashes <@!{player.DiscordID}> for {dmg}, chilling them!'
                return dmg, text
            else:
                dmg, text = self.meleeAttack(player)
                return dmg, text

    class Warwelf(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 48
            self.enemyName = 'Warwelf'
            self.enemyMaxHP = 48
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 2)
            self.enemyDropTable = [(155, 5), (100, 5), (239, 10), (248, 100)]
            self.enemyImgURL = 'https://kol.coldfront.net/thekolwiki/images/6/66/Werewolf.gif'
            self.enemyDesc = 'Careful or he will chew the dickens out of you, and you would sure miss that dickens.'
            self.enemyMaxDefence = 48
            self.enemyMaxAttack = 58
            self.enemyMaxHit = 7

        def calculateAttackOnPlayer(self, player):
            choices = [0, 1]
            choice = random.choices(choices, cum_weights=(50, 100), k=1)[0]
            if choice == 0:
                dmg, text = self.meleeAttack(player)
                text = f'Warwelf gnaws on <@!{player.DiscordID}> for {dmg}! My, warwelf, what big teeth you is having.'
                return dmg, text
            else:
                dmg, text = self.meleeAttack(player)
                text = f'Warwelf lycanthropes <@!{player.DiscordID}> square in the chest for {dmg}!'
                return dmg, text

    class Durid(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 49
            self.enemyName = 'Durid'
            self.enemyMaxHP = 35
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 2)
            self.enemyDropTable = [(208, 30), (208, 50), (234, 1), (113, 3)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Druid.png/150px-Druid.png?37de2'
            self.enemyDesc = 'Cat durid is for fite.'
            self.enemyMaxDefence = 55
            self.enemyMaxMagic = 85
            self.enemyMaxHit = 8
            self.enemyEquipMageAtk = 5

        def calculateAttackOnPlayer(self, player):
            dmg, text = self.mageAttack(player)
            return dmg, text

    class FirstMate(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 50
            self.enemyName = 'First Mate'
            self.enemyMaxHP = 50
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 2)
            self.enemyDropTable = [(56, 3), (63, 3), (239, 10), (70, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Pirate_%28Asgarnian_Ice_Dungeon%29.png/120px-Pirate_%28Asgarnian_Ice_Dungeon%29.png?7dc66'
            self.enemyDesc = 'An experienced plunderer of the seven seas, the best youve never heard of.'
            self.enemyMaxDefence = 50
            self.enemyMaxAttack = 70
            self.enemyMaxHit = 8
            self.enemyEquipMeleeAtk = 50

    class StoneSnake(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 51
            self.enemyName = 'Stone Snake'
            self.enemyMaxHP = 60
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (240, 1)
            self.enemyDropTable = [(22, 5), (100, 7), (23, 5), (121, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/The_Jormungand.png/280px-The_Jormungand.png?30d7b'
            self.enemyDesc = 'A massive stone snake capable of powerful magic.'
            self.enemyMaxDefence = 60
            self.enemyMaxMagic = 75
            self.enemyMaxHit = 12
            self.enemyEquipMageAtk = 30

        def calculateAttackOnPlayer(self, player):
            dmg, text = self.mageAttack(player)
            return dmg, text

    class CorruptedGoo(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 52
            self.enemyName = 'Corrupted Goo'
            self.enemyMaxHP = 76
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (240, 1)
            self.enemyDropTable = [(239, 15), (239, 20), (30, 5), (94, 5)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Jal-AkRek-Ket.png/250px-Jal-AkRek-Ket.png?aeaf8'
            self.enemyDesc = 'Some kind of mass that has been magically animated and given corrupt ends.'
            self.enemyMaxDefence = 60
            self.enemyMaxAttack = 60
            self.enemyMaxHit = 10
            self.enemyEquipMeleeAtk = 30

    class AdamantKnight(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 53
            self.enemyName = 'Adamant Knight'
            self.enemyMaxHP = 60
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(67, 2), (66, 2), (68, 2), (69, 2)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Adamant_armour_set_%28lg%29_equipped.png/130px-Adamant_armour_set_%28lg%29_equipped.png?43b64'
            self.enemyDesc = 'A knight in full adamant armor.'
            self.enemyMaxDefence = 60
            self.enemyMaxAttack = 60
            self.enemyMaxHit = 12
            self.enemyEquipMeleeAtk = 50

    class WanderingBard(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 54
            self.enemyName = 'Wandering Bard'
            self.enemyMaxHP = 50
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (239, 1)
            self.enemyDropTable = [(239, 10), (208, 30), (111, 10), (244, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Falo_the_Bard.png/140px-Falo_the_Bard.png?154d7'
            self.enemyDesc = 'Feel the music, music, music, music. Keep me movin\', don\'t stop me.'
            self.enemyMaxDefence = 90
            self.enemyMaxMagic = 70
            self.enemyMaxHit = 12
            self.enemyEquipMageAtk = 20

        def calculateAttackOnPlayer(self, player):
            dmg, text = self.mageAttack(player)
            return dmg, text

    class Valkyrie(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 55
            self.enemyName = 'Valkyrie'
            self.enemyMaxHP = 54
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (240, 1)
            self.enemyDropTable = [(239, 10), (92, 5), (222, 1), (239, 30)]
            self.enemyImgURL = 'http://1.bp.blogspot.com/-lBlvtUYY2lI/TXloSVfIsVI/AAAAAAAACpw/T1EkX5U3v_w/s400/valkyriehon.png'
            self.enemyDesc = 'A holy warrior, radiant like you have never seen. It cant be a good sign that they are here.'
            self.enemyMaxDefence = 40
            self.enemyMaxAttack = 70
            self.enemyMaxHit = 11
            self.enemyEquipMeleeAtk = 10

    class ExperiencedMage(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 56
            self.enemyName = 'Experienced Mage'
            self.enemyMaxHP = 80
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (240, 1)
            self.enemyDropTable = [(208, 30), (208, 50), (216, 1), (118, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Zamorak_mage_%28level_84%29.png/150px-Zamorak_mage_%28level_84%29.png?40fdf'
            self.enemyDesc = 'A mage that has had the benefit of managing to live for a decent amount of time.'
            self.enemyMaxDefence = 50
            self.enemyMaxMagic = 80
            self.enemyMaxHit = 12
            self.enemyEquipMageAtk = 50

        def calculateAttackOnPlayer(self, player):
            dmg, text = self.mageAttack(player)
            return dmg, text

    class ZombieBruiser(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 57
            self.enemyName = 'Zombie Bruiser'
            self.enemyMaxHP = 70
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (240, 1)
            self.enemyDropTable = [(61, 2), (62, 2), (101, 3), (240, 20)]
            self.enemyImgURL = 'https://static.wikia.nocookie.net/left4dead/images/1/13/Charger_2.png/revision/latest/scale-to-width-down/311?cb=20120609191223'
            self.enemyDesc = 'A zombie, but much bigger and tougher.'
            self.enemyMaxDefence = 60
            self.enemyMaxAttack = 60
            self.enemyMaxHit = 10
            self.enemyEquipMeleeAtk = 40

    class LesserDemon(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 58
            self.enemyName = 'Lesser Demon'
            self.enemyMaxHP = 65
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (240, 1)
            self.enemyDropTable = [(239, 20), (87, 1), (208, 15), (73, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Lesser_demon_%28lv_87%29.png/150px-Lesser_demon_%28lv_87%29.png?a055b'
            self.enemyDesc = 'A demon that you can just tell is stewing with inferiority syndrome.'
            self.enemyMaxDefence = 65
            self.enemyMaxAttack = 65
            self.enemyMaxHit = 9
            self.enemyEquipMeleeAtk = 30


    class IceMonster(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 59
            self.enemyName = 'Ice Monster'
            self.enemyMaxHP = 50
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (240, 2)
            self.enemyDropTable = [(21, 5), (136, 30), (65, 1), (208, 10)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Ice_troll.png/220px-Ice_troll.png?73c10'
            self.enemyDesc = 'An abominable creature, not quite man, but certainly covered in snow.'
            self.enemyMaxDefence = 70
            self.enemyMaxAttack = 70
            self.enemyMaxHit = 9

        def calculateAttackOnPlayer(self, player):
            choices = [0, 1]
            choice = random.choices(choices, cum_weights=(30, 100), k=1)[0]
            if choice == 0:
                dmg = random.randint(1,self.enemyMaxHit)
                buff = buffsdebuffs.buffFactory(4, player)
                player.applyBuffDebuff(buff)
                text = f'{self.enemyName} smashes <@!{player.DiscordID}> for {dmg}, chilling them!'
                return dmg, text
            else:
                dmg, text = self.meleeAttack(player)
                return dmg, text

    class GreenDragon(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 60
            self.enemyName = 'Green Dragon'
            self.enemyMaxHP = 75
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (241, 1)
            self.enemyDropTable = [(151, 3), (137, 30), (260, 3), (241, 10)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Green_dragon_%283%29.png/290px-Green_dragon_%283%29.png?3aec9'
            self.enemyDesc = 'A terrible green dragon.'
            self.enemyMaxDefence = 68
            self.enemyMaxAttack = 68
            self.enemyMaxHit = 14
            self.enemyEquipMeleeAtk = 20
            self.enemyMaxMagic = 60
            self.enemyAtkSpeed = 6

        def calculateAttackOnPlayer(self, player):
            choices = [0, 1]
            choice = random.choices(choices, cum_weights=(30, 100), k=1)[0]
            if choice == 0:
                self.enemyMaxHit = 20
                dmg, text = self.mageAttack(player)
                if dmg > 0:
                    text = f'Green Dragon breathes magical fire on <@!{player.DiscordID}> for {dmg}!'
                self.enemyMaxHit = 14
                return dmg, text
            else:
                dmg, text = self.meleeAttack(player)
                return dmg, text

    class HolyArcher(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 61
            self.enemyName = 'Aviansie'
            self.enemyMaxHP = 105
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (240, 2)
            self.enemyDropTable = [(137, 30), (138, 30), (225, 1), (94, 5)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Aviansie_%28level_97%2C_2%29.png/230px-Aviansie_%28level_97%2C_2%29.png?08575'
            self.enemyDesc = 'An extremely graceful bird-like creature wielding a radiant bow.'
            self.enemyMaxDefence = 60
            self.enemyMaxRange = 80
            self.enemyMaxHit = 17
            self.enemyEquipRangeAtk = 40
            self.enemyMaxMagic = 30

        def calculateAttackOnPlayer(self, player):
            dmg, text = self.rangeAttack(player)
            return dmg, text

    class Terrordog(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 62
            self.enemyName = 'Terrordog'
            self.enemyMaxHP = 81
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (240, 2)
            self.enemyDropTable = [(101, 5), (102, 5), (30, 10), (95, 3)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Terror_dog_%28level_100%29.png/200px-Terror_dog_%28level_100%29.png?535ad'
            self.enemyDesc = 'A terrifying dog beast of some kind. Well, apparently they arent dogs...'
            self.enemyMaxDefence = 71
            self.enemyMaxAttack = 68
            self.enemyMaxHit = 12
            self.enemyEquipMeleeAtk = 25
            self.enemyMaxMagic = 25

    class PirateCaptain(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 63
            self.enemyName = 'Pirate Captain'
            self.enemyMaxHP = 75
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (240, 3)
            self.enemyDropTable = [(239, 30), (111, 10), (70, 1), (198, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Pirate_%28Cabin_Fever%29.png/120px-Pirate_%28Cabin_Fever%29.png?81c51'
            self.enemyDesc = 'A leader of pirates, one must live a long time in a dangerous life to become such a thing.'
            self.enemyMaxDefence = 65
            self.enemyMaxAttack = 80
            self.enemyMaxHit = 13
            self.enemyEquipMeleeAtk = 65

    class Assassin(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 64
            self.enemyName = 'Assassin'
            self.enemyMaxHP = 55
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (240, 3)
            self.enemyDropTable = [(138, 30), (237, 1), (166, 1), (156, 3)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Assassin_%28A_Kingdom_Divided%2C_1%29.png/120px-Assassin_%28A_Kingdom_Divided%2C_1%29.png?2e86c'
            self.enemyDesc = 'Oh no, here come the ninjas to assassafrassinate me!'
            self.enemyMaxDefence = 105
            self.enemyMaxRange = 95
            self.enemyMaxHit = 12


        def calculateAttackOnPlayer(self, player):
            dmg, text = self.rangeAttack(player)
            return dmg, text

    class IceTroll(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 65
            self.enemyName = 'Ice Troll'
            self.enemyMaxHP = 70
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (240, 3)
            self.enemyDropTable = [(240, 20), (217, 1), (22, 5), (72, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Mother.png/180px-Mother.png?1b765'
            self.enemyDesc = 'Known to be very protective of any nearby large, wandering staircases.'
            self.enemyMaxDefence = 80
            self.enemyMaxAttack = 80
            self.enemyMaxHit = 10

        def calculateAttackOnPlayer(self, player):
            choices = [0, 1]
            choice = random.choices(choices, cum_weights=(30, 100), k=1)[0]
            if choice == 0:
                dmg = random.randint(1,self.enemyMaxHit)
                buff = buffsdebuffs.buffFactory(4, player)
                player.applyBuffDebuff(buff)
                text = f'{self.enemyName} smashes <@!{player.DiscordID}> for {dmg}, chilling them!'
                return dmg, text
            else:
                dmg, text = self.meleeAttack(player)
                return dmg, text

    class Beholder(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 66
            self.enemyName = 'Beholder'
            self.enemyMaxHP = 40
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (240, 3)
            self.enemyDropTable = [(208, 50), (209, 30), (235, 1), (245, 1)]
            self.enemyImgURL = 'http://media.wizards.com/2014/images/dnd/newtodnd/beholder_1.png'
            self.enemyDesc = 'An inherently egotistical being, only valuing itself. Beware the beams.'
            self.enemyMaxDefence = 60
            self.enemyMaxMagic = 120
            self.enemyMaxHit = 14

        def calculateAttackOnPlayer(self, player):
            choices = [0, 1, 2, 3]
            choice = random.choices(choices, cum_weights=(10, 20, 30, 100), k=1)[0]
            if choice == 0:
                dmg = random.randint(1, self.enemyMaxHit)
                buff = buffsdebuffs.buffFactory(4, player)
                player.applyBuffDebuff(buff)
                text = f'{self.enemyName} blasts <@!{player.DiscordID}> for {dmg} with an ice ray!'
                return dmg, text
            elif choice == 1:
                dmg = random.randint(1, self.enemyMaxHit)
                buff = buffsdebuffs.buffFactory(3, player)
                player.applyBuffDebuff(buff)
                text = f'{self.enemyName} blasts <@!{player.DiscordID}> for {dmg} with a poison ray!'
                return dmg, text
            elif choice == 2:
                dmg = 0
                buff = buffsdebuffs.buffFactory(1, self)
                self.applyBuffDebuff(buff)
                text = f'{self.enemyName} blasts itself with one of its own eye beams, and speeds up!'
                return dmg, text
            else:
                dmg, text = self.mageAttack(player)
                return dmg, text

    class EvilSpider(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 67
            self.enemyName = 'Evil Spider'
            self.enemyMaxHP = 75
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (240, 2)
            self.enemyDropTable = [(102, 5), (240, 20), (111, 10), (95, 5)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Giant_spider_%28Level_50%29.png/250px-Giant_spider_%28Level_50%29.png?b4ced'
            self.enemyDesc = 'Normal spiders are just trying to get by and do spider shit, not this one. This one is evil.'
            self.enemyMaxDefence = 80
            self.enemyMaxAttack = 80
            self.enemyMaxHit = 10

        def calculateAttackOnPlayer(self, player):
            choices = [0, 1]
            choice = random.choices(choices, cum_weights=(40, 100), k=1)[0]
            if choice == 0:
                dmg = random.randint(1,self.enemyMaxHit)
                buff = buffsdebuffs.buffFactory(3, player)
                player.applyBuffDebuff(buff)
                text = f'{self.enemyName} bites <@!{player.DiscordID}> for {dmg}, applying a slight poison!'
                return dmg, text
            else:
                dmg, text = self.meleeAttack(player)
                return dmg, text

    class BlueDragon(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 68
            self.enemyName = 'Blue Dragon'
            self.enemyMaxHP = 90
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (241, 3)
            self.enemyDropTable = [(152, 3), (138, 30), (261, 3), (241, 20)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Blue_dragon.png/290px-Blue_dragon.png?1f705'
            self.enemyDesc = 'A vicious blue dragon.'
            self.enemyMaxDefence = 75
            self.enemyMaxAttack = 75
            self.enemyMaxHit = 17
            self.enemyEquipMeleeAtk = 30
            self.enemyMaxMagic = 70
            self.enemyAtkSpeed = 6

        def calculateAttackOnPlayer(self, player):
            choices = [0, 1]
            choice = random.choices(choices, cum_weights=(30, 100), k=1)[0]
            if choice == 0:
                self.enemyMaxHit = 22
                dmg, text = self.mageAttack(player)
                if dmg > 0:
                    text = f'Blue Dragon breathes magical fire on <@!{player.DiscordID}> for {dmg}!'
                self.enemyMaxHit = 17
                return dmg, text
            else:
                dmg, text = self.meleeAttack(player)
                return dmg, text

    class Shaman(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 49
            self.enemyName = 'Shaman'
            self.enemyMaxHP = 75
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (240, 3)
            self.enemyDropTable = [(209, 30), (209, 50), (238, 1), (210, 20)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Grunsh.png/200px-Grunsh.png?bb311'
            self.enemyDesc = 'Seems intelligent.... for an ogre, at least.'
            self.enemyMaxDefence = 85
            self.enemyMaxMagic = 110
            self.enemyMaxHit = 13
            self.enemyEquipMageAtk = 8

        def calculateAttackOnPlayer(self, player):
            dmg, text = self.mageAttack(player)
            return dmg, text

    class TwistedExperiment(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 70
            self.enemyName = 'Twisted Experiment'
            self.enemyMaxHP = 80
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (240, 3)
            self.enemyDropTable = [(138, 50), (236, 1), (114, 3), (115, 2)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Husk_%28ranged%29.png/250px-Husk_%28ranged%29.png?a29e7'
            self.enemyDesc = 'You are not even sure what this once was.'
            self.enemyMaxDefence = 80
            self.enemyMaxRange = 110
            self.enemyMaxHit = 13
            self.enemyEquipRangeAtk = 18

        def calculateAttackOnPlayer(self, player):
            dmg, text = self.rangeAttack(player)
            return dmg, text

    class GreaterDemon(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 71
            self.enemyName = 'Greater Demon'
            self.enemyMaxHP = 82
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (240, 3)
            self.enemyDropTable = [(239, 50), (111, 20), (220, 1), (194, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Greater_demon_%284%29.png/250px-Greater_demon_%284%29.png?f293e'
            self.enemyDesc = 'Greater, huh? Talk about ego problems.'
            self.enemyMaxDefence = 74
            self.enemyMaxAttack = 100
            self.enemyMaxHit = 13

    class RuneKnight(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 72
            self.enemyName = 'Rune Knight'
            self.enemyMaxHP = 80
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (240, 3)
            self.enemyDropTable = [(73, 2), (74, 2), (75, 2), (76, 2)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Rune_armour_set_%28lg%29_equipped.png/130px-Rune_armour_set_%28lg%29_equipped.png?9b396'
            self.enemyDesc = 'A knight in full rune armor.'
            self.enemyMaxDefence = 90
            self.enemyMaxAttack = 90
            self.enemyMaxHit = 21
            self.enemyEquipMeleeAtk = 80
            self.enemyMaxMagic = 90

    class Frogeel(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 73
            self.enemyName = 'Frogeel'
            self.enemyMaxHP = 55
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (242, 1)
            self.enemyDropTable = [(239, 50), (19, 20), (21, 5), (122, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Frogeel.png/275px-Frogeel.png?581bd'
            self.enemyDesc = 'Is it a frog, or is it an eel?'
            self.enemyMaxDefence = 100
            self.enemyMaxAttack = 130
            self.enemyMaxHit = 18
            self.enemyAtkSpeed = 6

    class PirateLord(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 74
            self.enemyName = 'Pirate Lord'
            self.enemyMaxHP = 100
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (242, 1)
            self.enemyDropTable = [(33, 3), (95, 5), (223, 1), (77, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Pirate_%28Brimhaven%29.png/120px-Pirate_%28Brimhaven%29.png?094f1'
            self.enemyDesc = 'A leader of pirate leaders, eyepatch, pegleg and all.'
            self.enemyMaxDefence = 80
            self.enemyMaxAttack = 100
            self.enemyMaxHit = 18
            self.enemyAtkSpeed = 6

    class RedDragon(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 75
            self.enemyName = 'Red Dragon'
            self.enemyMaxHP = 100
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (241, 10)
            self.enemyDropTable = [(153, 3), (139, 30), (262, 3), (79, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Red_dragon.png/290px-Red_dragon.png?f0a8a'
            self.enemyDesc = 'A ferocious red dragon.'
            self.enemyMaxDefence = 90
            self.enemyMaxAttack = 90
            self.enemyMaxHit = 21
            self.enemyEquipMeleeAtk = 45
            self.enemyMaxMagic = 80
            self.enemyAtkSpeed = 6

        def calculateAttackOnPlayer(self, player):
            choices = [0, 1]
            choice = random.choices(choices, cum_weights=(30, 100), k=1)[0]
            if choice == 0:
                self.enemyMaxHit = 25
                dmg, text = self.mageAttack(player)
                if dmg > 0:
                    text = f'Red Dragon breathes magical fire on <@!{player.DiscordID}> for {dmg}!'
                self.enemyMaxHit = 21
                return dmg, text
            else:
                dmg, text = self.meleeAttack(player)
                return dmg, text

    class DarkMage(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 76
            self.enemyName = 'Dark Mage'
            self.enemyMaxHP = 110
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (242, 1)
            self.enemyDropTable = [(209, 50), (210, 20), (103, 3), (242, 10)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Dark_wizard_%28red%29.png/120px-Dark_wizard_%28red%29.png?c649f'
            self.enemyDesc = 'A dark wizard that has gained enough experience in magic to be considered a real mage.'
            self.enemyMaxDefence = 90
            self.enemyMaxMagic = 90
            self.enemyEquipMageAtk = 50
            self.enemyMaxHit = 20

        def calculateAttackOnPlayer(self, player):
            dmg, text = self.mageAttack(player)
            return dmg, text

    class Necromancer(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 77
            self.enemyName = 'Necromancer'
            self.enemyMaxHP = 95
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (242, 2)
            self.enemyDropTable = [(210, 20), (210, 50), (103, 3), (246, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Ancient_Wizard_%28magic%29.png/170px-Ancient_Wizard_%28magic%29.png?4b1cd'
            self.enemyDesc = 'Wise fwom youw gwave.'
            self.enemyMaxDefence = 105
            self.enemyMaxMagic = 125
            self.enemyEquipMageAtk = 20
            self.enemyMaxHit = 16

        def calculateAttackOnPlayer(self, player):
            dmg, text = self.mageAttack(player)
            return dmg, text

    class BanditLeader(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 78
            self.enemyName = 'Bandit Leader'
            self.enemyMaxHP = 150
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (242, 1)
            self.enemyDropTable = [(139, 30), (147, 15), (132, 1), (140, 50)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Iorwerth_Archer_%281%29.png/130px-Iorwerth_Archer_%281%29.png?cc42f'
            self.enemyDesc = 'A leader of one of the many bandit gangs, in strangely familiar armour.'
            self.enemyMaxDefence = 60
            self.enemyMaxRange = 130
            self.enemyMaxHit = 17
            self.enemyEquipRangeAtk = 75

        def calculateAttackOnPlayer(self, player):
            dmg, text = self.rangeAttack(player)
            return dmg, text

    class BlackDragon(Enemy,ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 79
            self.enemyName = 'Black Dragon'
            self.enemyMaxHP = 120
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (241, 8)
            self.enemyDropTable = [(154, 3), (264, 3), (241, 30), (123, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Black_dragon_%283%29.png/290px-Black_dragon_%283%29.png?e0389'
            self.enemyDesc = 'A brutal black dragon.'
            self.enemyMaxDefence = 100
            self.enemyMaxAttack = 100
            self.enemyMaxHit = 27
            self.enemyEquipMeleeAtk = 60
            self.enemyMaxMagic = 90
            self.enemyAtkSpeed = 6

        def calculateAttackOnPlayer(self, player):
            choices = [0, 1]
            choice = random.choices(choices, cum_weights=(30, 100), k=1)[0]
            if choice == 0:
                self.enemyMaxHit = 30
                dmg, text = self.mageAttack(player)
                if dmg > 0:
                    text = f'Black Dragon breathes magical fire on <@!{player.DiscordID}> for {dmg}!'
                self.enemyMaxHit = 27
                return dmg, text
            else:
                dmg, text = self.meleeAttack(player)
                return dmg, text
    class Diablos(Enemy,ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 80
            self.enemyName = 'Diablos'
            self.enemyMaxHP = 200
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (242, 3)
            self.enemyDropTable = [(242, 10), (103, 5), (89, 1), (267, 1)]
            self.enemyImgURL = 'https://static.wikia.nocookie.net/monsterhunter/images/3/39/MHRise-Diablos_Render_001.png/revision/latest/scale-to-width-down/1000?cb=20210217223736'
            self.enemyDesc = 'A colossal creature bearing two massive horns, and none too happy.'
            self.enemyMaxDefence = 140
            self.enemyMaxAttack = 104
            self.enemyMaxHit = 24
            self.enemyAtkSpeed = 5
            self.slam = False

        def calculateAttackOnPlayer(self, player):
            if self.slam:
                dmg, text = self.meleeAttack(player)
                if dmg > 0:
                    dmg = dmg*2
                    text = f'Diablos slams their horns down on <@!{player.DiscordID}>, dealing {dmg} damage!'
                    self.slam = False
                    return dmg, text
                else:
                    text = f'Diablos slams down their horns, but misses <@!{player.DiscordID}>'
                    self.slam = False
                    return dmg, text
            choices = [0, 1]
            choice = random.choices(choices, cum_weights=(30, 100), k=1)[0]
            if choice == 0:
                dmg = 0
                text = f'Diablos raises their horns high.'
                self.slam = True
                return dmg, text
            else:
                dmg, text = self.meleeAttack(player)
                return dmg, text

    class Inquisitor(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 81
            self.enemyName = 'Inquisitor'
            self.enemyMaxHP = 150
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (242, 3)
            self.enemyDropTable = [(242, 10), (140, 30), (116, 3), (226, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Karil_the_Tainted.png/160px-Karil_the_Tainted.png?33092'
            self.enemyDesc = 'A ghostly mage hunter, long since dead but still committed to purging magic.'
            self.enemyMaxDefence = 120
            self.enemyMaxRange = 200
            self.enemyMaxHit = 30

        def calculateAttackOnPlayer(self, player):
            choices = [0, 1]
            choice = random.choices(choices, cum_weights=(25, 100), k=1)[0]
            if choice == 0:
                dmg = random.randint(1, self.enemyMaxHit)
                buff = buffsdebuffs.buffFactory(5, player)
                player.applyBuffDebuff(buff)
                text = f'{self.enemyName} shoots <@!{player.DiscordID}> for {dmg} with a poisoned dart, making them less accurate!'
                return dmg, text
            else:
                dmg, text = self.rangeAttack(player)
                return dmg, text

    class Archmystic(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 82
            self.enemyName = 'Archmystic'
            self.enemyMaxHP = 125
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (242, 3)
            self.enemyDropTable = [(242, 10), (103, 5), (269, 1), (210, 100)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Yt-HurKot.png/220px-Yt-HurKot.png?18fed'
            self.enemyDesc = 'Among the strongest mages still alive.'
            self.enemyMaxDefence = 130
            self.enemyMaxMagic = 220
            self.enemyEquipMageAtk = 50
            self.enemyMaxHit = 31

        def calculateAttackOnPlayer(self, player):
            dmg, text = self.mageAttack(player)
            return dmg, text

    class Alchemist(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 83
            self.enemyName = 'Alchemist'
            self.enemyMaxHP = 180
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (242, 3)
            self.enemyDropTable = [(242, 10), (209, 50), (274, 3), (247, 1)]
            self.enemyImgURL = 'https://www.giantbomb.com/a/uploads/scale_small/0/2179/1518489-alchemist.jpg'
            self.enemyDesc = 'More pockets than you can count or she can remember.'
            self.enemyMaxDefence = 90
            self.enemyMaxMagic = 160
            self.enemyEquipMageAtk = 10
            self.enemyMaxHit = 22

        def calculateAttackOnPlayer(self, player):
            choices = [0, 1, 2, 3]
            choice = random.choices(choices, cum_weights=(10, 20, 30, 100), k=1)[0]
            if choice == 0:
                dmg = random.randint(1, self.enemyMaxHit)
                buff = buffsdebuffs.buffFactory(6, player)
                player.applyBuffDebuff(buff)
                text = f'{self.enemyName} throws acid at <@!{player.DiscordID}> for {dmg}, lowering their defence!'
                return dmg, text
            elif choice == 1:
                dmg = random.randint(1, self.enemyMaxHit)
                buff = buffsdebuffs.buffFactory(3, player)
                player.applyBuffDebuff(buff)
                text = f'{self.enemyName} shoots poison vials at <@!{player.DiscordID}> for {dmg}!'
                return dmg, text
            elif choice == 2:
                dmg = 0
                buff = buffsdebuffs.buffFactory(7, player)
                player.applyBuffDebuff(buff)
                text = f'{self.enemyName} takes a moment to brew up a special potion and throws it at you, applying a DMG down debuff!' # STR DOWN
                return dmg, text
            else:
                dmg, text = self.mageAttack(player)
                return dmg, text

    class FireSpirit(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 84
            self.enemyName = 'Fire Spirit'
            self.enemyMaxHP = 140
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (242, 5)
            self.enemyDropTable = [(242, 20), (103, 5), (95, 20), (195, 1)]
            self.enemyImgURL = 'https://oldschool.runescape.wiki/images/thumb/Fire_elemental.png/160px-Fire_elemental.png?e4577'
            self.enemyDesc = 'The embodiment of energy, an elemental of flame.'
            self.enemyMaxDefence = 120
            self.enemyMaxMagic = 380
            self.enemyMaxHit = 34
            self.minimumHit = 0

        def calculateAttackOnPlayer(self, player):
            choices = [0, 1]
            weight = 25-self.minimumHit
            choice = random.choices(choices, cum_weights=(weight, 100), k=1)[0]
            if choice == 1:
                dmg, text = self.mageAttack(player)
                if dmg > 0 and self.minimumHit > 0:
                    dmg += self.minimumHit
                    text = f'The fire spirit blasts <@!{player.DiscordID}> for {dmg}!'
                else:
                    dmg += self.minimumHit
                    text = f'The fire spirit misses, but the heat of the blasts still singes <@!{player.DiscordID}> for {dmg}!'

                return dmg, text
            else:
                dmg = 0
                self.minimumHit += 1
                text = f'The fire spirit charges up, currently {self.minimumHit} charges.'
                return dmg, text

    class Musk(Enemy, ABC):
        def __init__(self):
            super().__init__()
            self.enemyID = 85
            self.enemyName = 'Musk'
            self.enemyMaxHP = 250
            self.enemyCurrentHP = self.enemyMaxHP
            self.enemyAlwaysDrop = (242, 10)
            self.enemyDropTable = [(242, 50), (83, 2), (123, 1), (117, 1)]
            self.enemyImgURL = 'https://i.imgur.com/vbitq0x.jpg'
            self.enemyDesc = '"That\'s not what anyone meant by \'To the moon,\' you fucking jackass."'
            self.enemyMaxDefence = 380
            self.enemyMaxMagic = 480
            self.enemyMaxAttack = 640
            self.enemyMaxRange = 960
            self.enemyMaxHit = 52
        def calculateAttackOnPlayer(self, player):
            choices = [0, 1, 2, 3]
            choice = random.choices(choices, cum_weights=(30, 60, 90, 100), k=1)[0]
            if choice == 0:
                dmg, text = self.meleeAttack(player)
                return dmg, text
            elif choice == 1:
                dmg, text = self.rangeAttack(player)
                return dmg, text
            elif choice == 2:
                dmg, text = self.mageAttack(player)
                return dmg, text
            else:
                dmg = random.randint(1, 30)
                text = f'<@!{player.DiscordID}> cannot grasp the true form of Musk\'s attack, it deals {dmg} damage.'
                return dmg, text

    # THE BIG IF
    if ID == 1: return Plant()
    if ID == 2: return Bandit()
    if ID == 3: return BuffRat()
    if ID == 4: return Cow()
    if ID == 5: return Goblin()
    if ID == 6: return GoblinMiner()
    if ID == 7: return Chicken()
    if ID == 8: return Farmer()
    if ID == 9: return BigFarmer()
    if ID == 10: return MasterFarmer()
    if ID == 11: return Skelington()
    if ID == 12: return Zombo()
    if ID == 13: return SpookyGhost()
    if ID == 14: return Crab()
    if ID == 15: return BigCrab()
    if ID == 16: return GiantEnemyCrab()
    if ID == 17: return HillGiant()
    if ID == 18: return MossGiant()
    if ID == 19: return Squire()
    if ID == 20: return RangedGoblin()
    if ID == 21: return SteelKnight()
    if ID == 22: return Tentacle()
    if ID == 23: return RiverTroll()
    if ID == 24: return Entrepeneur()
    if ID == 25: return Bat()
    if ID == 26: return BlackKnight()
    if ID == 27: return FrozenArcher()
    if ID == 28: return Terrorbird()
    if ID == 29: return Mummy()
    if ID == 30: return DarkWizard()
    if ID == 31: return MithrilKnight()
    if ID == 32: return Pirate()
    if ID == 33: return Bear()
    if ID == 34: return BigZombo()
    if ID == 35: return GreenRiverTroll()
    if ID == 36: return MommaChicken()
    if ID == 37: return Defiler()
    if ID == 38: return Zombom()
    if ID == 39: return Sandraker()
    if ID == 40: return BigBat()
    if ID == 41: return Brawler()
    if ID == 42: return Spider()
    if ID == 43: return Mushroom()
    if ID == 44: return Vampire()
    if ID == 45: return GreatWizard()
    if ID == 46: return StrangeExperiment()
    if ID == 47: return FrozenMammoth()
    if ID == 48: return Warwelf()
    if ID == 49: return Durid()
    if ID == 50: return FirstMate()
    if ID == 51: return StoneSnake()
    if ID == 52: return CorruptedGoo()
    if ID == 53: return AdamantKnight()
    if ID == 54: return WanderingBard()
    if ID == 55: return Valkyrie()
    if ID == 56: return ExperiencedMage()
    if ID == 57: return ZombieBruiser()
    if ID == 58: return LesserDemon()
    if ID == 59: return IceMonster()
    if ID == 60: return GreenDragon()
    if ID == 61: return HolyArcher()
    if ID == 62: return Terrordog()
    if ID == 63: return PirateCaptain()
    if ID == 64: return Assassin()
    if ID == 65: return IceTroll()
    if ID == 66: return Beholder()
    if ID == 67: return EvilSpider()
    if ID == 68: return BlueDragon()
    if ID == 69: return Shaman()
    if ID == 70: return TwistedExperiment()
    if ID == 71: return GreaterDemon()
    if ID == 72: return RuneKnight()
    if ID == 73: return Frogeel()
    if ID == 74: return PirateLord()
    if ID == 75: return RedDragon()
    if ID == 76: return DarkMage()
    if ID == 77: return Necromancer()
    if ID == 78: return BanditLeader()
    if ID == 79: return BlackDragon()
    if ID == 80: return Diablos()
    if ID == 81: return Inquisitor()
    if ID == 82: return Archmystic()
    if ID == 83: return Alchemist()
    if ID == 84: return FireSpirit()
    if ID == 85: return Musk()
    # and so on
    assert 0, f'Bad ID: {ID}'
