# This cog contains "developer commands." So any commands that a GM in an MMO would want to do, we would put in here.
# We can have a list of allowed DiscordIDs at the top that is checked before each command.

import random
import discord
from discord.ext import commands, tasks
from buffsdebuffs import buffFactory
import asyncio


def setup(bot):
    bot.add_cog(devCog(bot))
    print('DevTest Cog Loaded')


class devCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = discord.utils.get(bot.guilds, name='intellectuals emote server')
        self.allowedIDs = [111341531058675712]

    def inputToItem(self, input):
        if input.isdigit():
            itemID = int(input)
            item = self.bot.gameManager.itemIDToItem(itemID)
            if item:
                return item
            else:
                print(f'Item not found.')
        else:
            itemID = self.bot.gameManager.itemNameToID(input)
            item = self.bot.gameManager.itemIDToItem(itemID)
            if item:
                return item
            else:
                print(f'Item not found')

    @commands.command()
    async def resetPlayer(self, ctx, *args):
        if ctx.message.author.id == ctx.message.mentions[0] or ctx.message.author.id == 111341531058675712:
            target = ctx.message.mentions[0]
            self.bot.gameManager.reset(target, self.bot)
            await ctx.send(f'Reset player <@!{target.id}>!', delete_after=30)
            return
        else:
            await ctx.send(f'You can only reset yourself!', delete_after=30)
        if not args:
            self.bot.gameManager.reset(ctx.message.author, self.bot)
            return


    @commands.command(aliases=['exp'])
    async def giveExp(self, ctx, *args):
        if ctx.message.author.id not in self.allowedIDs:
            await ctx.send('This is a developer command that you do not have access to :(', delete_after=10)
            return
        if not args:
            await ctx.send('This command requires arguments! !exp [player ping] [skill] [amount]', delete_after=15)
        target = None
        skill = None
        amount = None
        try:
            target = ctx.message.mentions[0]
            player = self.bot.gameManager.getPlayer(target.id)
            skill = str(args[1])
            amount = abs(int(args[2]))
        except IndexError:
            await ctx.send('One of the arguments was not initialized correctly, please check your syntax. !exp [player ping] [skill] [amount]', delete_after=15)
        embed = None
        try:
            print(f'Developer Give Experience command used to give {player.DiscordID} {amount} exp in {skill}')

            xpGained, embed = player.givePlayerExperience(skill, amount)
        except KeyError:
            await ctx.send('Key Error when giving player experience, likely skill name wasn\'t found.', delete_after=15)
        if embed:
            await ctx.send(content=f'Gave {target} {amount} experience in {skill}!', embed=embed, delete_after=300)
        else:
            await ctx.send(f'Gave {target} {amount} experience in {skill}!')

    @commands.command()
    async def welcome(self, ctx):
        if ctx.message.author.id not in self.allowedIDs:
            await ctx.send('This is a developer command that you do not have access to :(', delete_after=10)
            return
        await ctx.send(
            f'Welcome to Duel Bot v0.3, this update brought to you by caffeine and eurobeat! In the wake of calamitous events, everyone\'s resources have been lost, '
            f'along with most of the scrip. We must all rebuild in a world populated with enemies to fight, resources to gather, and things to craft. Ugh, it sounds like a four horsemen game.\n'
            f'Please be aware of a couple things: One, this whole thing was written in about 2 weeks, 3 weeks if we count the time I just spent picking up python and discordpy. '
            f'There are going to be bugs, and bugs I will work on fixing, even if I don\'t end up adding anything. Two, this bot is quite verbose, and many command responses are pretty large. '
            f'This means that things almost all look like shit on mobile, **and it is requested that you try to keep bot stuff to the channels made for that purpose.** '
            f'The bot does its best to clean up after itself, but you\'ll be glad that no one is trying to look at their inventory while you\'re trying to watch your combat. \n'
            f'This bot is almost entirely controlled by commands, with the prefix \'!\'. A few things will ask for confirmation by clicking a reaction, but that\'s it. '
            f'Commands will try to help if you if they can if something is input wrong, but most likely Ill just be thrown an error. Since this message is already getting long, '
            f'the command reference guide and FAQ can be accessed with !help.  I\'ll be updating this as I learn more about what information people need, or to at least add to the known bugs section.')

    @commands.command(aliases=['give'])
    async def giveItem(self, ctx, *args):
        if ctx.message.author.id not in self.allowedIDs:
            await ctx.send('This is a developer command that you do not have access to :(',delete_after=10)
            return
        if args:
            try:
                if ctx.message.mentions[0] and int(args[1]) and int(args[2]):
                    target = ctx.message.mentions[0]
                    itemID = int(args[1])
                    count = int(args[2])
                    print(f'Developer Give Item command used to give {target.display_name} {count} {itemID} (Item ID).')
                    await ctx.send(f'{self.bot.gameManager.giveItemToPlayer(itemID, target, count)}')

            except IndexError:
                print(f'Bad thing')
        else:
            print(f'Please args')

    @commands.command(aliases=['show', 'ShowItem', 'Show', 'shwo', 'swho'])
    async def showItem(self, ctx, *args):
        item = self.inputToItem(args[0])
        embed = discord.Embed(title=f'**{item.itemName}, ** ID: {item.ID}',
                              description=f"```{item.itemDesc}```", color=0xd25151)
        embed.set_thumbnail(url=item.itemEmoj)
        embed.add_field(name=f'Alch Value', value=f'{item.alchValue}', inline=True)
        if item.isCraftable:
            craftComps = ''
            for exItem in item.craftingComponents:
                i = self.bot.gameManager.itemIDToItem(int(exItem))
                craftComps += f'{i.itemName}: {item.craftingComponents[exItem]}\n'
            embed.add_field(name=f'Crafting Components', value=f'{craftComps}', inline=True)
        try:
            if item.equipmentStats:
                m = ''
                for stat in item.equipmentStats:
                    m += f'{stat}:{item.equipmentStats[stat]}\n'
                embed.add_field(name=f'Equipment Slot', value=f'{item.equipmentSlots}', inline=False)
                embed.add_field(name=f'Equipment Stats', value=f'{m}', inline=True)
                embed.add_field(name=f'Equipment Reqs', value=f'{item.equipmentReqs}', inline=True)
        except AttributeError:
            pass
        try:
            if item.itemEffects:
                if 'heal' in item.itemEffects:
                    embed.add_field(name=f'Consumable', value=f'+{item.magnitude} HP', inline=False)
        except AttributeError:
            pass
        await ctx.send(embed=embed, delete_after=30)
        await ctx.message.delete()
    @commands.command()
    async def giveMuns(self, ctx, *args):
        if ctx.message.author.id not in self.allowedIDs:
            await ctx.send('This is a developer command that you do not have access to :(',delete_after=10)
            return
        # Argument 1 should be int, Argument 2 should be a mention
        if args:
            try:
                amount = int(args[0])
                target = ctx.message.mentions[0]
                player = self.bot.gameManager.getPlayer(target.id)
                newScrip = player.changeScrip(amount)
                print(f'Developer Give Muns command used to give {target.display_name} {amount} Scrip!')
                await ctx.send(f'Gave {target.display_name} {amount} Scrip! They now have {newScrip}')
            except IndexError:
                await ctx.send(f'Something went wrong, are you sure you provided an integer to give and a mention to give it to?')
            except ValueError:
                await ctx.send(f'Got a ValueError, did you put the ping before the integer? Syntax is !giveMuns [integer] [ping user]')
        else:
            await ctx.send('Please provide some arguments! At least an integer amount to give is required.')

    @commands.command()
    async def whack(self, ctx, *args):
        if ctx.message.author.id not in self.allowedIDs:
            await ctx.send('This is a developer command that you do not have access to :(',delete_after=10)
            return
        amt = -int(args[0])
        player = self.bot.gameManager.getPlayer(ctx.message.author.id)
        player.changePlayerHP(amt)
        print(f'Developer Whack command used to whack {player.DiscordID} for {amt}!')
        await ctx.send(f'Whacked <@!{player.DiscordID}>, their HP is now {player.playerCurrentHP}')

    @commands.command()
    async def giveBuff(self, ctx, *args):
        if ctx.message.author.id not in self.allowedIDs:
            await ctx.send('This is a developer command that you do not have access to :(',delete_after=10)
            return
        if not args:
            print(f'Please args')
        try:
            buffID = int(args[1])
            target = ctx.message.mentions[0]
        except IndexError:
            await ctx.send(f'Please provide the correct command syntax. !giveBuff [user] [buffid]')
        player = self.bot.gameManager.getPlayer(target.id)
        buff = buffFactory(buffID, player)
        player.applyBuffDebuff(buff)

    @commands.command()
    async def showEnemyList(self, ctx, *args):
        if ctx.message.author.id not in self.allowedIDs:
            await ctx.send('This is a developer command that you do not have access to :(',delete_after=10)
            return
        await ctx.send(f'{self.bot.gameManager.allEnemies}')