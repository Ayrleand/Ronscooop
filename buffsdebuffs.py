import random
import asyncio
from abc import abstractmethod

def run_and_get(coro):
    task = asyncio.create_task(coro)
    asyncio.get_running_loop().run_until_complete(task)
    return task.result()

class Buff:
    def __init__(self, owner):
        self.owner = owner
        self.duration = 0
        self.name = ""
        self.id = 0
        self.onEnemy = False
        try:
            if not self.owner.isPlayer:
                self.onEnemy = True
        except AttributeError:
            self.onEnemy = True


    def onStart(self):
        # Override this with stuff to do at the start
        pass

    def onTick(self):
        self.duration -= 1
        if self.duration <= 0:
            self.onFinish()

    def onFinish(self):
        self.owner.buffs.remove(self)
        # Override this with stuff to do at the end

def buffFactory(ID, owner):
    # Buff and Debuff definitions
    class Fast1(Buff):
        def __init__(self, owner):
            super().__init__(owner)
            self.duration = 30
            self.name = "Go Fast"
            self.id = 1
            self.onStart()


        def onStart(self):
            print(f'{self.onEnemy}')
            if not self.onEnemy:
                self.owner.playerAtkSpeedMod = -1
            else:
                self.owner.enemyAtkSpdMod = -1


        def onFinish(self):
            if not self.onEnemy:
                self.owner.playerAtkSpeedMod = 0
            else:
                self.owner.enemyAtkSpdMod = 0
            self.owner.buffs.remove(self)

    class Regen1(Buff):
        def __init__(self, owner):
            super().__init__(owner)
            self.duration = 11
            self.name = "Regen 1"
            self.id = 2
            self.healTick = 0
            self.onStart()

        def onStart(self):
            self.owner.changePlayerHP(1)

        def onTick(self):
            self.duration -= 1
            self.healTick += 1
            if self.healTick == 2:
                self.owner.changePlayerHP(2)
                self.healTick = 0
            if self.duration <= 0:
                self.onFinish()


        def onFinish(self):
            self.owner.buffs.remove(self)

    class poisonOne(Buff):
        def __init__(self, owner):
            super().__init__(owner)
            self.duration = 11
            self.name = "Poison 1"
            self.id = 3
            self.healTick = 0
            self.onStart()

        def onStart(self):
            self.owner.changePlayerHP(0)

        def onTick(self):
            self.duration -= 1
            self.healTick += 1
            if self.healTick == 2:
                self.owner.changePlayerHP(-1)
                self.healTick = 0
            if self.duration <= 0:
                self.onFinish()

        def onFinish(self):
            self.owner.buffs.remove(self)

    class Slow1(Buff):
        def __init__(self, owner):
            super().__init__(owner)
            self.duration = 12
            self.name = "Chilled"
            self.id = 4
            self.onStart()

        def onStart(self):
            if not self.onEnemy:
                self.owner.playerAtkSpeedMod = 1
            else:
                self.owner.enemyAtkSpdMod = -1

        def onFinish(self):
            if not self.onEnemy:
                self.owner.playerAtkSpeedMod = 0
            else:
                self.owner.enemyAtkSpdMod = 0
            self.owner.buffs.remove(self)

    class AttackDebuff(Buff):
        def __init__(self, owner):
            super().__init__(owner)
            self.duration = 15
            self.name = "Inaccurate"
            self.id = 5
            self.onStart()

        def onStart(self):
            if not self.onEnemy:
                self.owner.playerCurrentAttack = (self.owner.playerMaxAttack - 5)

        def onFinish(self):
            if not self.onEnemy:
                self.owner.playerCurrentAttack = self.owner.playerMaxAttack
            self.owner.buffs.remove(self)

    class DefDown(Buff):
        def __init__(self, owner):
            super().__init__(owner)
            self.duration = 15
            self.name = "DEF Down"
            self.id = 6
            self.onStart()

        def onStart(self):
            if not self.onEnemy:
                self.owner.playerCurrentDefence = (self.owner.playerMaxDefence - 5)

        def onFinish(self):
            if not self.onEnemy:
                self.owner.playerCurrentDefence = self.owner.playerMaxDefence
            self.owner.buffs.remove(self)
            
    class StrDown(Buff):
        def __init__(self, owner):
            super().__init__(owner)
            self.duration = 15
            self.name = "DMG Down"
            self.id = 7
            self.onStart()

        def onStart(self):
            if not self.onEnemy:
                self.owner.playerCurrentStrength = (self.owner.playerMaxStrength - 5)
                self.owner.playerCurrentRanged = (self.owner.playerMaxRanged - 5)
                self.owner.playerCurrentMagic = (self.owner.playerCurrentMagic - 5)

        def onFinish(self):
            if not self.onEnemy:
                self.owner.playerCurrentStrength = self.owner.playerMaxStrength
                self.owner.playerCurrentRanged = self.owner.playerMaxRanged
                self.owner.playerCurrentMagic = self.owner.playerCurrentMagic
            try:
                self.owner.buffs.remove(self)
            except ValueError:
                pass

    # The big If for the factory
    if ID==1: return Fast1(owner)
    if ID==2: return Regen1(owner)
    if ID==3: return poisonOne(owner)
    if ID==4: return Slow1(owner)
    if ID==5: return AttackDebuff(owner)
    if ID==6: return DefDown(owner)
    if ID==7: return StrDown(owner)
    assert 0, f'Bad ID: {ID}'