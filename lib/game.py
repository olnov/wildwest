import pygame
from lib.shooter import Shooter
import sys
import random

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

player_points = 0
computer_points = 0

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.init()

font = pygame.font.Font(None, 74)

class Game:
    def __init__(self):
        # Clock to control game speed
        self.clock = pygame.time.Clock()
        
        # Create two shooters
        self.left_shooter = Shooter(100, RED)
        self.right_shooter = Shooter(SCREEN_WIDTH - 150, GREEN)
        
        # Countdown setup
        self.countdown = random.randint(2, 7)
        self.countdown_timer = pygame.time.get_ticks()
        self.game_started = False
        self.game_over = False
        self.winner = None
        
        # Load background image
        self.background = pygame.image.load("./assets/background_2.jpg")
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def run(self):
        # Main game loop
        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN and not self.game_over:
                    if event.key == pygame.K_SPACE and self.game_started:
                        self.handle_shoot()

            # Update game state
            self.update()

            # Drawing
            self.draw()
            
            # Update display
            pygame.display.flip()
            
            # Control game speed
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def update(self):
        # Countdown logic
        if not self.game_started:
            current_time = pygame.time.get_ticks()
            if current_time - self.countdown_timer > 1000:
                self.countdown -= 1
                self.countdown_timer = current_time
                
                if self.countdown <= 0:
                    self.game_started = True

    def handle_shoot(self):
        # Implement shooting logic
        self.game_over = True
        
    def draw(self):
        # Draw the background
        screen.blit(self.background, (0, 0))

        # Draw shooters
        self.left_shooter.draw(screen)
        self.right_shooter.draw(screen)

        # Draw countdown or result
        if not self.game_started:
            countdown_text = font.render('Get ready to fire..', True, WHITE)
            text_rect = countdown_text.get_rect(center=(SCREEN_WIDTH//2, 100))
            screen.blit(countdown_text, text_rect)
        elif self.game_over:
            result_text = font.render("Game Over!", True, WHITE)
            text_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            screen.blit(result_text, text_rect)
        elif self.game_started:
            fire_text = font.render('FIRE!', True, RED)
            text_rect = fire_text.get_rect(center=(SCREEN_WIDTH//2, 100))
            screen.blit(fire_text, text_rect)

        # Draw player and computer scores
        player_score = font.render(player_points, True, WHITE)
        text_rect = player_score.get_rect(center=(20, 500))
        screen.blit(player_score, text_rect)

        computer_score = font.render(computer_points, True, WHITE)
        text_rect = computer_score.get_rect(center=(SCREEN_WIDTH - 20, 500))
        screen.blit(computer_score, text_rect)

        
    
    def user_points_update(self):
        player_score = font.render(player_points, True, WHITE)
        text_rect = player_score.get_rect(center=(20, 500))
        screen.blit(player_score, text_rect)

        computer_score = font.render(computer_points, True, WHITE)
        text_rect = computer_score.get_rect(center=(SCREEN_WIDTH - 20, 500))
        screen.blit(computer_score, text_rect)

        if self.victory:
            global player_points += 1
            player_score = font.render(player_points, True, WHITE)
            text_rect = player_score.get_rect(center=(20, 500))
            screen.blit(player_score, text_rect)
        elif self.game_over:
            global computer_points += 1
            computer_score = font.render(computer_points, True, WHITE)
            text_rect = computer_score.get_rect(center=(SCREEN_WIDTH - 20, 500))
            screen.blit(computer_score, text_rect)
