import enemies
import random
import discord
from discord.ext import commands, tasks
import asyncio


def setup(bot):
    bot.add_cog(combatCog(bot))
    print('Combat Cog Loaded')


class combatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = discord.utils.get(bot.guilds, name='intellectuals emote server')

    # This is how we display HP values in the combat embed as emotes.
    def convertIntToEmoj(self, number):
        num = abs(number)
        numchars = [int(d) for d in str(num)]
        output = ""
        for number in numchars:
            if number == 0:
                output += '0️⃣'
            if number == 1:
                output += '1️⃣'
            if number == 2:
                output += '2️⃣'
            if number == 3:
                output += '3️⃣'
            if number == 4:
                output += '4️⃣'
            if number == 5:
                output += '5️⃣'
            if number == 6:
                output += '6️⃣'
            if number == 7:
                output += '7️⃣'
            if number == 8:
                output += '8️⃣'
            if number == 9:
                output += '9️⃣'
        return output

    @commands.command(name='areas', aliases=['zones', 'Areas', 'Zones', 'araes', 'Araes'])
    async def areas(self, ctx, *args):
        if not args:
            embed = discord.Embed(title=f"Monster Areas",
                                  description=f'Area Name (Combat Level Range) - Area ID',
                                  color=0xd25151)
            embed.set_thumbnail(url='https://oldschool.runescape.wiki/images/Postbag_from_the_Hedge_-_Goblins%2C_globes_and_golems%21.jpg?4891f')
            embed.add_field(name=f'Zones', value=f'Around Limbrudge (1 - 43) - 1\n'
                                                 f'Blood Gulch (3 - 82) - 2\n'
                                                 f'Jawson Bog (16 - 102) - 3\n'
                                                 f'Fountain (22 - 107) - 4\n'
                                                 f'Innistrad (14- 94) - 5\n'
                                                 f'Katabatic (27 - 89) - 6\n'
                                                 f'Ishgard (30 - 100) - 7\n'
                                                 f'Baako\'s Grave (32 - 165) - 8\n'
                                                 f'Sandy Plains (29 - 161) - 9\n'
                                                 f'Partially Collapsed Chrome Tunnel (115 - ???) - 10', inline=True)
            embed.add_field(name=f'!areas [areaid] to see the monsters in that area!', value=f'\u200b', inline=False)
            await ctx.send(embed=embed, delete_after=30)
        else:
            try:
                area = int(args[0])
            except ValueError:
                await ctx.send(f'Bad args', delete_after=10)
                return
            if area > 0 and area < 11:
                if area == 1:
                    embed = discord.Embed(title=f"Around Limbrudge",
                                          description=f'Enemy Name (Combat Level) - ID: (ID)',
                                          color=0xd25151)
                    embed.set_thumbnail(url='https://oldschool.runescape.wiki/images/thumb/Lumbridge.png/300px-Lumbridge.png?d76b2')
                    embed.add_field(name=f'Monsters', value=f'Plant (1) - ID: 1\n'
                                                            f'Chicken (1) - ID: 7\n'
                                                            f'Cow (3) - ID: 4\n'
                                                            f'Bandit (3) - ID: 2\n'
                                                            f'Buff Rat (4) - ID: 3\n'
                                                            f'Farmer (6) - ID: 8\n'
                                                            f'Big Farmer (12) - ID: 9\n'
                                                            f'Master Farmer (43) - ID: 10\n'
                                                            f'Entrepeneur (20) - ID: 24\n'
                                                            f'Momma Chicken (39) - ID: 36\n', inline=True)
                    await ctx.send(embed=embed, delete_after=30)
                if area == 2:
                    embed = discord.Embed(title=f"Blood Gulch",
                                          description=f'Enemy Name (Combat Level) - ID: (ID)',
                                          color=0xd25151)
                    embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/en/4/49/Blood_Gulch.png')
                    embed.add_field(name=f'Monsters', value=f'Goblin (3) - ID: 5\n'
                                                            f'Goblin Miner (5) - ID: 6\n'
                                                            f'Ranged Goblin (7) - ID: 20\n'
                                                            f'Bat (22) - ID: 25\n'
                                                            f'Defiler (42) - ID: 37\n'
                                                            f'Zombom (44) - ID:38\n'
                                                            f'Big Bat (45) - ID: 40\n'
                                                            f'Warwelf (60) - ID: 48\n'
                                                            f'Stone Snake (66) - ID: 51\n'
                                                            f'Terrordog (82) - ID: 62\n', inline=True)
                    await ctx.send(embed=embed, delete_after=30)
                if area == 3:
                    embed = discord.Embed(title=f"Jawson Bog",
                                          description=f'Enemy Name (Combat Level) - ID: (ID)',
                                          color=0xd25151)
                    embed.set_thumbnail(url='https://scentofagamer.files.wordpress.com/2020/01/johnavon_unstableswamp.jpg')
                    embed.add_field(name=f'Monsters', value=f'River Troll (16) - ID: 23\n'
                                                            f'Green River Troll (35) - ID:35\n'
                                                            f'Moss Giant (42) - ID: 18\n'
                                                            f'Brawler (51) - ID: 41\n'
                                                            f'Durid (63) - ID: 49\n'
                                                            f'Shaman (93) - ID: 69\n'
                                                            f'Frogeel (102) - ID: 73', inline=True)
                    await ctx.send(embed=embed, delete_after=30)
                if area == 4:
                    embed = discord.Embed(title=f"Fountain",
                                          description=f'Enemy Name (Combat Level) - ID: (ID)',
                                          color=0xd25151)
                    embed.set_thumbnail(url='http://4.bp.blogspot.com/-8RUKPwqD4s8/VLYdpEPYEGI/AAAAAAAAADs/VU6GaJb_cY4/s1600/b-r5rb-ships.jpg')
                    embed.add_field(name=f'Monsters', value=f'Crab (22) - ID: 14\n'
                                                            f'Big Crab (30) - ID: 15\n'
                                                            f'Hill Giant (32) - ID: 17\n'
                                                            f'Tentacle (14) - ID: 22\n'
                                                            f'Terrorbird (27) - ID: 28\n'
                                                            f'Pirate (34) - ID: 32\n'
                                                            f'First Mate (64) - ID: 50\n'
                                                            f'Pirate Captain (82) - ID: 63\n'
                                                            f'Pirate Lord (103) - ID: 74\n'
                                                            f'Giant Enemy Crab (107) - ID: 16\n', inline=True)
                    await ctx.send(embed=embed, delete_after=30)
                if area == 5:
                    embed = discord.Embed(title=f"Innistrad",
                                          description=f'Enemy Name (Combat Level) - ID: (ID)',
                                          color=0xd25151)
                    embed.set_thumbnail(url='https://media.magic.wizards.com/images/featured/Planes_Innistrad_Preloader.jpg')
                    embed.add_field(name=f'Monsters', value=f'Zombo (14) - ID: 12\n'
                                                            f'Skelington (21) - ID: 11\n'
                                                            f'Ghost (22) - ID: 13\n'
                                                            f'Big Zombo (34) - ID: 34\n'
                                                            f'Mushroom (54) - ID: 43\n'
                                                            f'Strange Experiment (56) - ID: 46\n'
                                                            f'Corrupted Goo (69) - ID: 52\n'
                                                            f'Zombie Bruiser (71) - ID: 57\n'
                                                            f'Beholder (90) - 66\n'
                                                            f'Twisted Experiment (93) - ID: 70\n', inline=True)
                    await ctx.send(embed=embed, delete_after=30)
                if area == 6:
                    embed = discord.Embed(title=f"Katabatic",
                                          description=f'Enemy Name (Combat Level) - ID: (ID)',
                                          color=0xd25151)
                    embed.set_thumbnail(url='https://static.wikia.nocookie.net/tribes/images/e/e1/Katabatic-wide.jpg/revision/latest?cb=20120403030449')
                    embed.add_field(name=f'Monsters', value=f'Frozen Archer (27) - ID: 27\n'
                                                            f'Bear (34) - ID: 33\n'
                                                            f'Sandraker (44) - ID: 39\n'
                                                            f'Frozen Mammoth (58) - ID:47\n'
                                                            f'Ice Monster (75) - ID: 59\n'
                                                            f'Aviansie (80) - ID: 61\n'
                                                            f'Ice Troll (89) - ID: 65\n', inline=True)
                    await ctx.send(embed=embed, delete_after=30)
                if area == 7:
                    embed = discord.Embed(title=f"Ishgard",
                                          description=f'Enemy Name (Combat Level) - ID: (ID)',
                                          color=0xd25151)
                    embed.set_thumbnail(url='https://static.wikia.nocookie.net/finalfantasy/images/1/1c/Ishgard.jpg/revision/latest?cb=20120228154223')
                    embed.add_field(name=f'Monsters', value=f'Squire (30) - ID: 19\n'
                                                            f'Steel Knight (12) - ID: 21\n'
                                                            f'Black Knight (23) - ID: 26'
                                                            f'Mithril Knight (33) - ID: 31\n'
                                                            f'Spider (51) - ID: 42\n'
                                                            f'Vampire (56) - ID: 44\n'
                                                            f'Adamant Knight (69) - ID: 53\n'
                                                            f'Wandering Bard (69) - ID: 54\n'
                                                            f'Assassin (86) - ID: 64\n'
                                                            f'Evil Spider (90) - ID: 67\n'
                                                            f'Rune Knight (100) - ID: 72\n', inline=True)
                    await ctx.send(embed=embed, delete_after=30)
                if area == 8:
                    embed = discord.Embed(title=f"Baako\'s Grave",
                                          description=f'Enemy Name (Combat Level) - ID: (ID)',
                                          color=0xd25151)
                    embed.set_thumbnail(url='https://www.mmobomb.com/file/2011/03/bloodline-champions.jpg')
                    embed.add_field(name=f'Monsters', value=f'Wizard (32) - ID: 30\n'
                                                            f'Master Wizard (56) - ID: 45\n'
                                                            f'Experienced Mage (71) - ID: 56\n'
                                                            f'Lesser Demon (74) - ID: 58\n'
                                                            f'Greater Demon (100) - ID: 71\n'
                                                            f'Dark Mage (108) - ID: 76\n'
                                                            f'Alchemist (145) - ID: 83\n'
                                                            f'Inquisitor (165) - ID: 81', inline=True)
                    await ctx.send(embed=embed, delete_after=30)
                if area == 9:
                    embed = discord.Embed(title=f"Sandy Plains",
                                          description=f'Enemy Name (Combat Level) - ID: (ID)',
                                          color=0xd25151)
                    embed.set_thumbnail(url='https://static.wikia.nocookie.net/monsterhunter/images/3/33/Desert-Area9.jpg/revision/latest?cb=20100210040119')
                    embed.add_field(name=f'Monsters', value=f'Mummy (29) - ID: 29\n'
                                                            f'Valkyrie (71) - ID: 55\n'
                                                            f'Green Dragon (79) - ID: 60\n'
                                                            f'Blue Dragon (90) - ID:68\n'
                                                            f'Red Dragon (106) - ID:75\n'
                                                            f'Necromancer (110) - ID: 77\n'
                                                            f'Black Dragon (120) - ID: 79\n'
                                                            f'Diablos (161) - ID: 80\n', inline=True)
                    await ctx.send(embed=embed, delete_after=30)
                if area == 10:
                    embed = discord.Embed(title=f"Partially Collapsed Chrome Tunnel",
                                          description=f'Enemy Name (Combat Level) - ID: (ID)',
                                          color=0xd25151)
                    embed.set_thumbnail(url='https://ichef.bbci.co.uk/news/1024/media/images/62484000/jpg/_62484134_tunnel_pic.jpg')
                    embed.add_field(name=f'Monsters', value=f'Bandit Leader (115) - ID: 78\n'
                                                            f'Archmystic (171) - ID: 82\n'
                                                            f'Fire Spirit (250) - ID 84\n'
                                                            f'Musk (???) - ID: 85', inline=True)
                    await ctx.send(embed=embed, delete_after=30)
            else:
                await ctx.send(f'Could not find that area ID)', delete_after=10)
        await ctx.message.delete()


    @commands.command(aliases=['Fight', 'battle', 'Battle', 'fihgt', 'Fihgt'])
    async def fight(self, ctx, *args):
        if not args:
            await ctx.send(f'Please provide arguments for this command (Enemy ID)', delete_after=15)
            return
        try:
            ID = int(args[0])
        except ValueError:
            await ctx.send(f'Please provide the enemies numeric ID', delete_after=15)
            return
        try:
            loops = int(args[1])
        except IndexError:
            loops = 1
        ogLoops = loops
        player = self.bot.gameManager.getPlayer(ctx.message.author.id)
        while loops > 0 and player.playerCurrentHP > 0 and not player.cancelBool:
            enemy = self.spawnEnemy(ID)
            await self.doCombat(player, enemy, ctx)
            self.bot.gameManager.allEnemies.remove(enemy)
            loops -= 1
        await ctx.message.delete()
        player.cancelBool = False
        if loops == 0:
            await ctx.send(f'{ctx.message.author.display_name.capitalize()} finished fighting {ogLoops} enemies!',
                           delete_after=30)

    # Spawns an enemy from the enemyFactory class, and sticks them in the game manager's list of enemies to be managed.
    def spawnEnemy(self, ID):
        enemy = enemies.enemyFactory(ID)
        self.bot.gameManager.allEnemies.append(enemy)
        return enemy

    # Given a bunch of information from the combat loop, creates an embed to be displayed for each combat step.
    def buildCombatEmbed(self, player, enemy, combatTick, playerText, enemyText, addComText, ctx):
        enemyHPBar = enemy.hitpointsDisplay()
        playerHPBar = player.hitpointsDisplay()
        embed = discord.Embed(title=f'{"💚" * enemyHPBar}{"🟥" * (20 - enemyHPBar)}',
                              description=f"**{enemy.enemyName}**\n"
                                          f"```{enemy.enemyDesc}```", color=0xd25151)
        embed.set_thumbnail(url=enemy.enemyImgURL)
        embed.add_field(name=f'Combat Duration', value=f'{round(combatTick, 2)}s', inline=True)
        ebuffMessage = "\u200b"
        eBuffs = enemy.readBuffs()
        for buff in eBuffs:
            ebuffMessage += f'{buff}: {round(int(eBuffs[buff]) * 0.6, 2)}s\n'
        embed.add_field(name=f'{enemy.enemyName} Buffs: ', value=f'{ebuffMessage}', inline=True)
        embed.add_field(name=f'{enemy.enemyName} HP: ', value=f'{self.convertIntToEmoj(enemy.enemyCurrentHP)}',
                        inline=True)
        embed.add_field(name=f'Combat Text',
                        value=f'{playerText}\n'
                              f'{enemyText}\n' + addComText,
                        inline=False)

        try:
            playerFoodAmt = player.playerInventory[str(player.playerFood)]
        except KeyError:
            playerFoodAmt = 0
        try:
            playerFood = self.bot.gameManager.itemIDToItem(player.playerFood).itemName
        except AttributeError:
            playerFood = 'None'
        embed.add_field(name=f'{ctx.message.author.display_name.capitalize()} Food',
                        value=f'{playerFood} ({playerFoodAmt})',
                        inline=True)
        pbuffMessage = "\u200b"
        pBuffs = player.readBuffs()
        for buff in pBuffs:
            pbuffMessage += f'{buff}: {round(int(pBuffs[buff]) * 0.6, 2)}s\n'
        embed.add_field(name=f'{ctx.message.author.display_name.capitalize()} Buffs: ', value=f'{pbuffMessage}',
                        inline=True)
        embed.add_field(name=f'{ctx.message.author.display_name.capitalize()} HP: ',
                        value=f'{self.convertIntToEmoj(player.playerCurrentHP)}',
                        inline=True)
        embed.add_field(name=f'{ctx.message.author.display_name}',
                        value=f'{"💚" * playerHPBar}{"🟥" * (20 - playerHPBar)}', inline=False)
        return embed

    # The main combat loop. Honestly, here be dragons. I have lived for days in this function alone, and it contains
    # bits and pieces from ways that I learned to do things 3 weeks ago that I now do differently, etc.
    async def doCombat(self, player, enemy, ctx):
        if player.inCombat:
            await ctx.send(f'You are already in combat!')
            return
        player.inCombat = True
        player.playerAttackDelay = 0
        combatTick = 0.0
        enemyAttackTick = 0
        if player.playerCurrentHP > 0 and enemy.enemyCurrentHP > 0 and not player.cancelBool:
            # IF A PLAYER HAS A SPECIAL ATTACK, A COMMAND CAN FLIP A FLAG THAT MAKES THE PLAYER CHOOSE THAT FUNCTION INSTEAD OF A NORMAL HIT
            playerDMG, playerText = player.calculateAttackOnEnemy(enemy)
            playerDMG = min(playerDMG, enemy.enemyCurrentHP)
            enemyDMG, enemyText = enemy.calculateAttackOnPlayer(player)
            enemyDMG = min(enemyDMG, player.playerCurrentHP)
            enemy.changeEnemyHP(-playerDMG)
            player.playerAttackDelay = player.changeAttackDelay(player.getAttackSpeed())
            baseExp = playerDMG
            xpGained, leveledUp = player.givePlayerExperience("maxhp", baseExp)
            if leveledUp:
                # User gained an HP level!
                await ctx.send(embed=leveledUp, delete_after=300)
            xpGained, leveledUp = player.givePlayerExperience(player.playerCombatStyle, baseExp * 4)
            if leveledUp:
                # User gained a level in their combat style!
                await ctx.send(embed=leveledUp, delete_after=300)
            addComText = player.changePlayerHP(-enemyDMG)
            enemyAttackTick = enemy.getEnemyAtkSpeed()
            embed = self.buildCombatEmbed(player, enemy, combatTick, playerText, enemyText, addComText, ctx)
            message = await ctx.send(embed=embed)
            await asyncio.sleep(0.6)
            combatTick += 0.6
        else:
            print(f'Idk how, but one of these things had 0 hp when combat started.')

        while player.playerCurrentHP > 0 and enemy.enemyCurrentHP > 0 and not player.cancelBool:
            player.changeAttackDelay(-1)
            player.changeEatDelay(-1)
            enemyAttackTick -= 1
            combatTick += 0.6

            if player.playerAttackDelay == 0 and enemyAttackTick == 0:
                playerDMG, playerText = player.calculateAttackOnEnemy(enemy)
                playerDMG = min(playerDMG, enemy.enemyCurrentHP)
                enemyDMG, enemyText = enemy.calculateAttackOnPlayer(player)
                enemyDMG = min(enemyDMG, player.playerCurrentHP)
                enemy.changeEnemyHP(-playerDMG)
                player.playerAttackDelay = player.changeAttackDelay(player.getAttackSpeed())
                baseExp = playerDMG
                xpGained, leveledUp = player.givePlayerExperience("maxhp", baseExp)
                if leveledUp:
                    # User gained an HP level!
                    await ctx.send(embed=leveledUp, delete_after=300)

                xpGained, leveledUp = player.givePlayerExperience(player.playerCombatStyle, baseExp * 4)
                if leveledUp:
                    # User gained a level in their combat style!
                    await ctx.send(embed=leveledUp, delete_after=300)
                addComText = player.changePlayerHP(-enemyDMG)
                enemyAttackTick = enemy.getEnemyAtkSpeed()
                embed = self.buildCombatEmbed(player, enemy, combatTick, playerText, enemyText, addComText, ctx)
                await message.edit(embed=embed)

            elif player.playerAttackDelay == 0:
                playerDMG, playerText = player.calculateAttackOnEnemy(enemy)
                playerDMG = min(playerDMG, enemy.enemyCurrentHP)
                enemy.changeEnemyHP(-playerDMG)
                player.playerAttackDelay = player.changeAttackDelay(player.getAttackSpeed())
                baseExp = playerDMG
                xpGained, leveledUp = player.givePlayerExperience("maxhp", baseExp)
                if leveledUp:
                    # User gained an HP level!
                    await ctx.send(embed=leveledUp, delete_after=300)
                xpGained, leveledUp = player.givePlayerExperience(player.playerCombatStyle, baseExp * 4)
                if leveledUp:
                    # User gained a level in their combat style!
                    await ctx.send(embed=leveledUp, delete_after=300)
                enemyText = '\u200b'
                addComText = '\u200b'
                embed = self.buildCombatEmbed(player, enemy, combatTick, playerText, enemyText, addComText, ctx)
                await message.edit(embed=embed)
            elif enemyAttackTick == 0:
                enemyDMG, enemyText = enemy.calculateAttackOnPlayer(player)
                enemyDMG = min(enemyDMG, player.playerCurrentHP)
                addComText = player.changePlayerHP(-enemyDMG)
                enemyAttackTick = enemy.getEnemyAtkSpeed()
                playerText = '\u200b'

                embed = self.buildCombatEmbed(player, enemy, combatTick, playerText, enemyText, addComText, ctx)
                await message.edit(embed=embed)
            await asyncio.sleep(0.6)

        await asyncio.sleep(2)
        if player.playerCurrentHP <= 0 and enemy.enemyCurrentHP <= 0:
            print(f'Double kill! {player.DiscordID} and {enemy.enemyName} slay each other in combat on the same turn!')
            embed = enemy.handleLoot(player)
            e = await ctx.send(embed=embed, delete_after=20)
            l = player.onDeath()
            await ctx.send(f'Oh dear, <@!{player.DiscordID}>, you are dead!\n'
                           f'You lose {l} Scrip!')
        elif enemy.enemyCurrentHP <= 0:
            embed = enemy.handleLoot(player)
            e = await ctx.send(embed=embed, delete_after=20)
        elif player.playerCurrentHP <= 0:
            print(f'{player.DiscordID} is slain by {enemy.enemyName}')
            l = player.onDeath()
            await ctx.send(f'Oh dear, <@!{player.DiscordID}>, you are dead!\n'
                           f'You lose {l} Scrip!')
        else:
            if player.cancelBool:
                b = await ctx.send(f'<@!{player.DiscordID}> ran away!', delete_after=10)
        player.inCombat = False
        await message.delete()
