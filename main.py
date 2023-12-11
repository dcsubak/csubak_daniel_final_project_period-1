# This file was created by: Daniel Csubak

# Sources:
# https://python.plainenglish.io/building-a-breakout-game-from-scratch-pygame-oop-132d992fedc0

import pygame
import sys
import random

class Paddle:
    # Player controlled object in which it is used to redirect the ball...
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 80, 10)
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
    
    def move(self, speed):
        keys = pygame.key.get_pressed()
        if keys [pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-speed, 0)
        elif keys [pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.move_ip(speed, 0)

class Brick:
    # Object that is meant to be hit by ball and gets killed and gives player points...
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 60, 20)
        self.color = (random.randint(0,255), random.randint(0, 255), random.randint(0,255))
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Ball:
    # Object that is constantly moving which can be redirected by player operated paddle in order to hit bricks to kill them...
    def __init__(self, x, y):
        self.start_x = x
        self.start_y = self.reset()
    
    def reset(self):
        self.rect = pygame.Rect(self.start_x, self.start_y, 10, 10)
        self.dx = 1
        self.dy = -1

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
    
    def move(self, speed):
        self.rect.move_ip(self.dx * speed, self.dy * speed)

    def bounce(self, paddle, bricks):
        if self.rect.left < 0 or self.rect.right > 800:
            self.dx *= -1
        elif self.rect.top < 0 or self.rect.colliderect(paddle.rect):
            self.dy *= -1
        else:
            hit_brick = self.rect.collidelist(bricks)
            if hit_brick != -1:
                self.dy *= -1
                return hit_brick
            
class BreakoutGame:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.font = pygame.font.Font(None, 36)
        self.score = 0
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.paddle = Paddle(width / 2, height - 20)
        self.ball = Ball(width / 2, height / 2)
        self.lives = 3
        self.reset_bricks()

    def reset_bricks(self):
        self.bricks = []
        for i in range(5):
            for j in range(12):
                self.bricks.append(Brick(j * 60 + 50, i * 20 + 50))
     
    def draw_text(self, text, pos):
        surface = self.font.render(text, True, (255, 255, 255))
        rect = surface.get_rect(center=pos)
        self.screen.blit(surface, rect)
                         
    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.paddle.move(2)

            if not self.bricks:
                self.ball.dx = 0
                self.ball.dy = 0
                self.draw_text("You Won!", (self.screen.get_width() / 2, self.screen.get_hieght() / 2)) 
                
