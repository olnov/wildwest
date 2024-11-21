import pygame
from lib.shooter import Shooter
import sys
import random
import time

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.init()

font = pygame.font.Font(None, 74)


class Game:
    def __init__(self):
        # Clock to control game speed
        self.clock = pygame.time.Clock()
        
          # Initialize left and right shooters
        self.left_shooter = Shooter(
            x=200,
            y=SCREEN_HEIGHT // 2,
            idle_folder="./assets/left_shooter/idle",
            shoot_folder="./assets/left_shooter/shoot",
            flip=False
        )

        self.right_shooter = Shooter(
            x=SCREEN_WIDTH - 260,
            y=SCREEN_HEIGHT // 2,
            idle_folder="./assets/right_shooter/idle",
            shoot_folder="./assets/right_shooter/shoot",
            flip=True
        )

         # Collect frames for diagnostics (if needed)
        self.idle_frames = self.left_shooter.idle_frames + self.right_shooter.idle_frames
        self.shooting_frames = self.left_shooter.shooting_frames + self.right_shooter.shooting_frames

        print(f"Idle frames loaded: {len(self.idle_frames)}")
        print(f"Shooting frames loaded: {len(self.shooting_frames)}")

        # Add this to your Game class initialization
        self.fire_sound = pygame.mixer.Sound("./assets/soundfx/fire_shot01.mp3")

        # Countdown setup
        self.countdown = random.randint(2, 7)
        self.countdown_timer = pygame.time.get_ticks()
        self.game_started = False
        self.game_over = False
        self.ready_to_restart = False
        self.winner = None
        self.start_screen = True
        self.player_points = 0
        self.computer_points = 0
        self.computer_shoot_speed = random.uniform(0.1, 1.5)
        self.start = 0
        
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
                
                if event.type == pygame.KEYDOWN and self.start_screen:
                    if event.key == pygame.K_SPACE:
                        self.start_screen = False

                if self.game_started and not self.game_over:
                    if time.time() - self.start > self.computer_shoot_speed:
                        self.computer_shoots()
 
                if event.type == pygame.KEYDOWN and not self.game_over:
                    if event.key == pygame.K_SPACE and self.game_started:
                        self.handle_shoot()
                
                if event.type == pygame.KEYDOWN and self.game_over:
                    if self.ready_to_restart == True and event.key == pygame.K_SPACE:
                        self.handle_restart()
                    elif self.ready_to_restart == False:
                        self.ready_to_restart = True
                    

            # Update game state
            self.update()

            # Drawing
            self.draw()
            
            # Shooters
            self.left_shooter.draw(screen)
            self.right_shooter.draw(screen)
            
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
                    self.start = time.time()

    def computer_shoots(self):
        self.computer_points += 1
        self.game_over = True
        self.ready_to_restart = False
        self.game_started = False
        print(self.player_points)
        print(self.computer_points)
        


        # Update shooters
        self.left_shooter.update()
        self.right_shooter.update()

    def handle_shoot(self):
        # Implement shooting logic

        if not self.game_started or self.game_over:
            return
        
        self.left_shooter.shoot()
        self.fire_sound.play()

        if self.game_started and not self.game_over:
            self.player_points += 1
            self.game_over = True
            self.ready_to_restart = False
            self.game_started = False
            print(self.player_points)
            print(self.computer_points)


    def handle_restart(self):
        if self.game_over and self.ready_to_restart:
            self.countdown = random.randint(2, 7)
            self.game_over = False
            self.game_started = False
            self.start = 0
            self.computer_shoot_speed = random.uniform(0.1, 1.5)
        
    def draw(self):
        # Draw the background
        screen.blit(self.background, (0, 0))

        # Draw shooters
        self.left_shooter.draw(screen)
        self.right_shooter.draw(screen)

        player_score = font.render(str(self.player_points), True, WHITE)
        player_rect = player_score.get_rect(center=(20, 550))
        screen.blit(player_score, player_rect)

        computer_score = font.render(str(self.computer_points), True, WHITE)
        computer_rect = computer_score.get_rect(center=(SCREEN_WIDTH - 20, 550))
        screen.blit(computer_score, computer_rect)

        if self.start_screen:
            welcome_text = font.render('Welcome to Highnoon shooter', True, WHITE)
            welcome_rect = welcome_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            screen.blit(welcome_text, welcome_rect)

            start_text = font.render('Press space to start', True, WHITE)
            start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
            screen.blit(start_text, start_rect)
        # Draw countdown or result
        elif not self.game_started:
            countdown_text = font.render('Get ready to fire..', True, WHITE)
            text_rect = countdown_text.get_rect(center=(SCREEN_WIDTH//2, 100))
            screen.blit(countdown_text, text_rect)
        elif self.game_over:
            result_text = font.render("Game Over!", True, WHITE)
            text_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            screen.blit(result_text, text_rect)

            restart_text = font.render("Press space to start new round", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
            screen.blit(restart_text, restart_rect)
        elif self.game_started:
            fire_text = font.render('FIRE!', True, RED)
            text_rect = fire_text.get_rect(center=(SCREEN_WIDTH//2, 100))
            screen.blit(fire_text, text_rect)


    