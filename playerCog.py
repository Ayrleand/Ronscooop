# This is where all of the interaction between players and their player objects will take place. Commands for users
# to check any aspect of their character, in addition to some actual interaction.

import random
import discord
from discord.ext import commands, tasks
import asyncio

from playground import Items



def setup(bot):
    bot.add_cog(playerCog(bot))
    print('Player Interaction Cog Loaded')


class playerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = discord.utils.get(bot.guilds, name='intellectuals emote server')

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
    async def buyPet(self, ctx, *args):
        player = self.bot.gameManager.getPlayer(ctx.message.author.id)
        playerPets = player.getPets()
        cost = 20000000
        if not args:
            embed = discord.Embed(title=f"The Pet Store",
                                  description=f'Pets cost 20,000,000 Scrip!',
                                  color=0xd25151)
            embed.add_field(name=f'BudChest', value=f'<:BudChest:891123380424695828>', inline=True)
            embed.add_field(name=f'LibChest', value=f'<:LibChest:898039850253553704>', inline=True)
            embed.add_field(name=f'BitChest', value=f'<:BitChest:901309135239389215>', inline=True)
            embed.add_field(name=f'DeBatChest', value=f'<:DeBatChest:891908362650935327>', inline=True)
            embed.add_field(name=f'SpookyChest', value=f'<:SpookyChest:900175097355198465>', inline=True)
            embed.add_field(name=f'ChudChest', value=f'<:ChudChest:893678223391612989>', inline=True)
            embed.add_field(name=f'CopChest', value=f'<:CopChest:903682087113097276>', inline=True)
            embed.add_field(name=f'ElonChest', value=f'<:ElonChest:904541364899938404>', inline=True)
            embed.add_field(name=f'TankChest', value=f'<:TankChest:904475431409950802>', inline=True)
            embed.add_field(name=f'WeebChest', value=f'<:WeebChest:907400408035631144>', inline=True)
            await ctx.send(embed=embed, delete_after=60)
            await ctx.message.delete()
        else:
            if args[0].upper() in ['BUDCHEST', 'LIBCHEST', 'BITCHEST', 'CHUDCHEST', 'SPOOKYCHEST', 'DEBATCHEST',
                                                              'ELONCHEST', 'WEEBCHEST', 'TANKCHEST', 'COPCHEST']:
                if player.playerScrip >= cost and args[0].upper() not in playerPets:
                    m = player.addPet(args[0])
                    player.changeScrip(-cost)
                    await ctx.send(f'{m}', delete_after=30)
                    await ctx.message.delete()
                else:
                    await ctx.send(f'You do not have enough Scrip to buy that pet, or you already have that pet!', delete_after=15)
                    await ctx.message.delete()
            else:
                await ctx.send(f'Unrecognized pet name!', delete_after=15)
                await ctx.message.delete()
    @commands.command(aliases=['pest', 'Pets', 'pet'])
    async def pets(self, ctx):
        player = self.bot.gameManager.getPlayer(ctx.message.author.id)
        playerPets = player.getPets()
        embed = discord.Embed(title=f"{ctx.message.author.display_name.capitalize()}\'s Pets",
                              description=f'\u200b',
                              color=0xd25151)
        embed.set_thumbnail(url='https://oldschool.runescape.wiki/images/thumb/Nature_house_built.png/200px-Nature_house_built.png?d10b4')
        m = "\u200b"
        for pet in playerPets:
            if pet == 'BUDCHEST':
                m += '<:BudChest:891123380424695828>, '
            if pet == 'LIBCHEST':
                m += '<:LibChest:898039850253553704>, '
            if pet == 'BITCHEST':
                m += '<:BitChest:901309135239389215>, '
            if pet == 'DEBATCHEST':
                m += '<:DeBatChest:891908362650935327>, '
            if pet == 'SPOOKYCHEST':
                m += '<:SpookyChest:900175097355198465>, '
            if pet == 'CHUDCHEST':
                m += '<:ChudChest:893678223391612989>, '
            if pet == 'COPCHEST':
                m += '<:CopChest:903682087113097276>, '
            if pet == 'ELONCHEST':
                m += '<:ElonChest:904541364899938404>, '
            if pet == 'TANKCHEST':
                m += '<:TankChest:904475431409950802>, '
            if pet == 'WEEBCHEST':
                m += '<:WeebChest:907400408035631144>, '
        embed.add_field(name=f'\u200b', value=f'{m}', inline=False)
        await ctx.send(embed=embed, delete_after=60)
        await ctx.message.delete()

    @commands.command(aliases= ['boostInventory', 'maxSize', 'expand', 'expandInventory', 'epxand', 'increaseinventory', 'incraeseInvenroy'])
    async def increaseInventory(self, ctx):
        player = self.bot.gameManager.getPlayer(ctx.message.author.id)
        if player.playerMaxInventory > 100:
            await ctx.send(f'You have reached the maximum amount of inventory space!')
        cost = 20000 + (player.playerMaxInventory - 20)*10000
        message = await ctx.send(
            f'{ctx.message.author.display_name} currently has an inventory size of {player.playerMaxInventory}.\n'
            f'Would you like to spend {cost} Scrip to increase this by one?')
        await message.add_reaction('\N{THUMBS UP SIGN}')
        def reactUserCheck(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in '\N{THUMBS UP SIGN}'

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=reactUserCheck)
        except asyncio.TimeoutError:
            await ctx.message.delete()
            await message.edit(content=f'Request timed out!')
            await asyncio.sleep(3)
            await message.delete()
            return
        if player.playerScrip >= cost:
            await ctx.message.delete()
            inv = player.changeMaxInvt(1)
            player.changeScrip(-cost)
            await message.edit(content=f'Expanded your inventory! {ctx.message.author.display_name} now has an inventory size of {inv}!')
            await asyncio.sleep(3)
            await message.delete()

        else:
            await ctx.message.delete()
            await message.edit(content=f'Sorry, you don\'t have {cost} Scrip to spend!')
            await asyncio.sleep(3)
            await message.delete()



    @commands.command(aliases=['showcancel', 'amicancel', 'showcanecl'])
    async def showCancel(self, ctx):
        player = self.bot.gameManager.getPlayer(ctx.message.author.id)
        m = await ctx.send(f'{player.cancelBool}')
        await asyncio.sleep(10)
        await m.delete()
        await ctx.message.delete()

    @commands.command(aliases=['pitch', 'alch', 'slel', 'slle', 'Sell', 'Slel'])
    async def sell(self, ctx, *args):
        if args:
            player = self.bot.gameManager.getPlayer(ctx.message.author.id)
            item = self.inputToItem(args[0])
            if player.checkInventory(item):
                amount = int(player.playerInventory[f'{item.ID}'])
                try:
                    amount = int(args[1])
                except IndexError:
                    pass
                sellValue = amount * int(item.alchValue)
                m = await ctx.send(f'You are about to sell {amount} {item.itemName} for {sellValue}, is that cool?')
                reacts = ['✅','❌']
                await m.add_reaction('✅')
                await m.add_reaction('❌')

                def reactUserCheck(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) in reacts

                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=reactUserCheck)
                except asyncio.TimeoutError:
                    await ctx.send(f'{ctx.message.author.display_name} did not accept in time.')
                    await m.delete()
                    return
                if str(reaction) == reacts[0]:
                    player.addToInventory(item.ID, -amount)
                    n = player.changeScrip(sellValue)
                    r = await ctx.send(
                        f'{ctx.message.author.display_name} sold {amount} {item.itemName} for {sellValue}, they now have {n} Scrip!')
                    await asyncio.sleep(3)
                    await r.delete()
                    await ctx.message.delete()
                await m.delete()
                return
            else:
                r = await ctx.send(f'You do not have any of those!')
                await asyncio.sleep(3)
                await r.delete()
                await ctx.message.delete()
                return
        else:
            r = await ctx.send(f'Please provide some arguments for this command. Syntax: !sell [item] [amount]')
            await asyncio.sleep(5)
            await r.delete()
            await ctx.message.delete()
            return

    @commands.command(aliases=['equip', 'wear', 'puton', 'equipitem', 'EquipItem', 'eqiupItem', 'eqiupitem', 'eqiup', 'euqip'])
    async def equipItem(self, ctx, *args):
        player = self.bot.gameManager.getPlayer(ctx.message.author.id)
        if args:
            item = self.inputToItem(args[0])
            mText = player.equipItem(item)
            r = await ctx.send(f'{mText}')
            await asyncio.sleep(5)
            await ctx.message.delete()
            await r.delete()
        else:
            embed = discord.Embed(title=f'{ctx.message.author.display_name.capitalize()} Equippable Items',
                                  description=f"**Item Name / Item ID**", color=0xd25151)
            embed.set_thumbnail(url=ctx.message.author.avatar_url)
            equipList = "\u200b"
            for item in player.playerInventory:
                exItem = self.bot.gameManager.itemIDToItem(int(item))
                try:
                    if exItem.equipmentStats:
                        equipList += f'{exItem.itemName} / {exItem.ID}, Reqs: {exItem.equipmentReqs}\n'
                except AttributeError:
                    pass
            embed.add_field(name=f'(Remember !equip hates spaces)', value=f'{equipList}', inline=True)
            r = await ctx.send(embed=embed)
            await asyncio.sleep(60)
            await r.delete()
            await ctx.message.delete()


    @commands.command(aliases=['run', 'cabcek', 'Cancel', 'cacnel', 'vanvel', 'vancel', 'Vancel', 'Vanvel'])
    async def cancel(self, ctx, *args):
        player = self.bot.gameManager.getPlayer(ctx.message.author.id)
        player.cancelBool = True
        player.inCombat = False
        await asyncio.sleep(3)
        await ctx.message.delete()

    @commands.command(name='food', aliases = ['pickfood', 'equipfood', 'choosefood', 'Food', 'Fodo', 'fodo', 'myfood'])
    async def food(self, ctx, *args):
        player = self.bot.gameManager.getPlayer(ctx.message.author.id)
        if not args:
            r = await ctx.send(f'Please provide some arguments for this command. Argument should be an item ID or name without spaces.')
            await asyncio.sleep(5)
            await r.delete()
            await ctx.message.delete()
            return
        item = self.inputToItem(args[0])

        if player.checkInventory(item):
            try:
                if "heal" in item.itemEffects:
                    player.changeFood(item.ID)
                    r = await ctx.send(f'{ctx.message.author.display_name.capitalize()} chooses {item.itemName} as their food!')
                    await asyncio.sleep(10)
                    await r.delete()
                    await ctx.message.delete()
                else:
                    await ctx.send(f'Please pick a food!', delete_after=10)
            except AttributeError:
                r = await ctx.send(f'That item is not a consumable!')
                await asyncio.sleep(10)
                await r.delete()
                await ctx.message.delete()
        else:
            r = await ctx.send(f'You do not have that item!')
            await asyncio.sleep(10)
            await r.delete()
            await ctx.message.delete()


    @commands.command(aliases=['Style', 'combatstyle', 'changestyle', 'stlye', 'attackstyle', 'Stlye'])
    async def style(self, ctx, *args):
        styles = ["attack", "strength", "defence"]
        player = self.bot.gameManager.getPlayer(ctx.message.author.id)
        if args:
            if player.playerCombatStyle in ['ranged', 'magic']:
                await ctx.send(f'You can only change your combat style while using a melee weapon!', delete_after=10)
                await asyncio.sleep(10)
                await ctx.message.delete()
                return
            if args[0].lower() in styles:
                player.playerCombatStyle = args[0].lower()
                r = await ctx.send(f'{ctx.message.author.display_name} changed to training {args[0].lower()}.')
                await asyncio.sleep(10)
                await r.delete()
                await ctx.message.delete()
        else:
            r = await ctx.send(f'{ctx.message.author.display_name.capitalize()} Attack Style: {player.playerCombatStyle}')
            await asyncio.sleep(10)
            await r.delete()
            await ctx.message.delete()

    @commands.command(name='stats', aliases=['checkGearStats', 'Stats', 'sttas', 'Sttas', 'ststs', 'equipstats'])
    async def stats(self, ctx, *args):
        embed = discord.Embed(title=f"{ctx.message.author.display_name} Equipment Stats", description="",
                              color=0xd25151)
        player = self.bot.gameManager.getPlayer(ctx.message.author.id)
        embed.add_field(name=f'Attack Speed', value=f'{player.getAttackSpeed()}', inline=False)
        embed.add_field(name=f'Melee Atk', value=f'{player.playerMeleeAtk}', inline=True)
        embed.add_field(name=f'Range Atk', value=f'{player.playerRangeAtk}', inline=True)
        embed.add_field(name=f'Mage Atk', value=f'{player.playerMageAtk}', inline=True)
        embed.add_field(name=f'Melee Str', value=f'{player.playerMeleeStr}', inline=True)
        embed.add_field(name=f'Range Str', value=f'{player.playerRangeStr}', inline=True)
        embed.add_field(name=f'Mage Str', value=f'{player.playerMageStr}', inline=True)
        embed.add_field(name=f'Melee Def', value=f'{player.playerMeleeDef}', inline=True)
        embed.add_field(name=f'Range Def', value=f'{player.playerRangeDef}', inline=True)
        embed.add_field(name=f'Mage Def', value=f'{player.playerMageDef}', inline=True)
        r = await ctx.send(embed=embed)
        await asyncio.sleep(60)
        await r.delete()
        await ctx.message.delete()

    @commands.command(name='gear', aliases=['equipment', 'wearing', 'armor', 'equips', 'Gear', 'gaer', 'Gaer'])
    async def gear(self, ctx):
        embed = discord.Embed(title=f"{ctx.message.author.display_name.capitalize()} Gear", description="", color=0xd25151)
        player = self.bot.gameManager.getPlayer(ctx.message.author.id)
        embed.set_thumbnail(url= 'https://oldschool.runescape.wiki/images/Worn_equipment_tab.png?c4bec')
        leftM= []
        for slot in player.playerEquipment:
            item = self.bot.gameManager.itemIDToItem(player.playerEquipment[f'{slot}'])
            if item:
                leftM.append(item.itemName)
            else:
                leftM.append(f'None')

        embed.add_field(name=f'Left', value=f'Main Hand: {leftM[5]}\n'
                                            f'Head: {leftM[0]}\n'
                                            f'Body: {leftM[1]}\n'
                                            f'Gloves: {leftM[4]}\n'
                                            f'Legs: {leftM[2]}\n'
                                            f'Feet: {leftM[3]}\n', inline=True)

        embed.add_field(name=f'Right', value=f'Off Hand: {leftM[6]}\n'
                                            f'Neck: {leftM[8]}\n'
                                            f'Back: {leftM[7]}\n'
                                            f'Ring 1: {leftM[10]}\n'
                                            f'Ring 2: {leftM[11]}\n'
                                            f'Ammo: {leftM[9]}\n', inline=True)
        r = await ctx.send(embed=embed)
        await asyncio.sleep(60)
        await r.delete()
        await ctx.message.delete()


        # for slot in player.playerEquipment:
        #     item = self.bot.gameManager.itemIDToItem(player.playerEquipment[f'{slot}'])
        #     if item:
        #         embed.add_field(name=f'{slot.upper()}', value=f'{item.itemName}', inline=True)
        #     else:
        #         embed.add_field(name=f'{slot.upper()}', value=f'\u200b', inline=True)
        # await ctx.send(embed=embed)

    @commands.command(name='inventory', aliases=['items', 'stuff', 'myshit', 'ivnetnory', 'ivnentory', 'bag', 'Inventory', 'Ivnetory'])
    async def inventory(self, ctx):
        player = self.bot.gameManager.getPlayer(ctx.message.author.id)
        embed = discord.Embed(title=f"{ctx.message.author.display_name.capitalize()}\'s Inventory",
                              description=f'{len(player.playerInventory)} / {player.playerMaxInventory}, Scrip: {player.playerScrip}',
                              color=0x620674)
        embed.set_thumbnail(url='https://oldschool.runescape.wiki/images/thumb/Looting_bag_detail.png/155px-Looting_bag_detail.png?1bf07')
        playerInvPages = 1 + int(len(player.playerInventory)/20)

        x = 0
        iterable = iter(player.playerInventory.items())
        for i in range(playerInvPages):
            m = "\u200b"
            for z in range(20):
                try:
                    ID, count = next(iterable)
                except StopIteration:
                    break
                x = self.bot.gameManager.itemIDToItem(int(ID))
                m += f'**{x.itemName}: {count}** *(ID: {x.ID})*\n'
                if z >= 20:
                    break
            embed.add_field(name=f'Page {i+1}', value=m, inline=True)
        await ctx.send(embed=embed, delete_after=60)
        await ctx.message.delete()

    @commands.command(name='skills', aliases=["levels", 'skillsheet', 'Skills', 'Levels', 'MySkills', 'myskills', 'sklils', 'sikls'])
    # Takes in the dictionary returned by player.getSkills and parses it into an embed message.
    async def skills(self, ctx, *args):
        embed = discord.Embed(title=f"{ctx.message.author.display_name.capitalize()}\'s Skills", description="",
                              color=0xd25151)
        player = self.bot.gameManager.getPlayer(ctx.message.author.id)
        stats = player.getSkills()
        for name in stats:
            embed.add_field(name=f'{name}', value=f'{stats[name]}', inline=True)
        r = await ctx.send(embed=embed)
        await asyncio.sleep(30)
        await r.delete()
        await ctx.message.delete()

    @commands.command(name='skill', aliases=['skillDetail', 'checkSkill', 'Skill', 'sikll', 'slikl'])
    async def skill (self, ctx, *args):
        player = self.bot.gameManager.getPlayer(ctx.message.author.id)
        try:
            skill = args[0]
        except IndexError:
            r = await ctx.send(f'Please provide a skill name to check!')
            await asyncio.sleep(10)
            await r.delete()
            await ctx.message.delete()
            return
        currentExp, currentLevel, currentNexLevel = player.getSkill(skill)
        embed = discord.Embed(title=f"{ctx.message.author.display_name.capitalize()} {skill.capitalize()}", description="",
                              color=0xd25151)
        embed.add_field(name=f'Current Level: ', value=f'{currentLevel}', inline=True)
        embed.add_field(name=f'Current Exp: ', value=f'{currentExp}', inline=True)
        if currentLevel < 99:
            embed.add_field(name=f'Exp for Next Level: ', value=f'{currentNexLevel}', inline=True)
        else:
            embed.add_field(name=f'Exp for Next Level: ', value=f'You\'re done! Congratulations!', inline=True)
        r = await ctx.send(embed=embed)
        await asyncio.sleep(10)
        await r.delete()
        await ctx.message.delete()


    @commands.command(name='scrip', aliases=['money', 'currency', 'cash', 'muns', 'Scrip', 'Money', 'scirp', 'Scirp', 'svrip', 'svip', 'Svrip'])
    async def scrip(self, ctx, *args):
        player = self.bot.gameManager.getPlayer(ctx.message.author.id)
        scrip = player.checkScrip()
        r = await ctx.send(f'{ctx.message.author.display_name.capitalize()} has {scrip} Scrip!')
        await asyncio.sleep(10)
        await r.delete()
        await ctx.message.delete()

    @commands.command()
    async def buffs(self, ctx, *args):
        player = self.bot.gameManager.getPlayer(ctx.message.author.id)
        message = "Buffs:\n"
        pBuffs = player.readBuffs()
        for buff in pBuffs:
            message+=f'{buff}: {int(pBuffs[buff]) * 0.6}s\n'
        r = await ctx.send(f'{message}')
        await asyncio.sleep(30)
        await r.delete()
        await ctx.message.delete()

    @commands.command(name='use', aliases=['eat', 'Use', 'Eat', 'u', 'e', 'ues', 'Ues', 'Eta', 'eta'])
    async def use(self, ctx, *args):
        if not args:
            r = await ctx.send(f'Please provide an item to use!')
            await asyncio.sleep(10)
            await r.delete()
            await ctx.message.delete()
            return
        player = self.bot.gameManager.getPlayer(ctx.message.author.id)
        item = self.inputToItem(args[0])
        try:
            a = item.use(player, player)
            await ctx.send(a, delete_after=3)
            await ctx.message.delete()
        except AttributeError:
            await ctx.send(f'Item is not a consumable!', delete_after=5)
            await ctx.message.delete()
            return




