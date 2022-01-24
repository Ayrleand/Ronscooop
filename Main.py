import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient
from GameManager import GameManager
from ItemManager import ItemManager
from playground.buffmanager import BuffMgmtCog

#This section loads things like the bot's token and guild ID to be used from an outside env file for security.
load_dotenv()
MONGO = os.getenv('MONGO_CONNECTION_STRING')
client = MongoClient(MONGO)
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#Intents are required for most discord bot actions now
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

#Remove default help command, I want to make my own
bot.remove_command('help')
bot.db = client.testuserdata
itemManager = ItemManager()
bot.gameManager = GameManager(itemManager, bot)




@bot.event
async def on_ready():
    print(f'Reactor Online, Sensors Online, Weapons Online, All Systems: Nominal.')

    bot.guild = discord.utils.get(bot.guilds, name=GUILD)
    bot.gameManager.getGuild(bot)
    print(f'{bot.user} is connected to {bot.guild.name}(ID: {bot.guild.id})')
    bot.load_extension("devCog")
    bot.load_extension("playerCog")
    bot.load_extension("combat")
    bot.load_extension("smithing")
    bot.load_extension("mining")
    bot.load_extension("farming")
    bot.load_extension("fishing")
    bot.load_extension("woodcutting")
    bot.load_extension("cooking")
    bot.load_extension("fletching")
    bot.load_extension("crafting")
    bot.buffManager = BuffMgmtCog(bot)
    await bot.buffManager.theLoop()

@bot.event
async def on_member_join(member):
    # This function runs when a new person joins the guild, searching for them in the player DB and creating a new player
    if not bot.db.testuserdata.find_one({"Player.Info.DiscordID": member.id}):
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
        print(f'{member.display_name} has joined, added new object to the DB.')
        bot.gameManager.spawnPlayer(member, bot)
        await member.create_dm()
        await member.dm_channel.send(f'Greetings {member.name}, your skull size has been documented.')


@bot.command(name='refreshCog', help='Reloads the given Cog.')
async def refreshCog(ctx, *args):
    if args and ctx.message.author.id == 111341531058675712:
        bot.reload_extension(f'{args[0]}')


@bot.command(name='loadCog', help='Attempt to load a cog')
async def loadCog(ctx, *args):
    if args and ctx.message.author.id == 111341531058675712:
        bot.load_extension(f'{args[0]}')


@bot.command(name='unloadCog', help='Attempt to load a cog')
async def unloadCog(ctx, *args):
    if args and ctx.message.author.id == 111341531058675712:
        bot.unload_extension(f'{args[0]}')

@bot.command(name='help', aliases=['hlep', 'Help', 'Hlep'])
async def help(ctx):
    embed = discord.Embed(title="Ronscoop Command Reference / FAQ",
                          url="https://docs.google.com/document/d/1e-66FZgH3mkSoLTTfYbD11fzBVFrpOuQOoILedgrZfA/edit?usp=sharing",
                          color=0xd400ff)
    await ctx.send(embed=embed, delete_after=60)


bot.run(TOKEN)
