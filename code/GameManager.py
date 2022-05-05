import time
import pygame


class GameManager:

    def __init__(self, display, speed_jumpscare_sound, speed_jumpscare_sprite):

        self.oxygen = 100
        self.display = display
        self.speedJumpscareSound = speed_jumpscare_sound
        self.speedJumpscareSprite = speed_jumpscare_sprite
        self.squaresAmount = 7
        self.squareSize = display.get_width()/50
        self.font = pygame.font.Font('static/OCRAM.ttf', int(self.squareSize/2))

    def update_draw_oxygen(self, door_open):

        if not door_open:
            self.oxygen -= 0.02
            if self.oxygen <= 0:
                self.speedJumpscareSound.play()
                time.sleep(1)
                self.display.blit(self.speedJumpscareSprite, (0, 0))
                pygame.display.update()
                time.sleep(1)
                quit()

        percent = self.oxygen/100
        anti_percent = 100-self.oxygen

        rendered_text = self.font.render("Power left:{}%".format(int(self.oxygen)),
                                         False, (255, 255, 255))

        start_width = self.display.get_width()/10

        toAdd = 0
        self.display.blit(rendered_text, (start_width,
                                          self.display.get_height() - self.display.get_height() / 4.4))
        for i in range(int(self.squaresAmount*percent)):

            pygame.draw.rect(self.display, (anti_percent*2.8, 255*percent, 0),
                             (start_width+i*self.squareSize+toAdd,
                              self.display.get_height()-self.display.get_height()/5,
                              self.squareSize, self.display.get_height()/10))

            toAdd += self.squareSize / 5

    def draw_rect_alpha(self, surface, color, rect):
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA).convert_alpha()
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        surface.blit(shape_surf, rect)