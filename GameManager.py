import discord
from player import Player
from Items import ItemType

class GameManager:
    allPlayers = []
    allEnemies = []

    def __init__(self, ItemManager, bot):
        print(f'Game Manager Loaded')
        self.ItemManager = ItemManager
        self.bot = bot
        self.guild = discord.utils.get(bot.guilds, name='intellectuals emote server')
        self.expTable = {
            1: 0,
            2: 83,
            3: 174,
            4: 276,
            5: 388,
            6: 512,
            7: 650,
            8: 801,
            9:969,
            10:1154,
            11:1358,
            12: 1584,
            13:1833,
            14:2107,
            15:2411,
            16:2746,
            17:3115,
            18:3523,
            19:3973,
            20:4470,
            21:5018,
            22:5624,
            23:6291,
            24:7028,
            25:7842,
            26:8740,
            27:9730,
            28:10824,
            29:12031,
            30:13363,
            31:14833,
            32:16453,
            33:18247,
            34:20224,
            35:22406,
            36:24815,
            37:27473,
            38:30408,
            39:33648,
            40:37224,
            41:41171,
            42:45529,
            43:50339,
            44:55649,
            45:61512,
            46:67983,
            47:75127,
            48:83014,
            49:91721,
            50:101333,
            51:111945,
            52:123660,
            53:136594,
            54:150872,
            55:166636,
            56:184040,
            57:203254,
            58:224466,
            59:247866,
            60:273742,
            61:302288,
            62:333804,
            63:368599,
            64:407015,
            65:449428,
            66:496254,
            67:547953,
            68:605032,
            69:668051,
            70:737627,
            71:814445,
            72:899257,
            73:992895,
            74:1096278,
            75:1210421,
            76:1336443,
            77:1475581,
            78:1629200,
            79:1798808,
            80:1986068,
            81:2192818,
            82:2421087,
            83:2673114,
            84:2951373,
            85:3258594,
            86:3597792,
            87:3972294,
            88:4385776,
            89:4842295,
            90:5346332,
            91:5902831,
            92:6517253,
            93:7195629,
            94:7944614,
            95:8771558,
            96:9684577,
            97:10692629,
            98:11805606,
            99:13034431,
            100:14391160,
            101:15889109,
            102:17542976,
            103:19368992,
            104:21385073,
            105:23611066,
            106:26068632,
            107:28782069,
            108:31777943,
            109:35085654,
            110:38737661,
            111:42769801,
            112:47221641,
            113:52136869,
            114:57563718,
            115:63555443,
            116:70170840,
            117:77474828,
            118:85539082,
            119:94442737,
            120:104273167,
            121:115126838,
            122:127110260,
            123:140341028,
            124:154948977,
            125:188884740,
            126:200000000
        }


    # Give the bot which knows the guild, for each member in the server, check if that person is in the DB already and
    # make sure they're not a bot. If they aren't in the DB, make them the default user object. If they're not a bot,
    # Spawn that player.
    def getGuild(self, bot):
        usersMade = 0
        for member in bot.guild.members:
            if not bot.db.testuserdata.find_one({"Player.Info.DiscordID": member.id}) and not member.bot:
                user = {
                    "Player": {
                        "Inventory": {},
                        "Skills": {
                            "maxhp": {
                                "Level": 3,
                                "Experience": 184,
                                "nextLevel": 276
                            },
                            "attack": {
                                "Level": 1,
                                "Experience": 0,
                                "nextLevel": 83
                            },
                            "strength": {
                                "Level": 1,
                                "Experience": 0,
                                "nextLevel": 83
                            },
                            "defence": {
                                "Level": 1,
                                "Experience": 0,
                                "nextLevel": 83
                            },
                            "ranged": {
                                "Level": 1,
                                "Experience": 0,
                                "nextLevel": 83
                            },
                            "magic": {
                                "Level": 1,
                                "Experience": 0,
                                "nextLevel": 83
                            },
                            "prayer": {
                                "Level": 1,
                                "Experience": 0,
                                "nextLevel": 83
                            },
                            "mining": {
                                "Level": 1,
                                "Experience": 0,
                                "nextLevel": 83
                            },
                            "fishing": {
                                "Level": 1,
                                "Experience": 0,
                                "nextLevel": 83
                            },
                            "farming": {
                                "Level": 1,
                                "Experience": 0,
                                "nextLevel": 83
                            },
                            "woodcutting": {
                                "Level": 1,
                                "Experience": 0,
                                "nextLevel": 83
                            },
                            "smithing": {
                                "Level": 1,
                                "Experience": 0,
                                "nextLevel": 83
                            },
                            "crafting": {
                                "Level": 1,
                                "Experience": 0,
                                "nextLevel": 83
                            },
                            "fletching": {
                                "Level": 1,
                                "Experience": 0,
                                "nextLevel": 83
                            },
                            "cooking": {
                                "Level": 1,
                                "Experience": 0,
                                "nextLevel": 83
                            },
                            "runecrafting": {
                                "Level": 0,
                                "Experience": 0,
                                "nextLevel": 0
                            }
                        },
                        "Info": {
                            "DiscordID": member.id,
                            "Currency": 0,
                            "Wins": 0,
                            "Losses": 0,
                            "inventorySize": 20,
                            "food": 0,
                            "maxplots": 4
                        },
                        "Pets": {},
                        "Modifiers": {
                            "currencyGainRate": 1,
                            "experienceRate": 0.5,
                            "skillingRate": 3.0,

                        },
                        "Equipment": {
                            "head": 0,
                            "body": 0,
                            "legs": 0,
                            "feet": 0,
                            "hands": 0,
                            "mhand": 0,
                            "ohand": 0,
                            "back": 0,
                            "neck": 0,
                            "ammo": 0,
                            "ring1": 0,
                            "ring2": 0
                        },
                        "farm": {

                        }
                    }
                }
                u = bot.db.testuserdata.insert_one(user)
                usersMade += 1
            if not member.bot:
                self.spawnPlayer(member, bot)

        print(f'Made {usersMade} new users in DB and spawned their players.')

    # Converts an item name without spaces or item ID into the item object of that item, if it can find it.
    # Used to get from an item ID to a name or other properties usually
    def inputToItem(self, input):
        if input.isdigit():
            itemID = int(input)
            item = self.itemIDToItem(itemID)
            if item:
                return item
            else:
                print(f'{input} not found using inputToItem.')
        else:
            itemID = self.itemNameToID(input)
            item = self.itemIDToItem(itemID)
            if item:
                return item
            else:
                print(f'{input} not found using inputToItem.')

    # Occasionally, players will get stuck due to an unknown network error. We still don't know what causes the error
    # but this function should allow us to individually reset players when this happens rather than reset the whole bot.
    def reset(self, user, bot):
        player = self.getPlayer(user.id)
        self.allPlayers.remove(player)
        self.spawnPlayer(user, bot)
        print(f'Attempted to reset {user.display_name}')

    # Checks if the player is already in the player list, if they aren't, creates a Player object for them and
    # puts it in there.
    def spawnPlayer(self, user: discord.user, bot):
        player = Player(user, bot)
        if player.DiscordID not in [x.DiscordID for x in self.allPlayers]:
            self.allPlayers.append(player)
            print(f'{user.display_name} added! Players: {[x.DiscordID for x in self.allPlayers]}')
        else:
            print(f'We already have that player!')


    # Given a Discord ID, finds a player with that ID in the player list and returns them.
    def getPlayer(self, discordID):
        for player in self.allPlayers:
            if player.DiscordID == discordID:
                return player
        print(f'getPlayer could not find a player of the given ID!')
        return

    # Converts an item ID into that item object, if it exists.
    def itemIDToItem(self, ID):
        item = self.ItemManager.itemCreator.create_item(ID)
        return item

    # Converts an item name without spaces into an item object, if it exists.
    def itemNameToID(self, name):
        name.replace(" ", "")
        name = name.upper()
        if name in ItemType.__members__:
            ID = ItemType[f'{name}'].value
            return ID
        else:
            print(f'Could not find an item with that name.')

    # Gives an item to a player from the game manager. Used in the dev command !give.
    def giveItemToPlayer(self, itemID, user: discord.user, count: int):
        player = self.getPlayer(user.id)
        response = player.addToInventory(itemID, count)
        return response

