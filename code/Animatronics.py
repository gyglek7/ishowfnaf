import pygame
import random
import time

from code.Timer import Timer


class BaseSpeed:

    def __init__(self, sprite, size, aggressive, wait_time, speed_jumpscare_sound, speed_jumpscare, display):

        self.sprite = pygame.transform.scale(sprite, size)
        self.size = size
        self.aggressive = aggressive
        self.waitTime = wait_time
        self.speedJumpscareSound = speed_jumpscare_sound
        self.speedJumpscareSprite = speed_jumpscare
        self.display = display

        self.nextAttack = None
        self.beforeKill = None

        self.attacking = False

    def update(self, door_open):
        if not self.beforeKill:
            if not self.nextAttack:
                self.nextAttack = Timer(random.randint(self.aggressive,
                                                       self.aggressive*3))
            else:
                self.nextAttack.update()
        if self.beforeKill:
            self.beforeKill.update()

        if self.nextAttack:
            if self.nextAttack.done:
                self.nextAttack = None
                self.attacking = True
                self.beforeKill = Timer(self.waitTime)

        if self.beforeKill:
            if self.beforeKill.done:
                if door_open:
                    self.speedJumpscareSound.play()
                    time.sleep(1)
                    self.display.blit(self.speedJumpscareSprite, (0, 0))
                    pygame.display.update()
                    time.sleep(1)
                    quit()
                else:
                    self.beforeKill = None
                    self.attacking = False


class BaseBen:
    def __init__(self, displaySize, sprite, aggressive, wait_time, jumpscare_sound):
        self.displaySize = displaySize
        self.sprite = sprite
        self.aggressive = aggressive
        self.waitTime = wait_time
        self.jumpscareSound = jumpscare_sound

        self.currentLocation = (0, 0)
        self.attacking = False
        self.spawnTimer = Timer(random.randint(aggressive,
                                               aggressive*3))
        self.beforeKillTimer = None

    def update(self):
        if self.spawnTimer:
            self.spawnTimer.update()
        if self.beforeKillTimer:
            self.beforeKillTimer.update()
        if self.spawnTimer:
            if self.spawnTimer.done:
                self.attacking = True
                self.currentLocation = (
                    random.randint(0, self.displaySize[0]-self.sprite.get_size()[0]),
                    self.displaySize[1]-self.sprite.get_size()[1]
                )
                self.spawnTimer = None
                self.beforeKillTimer = Timer(self.waitTime)
        if self.attacking:
            if self.beforeKillTimer:
                if self.beforeKillTimer.done:
                    pass


