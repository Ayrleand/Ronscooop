from abc import abstractmethod
from enum import Enum
import json
import buffsdebuffs


class Item:
    def __init__(self, ID, itemName, itemDesc, itemEmoj, isCraftable, craftingComponents, xpForCrafting, alchValue):
        self.ID = ID
        self.itemName = itemName
        self.itemDesc = itemDesc
        self.itemEmoj = itemEmoj
        self.isCraftable = isCraftable
        self.craftingComponents = craftingComponents
        self.xpForCrafting = xpForCrafting
        self.alchValue = alchValue


class Consumable(Item):
    def __init__(self, ID, itemName, itemDesc, itemEmoj, isCraftable, craftingComponents, xpForCrafting, alchValue, itemEffects,
                 magnitude):
        super().__init__(ID, itemName, itemDesc, itemEmoj, isCraftable, craftingComponents, xpForCrafting, alchValue)
        self.itemEffects = itemEffects
        # itemEffects MUST BE A LIST
        self.magnitude = magnitude


    def use(self, owner, target):
        a = ""
        if str(self.ID) in owner.playerInventory:
            if owner.playerEatDelay > 0:
                return f'You must wait {owner.playerEatDelay} ticks to eat again!'
            if owner.inCombat:
                owner.changeEatDelay(6)
                owner.changeAttackDelay(3)
            owner.addToInventory(self.ID, -1)
            for effect in self.itemEffects:
                a += getattr(self, f'{effect}')(self.magnitude, target)
            return a
        else:
            return f'User does not have that item.\n'
    # What are the things that consumable items could do? You can feed them targets, stat names, values, durations
    def heal(self, magnitude, target):
        target.changePlayerHP(magnitude)
        return f'<@!{target.DiscordID}> heals for {magnitude} by consuming {self.itemName}!\n'
    def damage(self, magnitude, target):
        target.changeEnemyHP(-magnitude)

    def overheal(self, magnitude, target):
        target.overhealPlayer(magnitude)
        return f'<@!{target.DiscordID}> heals for {magnitude} by consuming {self.itemName}!\n'

    def prayerExp(self, magnitude, target):
        baseExp = magnitude
        xpGained, leveledUp = target.givePlayerExperience("prayer", baseExp)
        if leveledUp:
            return leveledUp
        else:
            return f'<@!{target.DiscordID}> gains {xpGained} Prayer Experience!\n'

    def healregen(self, magnitude, target):
        buff = buffsdebuffs.buffFactory(2, target)
        target.applyBuffDebuff(buff)
        target.changePlayerHP(magnitude)
        return f'<@!{target.DiscordID}> heals for {magnitude} and gains a slight regen by consuming {self.itemName}!\n'


class Equippable(Item):
    def __init__(self, ID, itemName, itemDesc, itemEmoj, isCraftable, craftingComponents, xpForCrafting, alchValue, equipmentStats,
                 equipmentSlots, equipmentReqs):
        super().__init__(ID, itemName, itemDesc, itemEmoj, isCraftable, craftingComponents, xpForCrafting, alchValue)
        self.equipmentStats = equipmentStats
        self.equipmentSlots = equipmentSlots
        self.equipmentReqs = equipmentReqs



# Write a big ass Enum for item ID, item name
class ItemType(Enum):
    LOGS = 1
    OAKLOGS = 2
    WILLOWLOGS = 3
    TEAKLOGS = 4
    MAPLELOGS = 5
    MAHOGANYLOGS = 6
    YEWLOGS = 7
    MAGICLOGS = 8
    REDWOODLOGS = 9
    RAWSHRIMP = 10
    RAWSARDINE = 11
    RAWTROUT = 12
    RAWSALMON = 13
    RAWLOBSTER = 14
    RAWSWORDFISH = 15
    COPPERORE = 16
    TINORE = 17
    IRONORE = 18
    COALORE = 19
    SILVERORE = 20
    GOLDORE = 21
    MITHRILORE = 22
    ADAMANTORE = 23
    RUNITEORE = 24
    DRAGONITEORE = 25
    BRONZEBAR = 26
    IRONBAR = 27
    STEELBAR = 28
    SILVERBAR = 29
    GOLDBAR = 30
    MITHRILBAR = 31
    ADAMANTBAR = 32
    RUNEBAR = 33
    DRAGONBAR = 34
    BRONZESCIMITAR = 35
    BRONZEBATTLEAXE = 36
    BRONZE2HSWORD = 37
    BRONZEHELMET = 38
    BRONZEBOOTS = 39
    BRONZEPLATELEGS = 40
    BRONZEPLATEBODY = 41
    IRONSCIMITAR = 42
    IRONBATTLEAXE = 43
    IRON2HSWORD = 44
    IRONHELMET = 45
    IRONBOOTS = 46
    IRONPLATELEGS = 47
    IRONPLATEBODY = 48
    STEELSCIMITAR = 49
    STEELBATTLEAXE = 50
    STEEL2HSWORD = 51
    STEELHELMET = 52
    STEELBOOTS = 53
    STEELPLATELEGS = 54
    STEELPLATEBODY = 55
    MITHRILSCIMITAR = 56
    MITHRILBATTLEAXE = 57
    MITHRIL2HSWORD = 58
    MITHRILHELMET = 59
    MITHRILBOOTS = 60
    MITHRILPLATELEGS = 61
    MITHRILPLATEBODY = 62
    ADAMANTSCIMITAR = 63
    ADAMANTBATTLEAXE = 64
    ADAMANT2HSWORD = 65
    ADAMANTHELMET = 66
    ADAMANTBOOTS = 67
    ADAMANTPLATELEGS = 68
    ADAMANTPLATEBODY = 69
    RUNESCIMITAR = 70
    RUNEBATTLEAXE = 71
    RUNE2HSWORD = 72
    RUNEHELMET = 73
    RUNEBOOTS = 74
    RUNEPLATELEGS = 75
    RUNEPLATEBODY = 76
    DRAGONSCIMITAR = 77
    DRAGONBATTLEAXE = 78
    DRAGON2HSWORD = 79
    DRAGONHELMET = 80
    DRAGONBOOTS = 81
    DRAGONPLATELEGS = 82
    DRAGONPLATEBODY = 83
    BRONZESHIELD = 84
    IRONSHIELD = 85
    STEELSHIELD = 86
    MITHRILSHIELD = 87
    ADAMANTSHIELD = 88
    RUNESHIELD = 89
    DRAGONSHIELD = 90
    TOPAZ = 91
    SAPPHIRE = 92
    EMERALD = 93
    RUBY = 94
    DIAMOND = 95
    POTATOSEEDS = 96
    ONIONSEEDS = 97
    CABBAGESEEDS = 98
    TOMATOSEEDS = 99
    CORNSEEDS = 100
    STRAWBERRYSEEDS = 101
    WATERMELONSEEDS = 102
    SNAPEGRASSSEEDS = 103
    POTATOES = 104
    ONIONS = 105
    CABBAGES = 106
    CORN = 107
    STRAWBERRIES = 108
    WATERMELONS = 109
    SNAPEGRASS = 110
    COMPOST = 111
    ACORN = 112
    WILLOWTREESEEDS = 113
    MAPLETREESEEDS = 114
    YEWTREESEEDS = 115
    MAGICTREESEEDS = 116
    AMULETOFSKILLING = 117
    AMULETOFSTRENGTH = 118
    AMULETOFDEFENCE = 119
    AMULETOFACCURACY = 120
    AMULETOFRANGED = 121
    AMULETOFGLORY = 122
    AMULETOFFURY = 123
    AMULETOFTORTURE = 124
    FEATHERS = 125
    BOWSTRINGS = 126
    NORMALBOW = 127
    OAKBOW = 128
    WILLOWBOW = 129
    MAPLEBOW = 130
    YEWBOW = 131
    MAGICBOW = 132
    REDWOODBOW = 133
    BRONZEARROWS = 134
    IRONARROWS = 135
    STEELARROWS = 136
    MITHRILARROWS = 137
    ADAMANTARROWS = 138
    RUNEARROWS = 139
    DRAGONARROWS = 140
    BRONZEARROWTIPS = 141
    IRONARROWTIPS = 142
    STEELARROWTIPS = 143
    MITHRILARROWTIPS = 144
    ADAMANTARROWTIPS = 145
    RUNEARROWTIPS = 146
    DRAGONARROWTIPS = 147
    ARROWSHAFTS = 148
    HEADLESSARROWS = 149
    COWHIDE = 150
    GREENDRAGONHIDE = 151
    BLUEDRAGONHIDE = 152
    REDDRAGONHIDE = 153
    BLACKDRAGONHIDE = 154
    LEATHER = 155
    GREENDRAGONLEATHER = 156
    BLUEDRAGONLEATHER = 157
    REDDRAGONLEATHER = 158
    BLACKDRAGONLEATHER = 159
    LEATHERCOWL = 160
    LEATHERBOOTS = 161
    LEATHERGLOVES = 162
    LEATHERVAMBRACES = 163
    LEATHERCHAPS = 164
    LEATHERBODY = 165
    GREENDHIDEVAMBRACES = 166
    GREENDHIDECHAPS = 167
    GREENDHIDEBODY = 168
    BLUEDHIDEVAMBRACES = 169
    BLUEDHIDECHAPS = 170
    BLUEDHIDEBODY = 171
    REDDHIDEVAMBRACES = 172
    REDDHIDECHAPS = 173
    REDDHIDEBODY = 174
    BLACKDHIDEVAMBRACES = 175
    BLACKDHIDECHAPS = 176
    BLACKDHIDEBODY = 177
    SILVERTOPAZRING = 178
    SILVERSAPPHIRERING = 179
    SILVEREMERALDRING = 180
    SILVERRUBYRING = 181
    SILVERDIAMONDRING = 182
    GOLDTOPAZRING = 183
    GOLDSAPPHIRERING = 184
    GOLDEMERALDRING = 185
    GOLDRUBYRING = 186
    GOLDDIAMONDRING = 187
    GOLDTOPAZNECKLACE = 188
    GOLDSAPPHIRENECKLACE = 189
    GOLDEMERALDNECKLACE = 190
    GOLDRUBYNECKLACE = 191
    GOLDDIAMONDNECKLACE = 192
    BASICCAPE = 193
    REINFORCEDCAPE = 194
    FIRECAPE = 195
    INFERNOCAPE = 196
    RANGERHAT = 197
    RANGERBOOTS = 198
    BATTEREDCHEST = 199
    AVERAGECHEST = 200
    EXQUISITECHEST = 201
    RUNEESSENCE = 202
    AIRRUNE = 203
    WATERRUNE = 204
    EARTHRUNE = 205
    FIRERUNE = 206
    MINDRUNE = 207
    CHAOSRUNE = 208
    DEATHRUNE = 209
    BLOODRUNE = 210
    BODYRUNE = 211
    NATURERUNE = 212
    SPIRITRUNE = 213
    ANCIENTRUNE = 214
    AIRSTAFF = 215
    AIRBATTLESTAFF = 216
    AIRMYSTICSTAFF = 217
    WATERSTAFF = 218
    WATERBATTLESTAFF = 219
    WATERMYSTICSTAFF = 220
    EARTHSTAFF = 221
    EARTHBATTLESTAFF = 222
    EARTHMYSTICSTAFF = 223
    FIRESTAFF = 224
    FIREBATTLESTAFF = 225
    FIREMYSTICSTAFF = 226
    WIZARDHAT = 227
    WIZARDROBES = 228
    WIZARDROBEBOTTOMS = 229
    WIZARDBOOTS = 230
    MAGEHAT = 231
    MAGEROBES = 232
    MAGEROBEBOTTOMS = 233
    MAGEBOOTS = 234
    MYSTICHAT = 235
    MYSTICROBES = 236
    MYSTICROBEBOTTOMS = 237
    MYSTICBOOTS = 238
    BONES = 239
    BIGBONES = 240
    DRAGONBONES = 241
    MAGICBONES = 242
    STEELGLOVES = 243
    MITHRILGLOVES = 244
    ADAMANTGLOVES = 245
    RUNEGLOVES = 246
    BARROWSGLOVES = 247
    RAWCHICKEN = 248
    CHICKEN = 249
    TOMATOES = 250
    RAWTUNA = 251
    RAWKARAMBWAN = 252
    RAWSHARK = 253
    RAWMANTARAY = 254
    RAWANGLERFISH = 255
    SHRIMP = 256
    SARDINES = 257
    TROUT = 258
    SALMON = 259
    TUNA = 260
    LOBSTER = 261
    SWORDFISH = 262
    KARAMBWAN = 263
    SHARKS = 264
    MANTARAYS = 265
    ANGLERFISH = 266
    POGGERSBOWSTRING = 267
    DRAGONCLAW = 268
    DRAGONCLAWFRAGMENT = 269
    STEWEDCABBAGE = 270
    STEWS = 271
    COOKEDCORN = 272
    TUNAPOTATOES = 273
    SUMMERPIES = 274
    PREPAREDRAY = 275


class ItemCreator:
    "THe Item Factory"
    item_dict = {}

    # def create_potato(self):
    #     item_type = ItemType.POTATOES
    #     if item_type in ItemCreator.item_dict:
    #         return ItemCreator.item_dict[item_type]
    #     ItemCreator.item_dict[item_type] = Consumable(item_type.value, "Potatoes", "Some potatoes.")
    #     return ItemCreator.item_dict[item_type]

    def create_item(self, id):
        try:
            if id > 0:
                item_type = ItemType(id)
                with open("data.txt") as json_file:
                    items = json.load(json_file)
                if item_type in ItemCreator.item_dict:
                    return ItemCreator.item_dict[item_type]
                itemID = None
                itemName = None
                itemDesc = None
                itemEmoj = None
                isCraftable = None
                craftingComponents = None
                xpForCrafting = None
                equipmentStats = None
                alchValue = None
                itemEffects = None
                for item in items:
                    if item["id"] == id:
                        itemID = item["id"]
                        itemName = item["itemName"]
                        itemDesc = item["itemDesc"]
                        itemEmoj = item["itemEmoj"]
                        isCraftable = item["isCraftable"]
                        craftingComponents = item["craftingComponents"]
                        xpForCrafting = item["xpForCrafting"]
                        alchValue = item["alchValue"]
                        if "equipmentStats" in item:
                            equipmentStats = item["equipmentStats"]
                            equipmentSlots = item["equipmentSlots"]
                            equipmentReqs = item["equipmentReqs"]
                        elif "itemEffects" in item:
                            itemEffects = item["itemEffects"]
                            magnitude = item["magnitude"]
                if itemID and itemName and itemDesc:
                    if equipmentStats:
                        ItemCreator.item_dict[item_type] = Equippable(itemID, itemName, itemDesc, itemEmoj, isCraftable,
                                                                      craftingComponents, xpForCrafting, alchValue, equipmentStats,
                                                                      equipmentSlots, equipmentReqs)

                    elif itemEffects:
                        ItemCreator.item_dict[item_type] = Consumable(itemID, itemName, itemDesc, itemEmoj, isCraftable,
                                                                      craftingComponents, xpForCrafting, alchValue, itemEffects,
                                                                        magnitude)
                    else:
                        ItemCreator.item_dict[item_type] = Item(itemID, itemName, itemDesc, itemEmoj, isCraftable,
                                                                craftingComponents, xpForCrafting, alchValue)
                    return ItemCreator.item_dict[item_type]
                else:
                    print(f'Something went wrong, most likely you tried to create an item that is not fully implemented')
            elif id == 0:
                pass
            else:
                print(f'That item ID is out of range.')
        except TypeError:
            pass