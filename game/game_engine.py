import pygame
from .paddle import Paddle
from .ball import Ball
import os

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.max_score = 5
        self.game_over = False
        self.winner_text = ""
        # Load sound effects
        self.hit_sound = pygame.mixer.Sound(os.path.join("assets", "hit.wav"))       # paddle hit
        self.wall_sound = pygame.mixer.Sound(os.path.join("assets", "wall.wav"))     # wall bounce
        self.score_sound = pygame.mixer.Sound(os.path.join("assets", "score.wav"))   # scoring



    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        if self.game_over:
            return

        # Move ball with wall sound
        self.ball.move(wall_sound=self.wall_sound)

        # Check paddle collisions with hit sound
        self.ball.check_collision(self.player, self.ai, hit_sound=self.hit_sound)

        self.ai.auto_track(self.ball, self.height)

        if self.ball.x <= 0:
            self.ai_score += 1
            self.score_sound.play()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.score_sound.play()
            self.ball.reset()

        # Check for winner
        if self.player_score == self.max_score:
            self.game_over = True
            self.winner_text = "Player Wins!"
        elif self.ai_score == self.max_score:
            self.game_over = True
            self.winner_text = "AI Wins!"



    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))
        if self.game_over:
            winner_surface = self.font.render(self.winner_text, True, WHITE)
            text_rect = winner_surface.get_rect(center=(self.width // 2, self.height // 2))
            screen.blit(winner_surface, text_rect)

    def show_replay_options(self, screen):
        """
        Display replay options after a game ends and wait for player input.
        Options:
          3 → Best of 3
          5 → Best of 5
          7 → Best of 7
          ESC → Exit
        """
        waiting = True
        font = pygame.font.SysFont("Arial", 28)
        WHITE = (255, 255, 255)

        while waiting:
            screen.fill((0, 0, 0))

            # Display menu
            lines = [
                "Game Over! Choose match length:",
                "Press 3 → Best of 3",
                "Press 5 → Best of 5",
                "Press 7 → Best of 7",
                "Press ESC → Exit"
            ]
            for i, line in enumerate(lines):
                text_surf = font.render(line, True, WHITE)
                text_rect = text_surf.get_rect(center=(self.width // 2, self.height // 2 - 60 + i * 40))
                screen.blit(text_surf, text_rect)

            pygame.display.flip()

            # Handle input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        self.max_score = 2  # Best of 3 → first to 2 wins
                        waiting = False
                    elif event.key == pygame.K_5:
                        self.max_score = 3  # Best of 5 → first to 3 wins
                        waiting = False
                    elif event.key == pygame.K_7:
                        self.max_score = 4  # Best of 7 → first to 4 wins
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

        # Reset game state for replay
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.winner_text = ""
        self.ball.reset()
