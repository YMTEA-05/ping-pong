import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self, hit_sound=None, wall_sound=None):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Wall bounce
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            if wall_sound:
                wall_sound.play()

    def check_collision(self, player, ai, hit_sound=None):
        ball_rect = self.rect()
        player_rect = player.rect()
        ai_rect = ai.rect()

        # Player paddle collision
        if ball_rect.colliderect(player_rect):
            self.x = player_rect.right
            self.velocity_x = abs(self.velocity_x)
            if hit_sound:
                hit_sound.play()

        # AI paddle collision
        elif ball_rect.colliderect(ai_rect):
            self.x = ai_rect.left - self.width
            self.velocity_x = -abs(self.velocity_x)
            if hit_sound:
                hit_sound.play()



    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
