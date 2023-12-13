# This file was created by: Daniel Csubak

# Sources:
# https://python.plainenglish.io/building-a-breakout-game-from-scratch-pygame-oop-132d992fedc0
# https://www.youtube.com/watch?v=z6h6l1yJ5-w
# https://www.youtube.com/watch?v=atoGQ9o0ooI
# Content from Chris Cozort
# Content from Liam Hare

# Goals:
# Make working breakout game...
# Make score counter...
# Make bricks reset...
# Make power-ups...
# Make Respawns...

# Rules:
# When player runs out of lives, bricks reset...
# When player misses ball, they use up 1 of there 3 lives given...
# When player moves paddle, they can hit the ball...
# When bricks are destroyed, player recieves +5 points...

# Feedback:
# When player hits ball with paddle, they redirect the ball from collisions...
# When ball hits bricks, they kill the brick because of collision...
# When player kills brick, they are rewarded points...

# Freedom:
# Player can move paddle freely...
# Player can miss or hit ball with paddle...
# Player can reset game by missing ball with paddle...

import pygame
import sys
import random

class Paddle:
    # Initialization of the paddle class which is player controlled...
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 80, 10)

    def draw(self, screen):
        # Creates paddle on the screen...
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

    def move(self, speed):
        # Keybinds used to manipulate the paddle controlled by the player...
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.rect.move_ip(-speed * 2, 0)  # Speed is adjustable and subject to change...
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < 800:
            self.rect.move_ip(speed * 2, 0)  # Speed is adjustable and subject to change...

class Brick:
    # Initialization of the brick class which does not move...
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 60, 20) # Dimensions of each brick throughout...
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def draw(self, screen):
        # Creates bricks on the screen...
        pygame.draw.rect(screen, self.color, self.rect)

class Ball:
    # Initialization of the ball class which moves and is manipulated by collisions...
    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y
        self.reset()

    def reset(self):
        # Resets the ball back to its original position...
        self.rect = pygame.Rect(self.start_x, self.start_y, 10, 10)
        self.dx = 1
        self.dy = -1

    def draw(self, screen):
        # Creates the ball on the screen...
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

    def move(self, speed):
        # How the ball is able to move based on its collisions and position...
        self.rect.move_ip(self.dx * speed, self.dy * speed)

    def bounce(self, paddle, bricks):
        # Function and mechanics allowing the ball to have a hitbox and be reactive to collisions...
        if self.rect.left < 0 or self.rect.right > 800:
            self.dx *= -1
        elif self.rect.top < 0 or self.rect.colliderect(paddle.rect):
            self.dy *= -1
        else:
            brick_rects = [brick.rect for brick in bricks if isinstance(brick, Brick)] # What the balls reaction to after making collision with brick...
            hit_brick = self.rect.collidelist(brick_rects)
            if hit_brick != -1:
                self.dy *= -1
                return hit_brick

class BreakoutGame:
    # Setting dimensions of the game window on screen...
    def __init__(self, width=800, height=600):
        pygame.init()
        self.font = pygame.font.Font(None, 36)
        self.score = 0
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock() # Loop for game to run at 90 fps...
        self.paddle = Paddle(width / 2, height - 20)
        self.ball = Ball(width / 2, height / 2)
        self.lives = 3 # Amount of player's lives given at start of the game...
        self.reset_bricks() # Game resets if player has run out of all 3 lives...

    def reset_bricks(self):
        # Bricks get reset and reinstantiaded when game starts over...
        self.bricks = []
        for i in range(5):
            for j in range(12):
                self.bricks.append(Brick(j * 60 + 50, i * 20 + 50))

    def draw_text(self, text, pos):
        # Creating text on screen so it can be viewed by player...
        surface = self.font.render(text, True, (255, 255, 255))
        rect = surface.get_rect(center=pos) # Position of where text goes on screen...
        self.screen.blit(surface, rect)

    def run_game(self):
        # Game loop...
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Exit window/game...
                    pygame.quit()
                    sys.exit()

            self.paddle.move(4) # Base paddle speed based on player input...

            if not self.bricks:
                self.ball.dx = 0
                self.ball.dy = 0
                self.draw_text("Congratulations! You Win!", (self.screen.get_width() / 2, self.height / 2))
                self.draw_text("Press any key to start a new game.", (self.screen.get_width() / 2, self.height / 2 + 50))
                pygame.display.flip()
                waiting_for_input = True # Waiting for player to press any key to start...
                while waiting_for_input:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            waiting_for_input = False

                self.reset_bricks()  # Respawns a new set of bricks...
                self.ball.reset()
                self.paddle = Paddle(self.width / 2, self.height - 20)
                self.score = 0
                self.lives = 3  # Reset lives...

            self.ball.move(2)
            hit_brick = self.ball.bounce(self.paddle, self.bricks)

            if hit_brick is not None:
                if random.random() < 0.1:  # 10% chance for a power-up when player collides ball with bricks...
                    self.spawn_power_up(self.bricks[hit_brick])
                del self.bricks[hit_brick]
                self.score += 5 # Points player recieves for colliding ball with bricks...

            for ball in self.bricks: # Moves all balls, including the newly spawned ones resulting from power-up...
                if isinstance(ball, Ball):  # Only move ball instances, not other objects present...
                    ball.move(2)
                    brick_hit = ball.bounce(self.paddle, self.bricks)
                    if brick_hit is not None:
                        del self.bricks[brick_hit]
                        self.score += 5 # Points player recieves for colliding ball with bricks...

            if self.ball.rect.bottom > self.height: # Check if ball hit the bottom of the screen...
                self.lives -= 1
                if self.lives == 0:
                    self.reset_bricks()  # Respawns a new set of bricks...
                    self.score = 0
                    self.lives = 3  # Resets lives...
                self.ball.reset()
                self.paddle = Paddle(self.width / 2, self.height - 20)

            self.screen.fill((0, 0, 0))
            self.paddle.draw(self.screen)
            self.ball.draw(self.screen)
            for brick in self.bricks:
                brick.draw(self.screen)
            self.draw_text(f"Score: {self.score} Lives: {self.lives}", (self.screen.get_width() / 2, 20))
            pygame.display.flip()
            self.clock.tick(120) # Overall game framerate which is what every game asset runs at...

    def spawn_power_up(self, brick):
        # Spawns a power-up if player hits 10% chance spawning more balls...
        # Spawn 5 balls instead of one at the position of the brick that was collided with by initial ball...
        for _ in range(5):
            new_ball = Ball(brick.x, brick.y)
            new_ball.dx = random.choice([-1, 1])  # Randomize the initial balls trajectory and direction...
            new_ball.dy = -1  # Move upwards...
            self.bricks.append(new_ball)

if __name__ == "__main__":
    breakout = BreakoutGame()
    breakout.run_game()
