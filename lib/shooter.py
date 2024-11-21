import pygame


SCREEN_HEIGHT = 600

class Shooter:
    def __init__(self, x, color):
        self.x = x
        self.y = SCREEN_HEIGHT // 2
        self.color = color
        self.width = 50
        self.height = 100
        self.shot = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, 
                         (self.x, self.y, self.width, self.height))
