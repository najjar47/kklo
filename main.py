import pygame
import sys
import arabic_reshaper
from bidi.algorithm import get_display
import json

# تهيئة pygame
pygame.init()

# ثوابت اللعبة
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.8

# الألوان
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# إنشاء النافذة
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("مقاوم القسام")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT - 100
        self.velocity_y = 0
        self.jumping = False

    def update(self):
        # الحركة والقفز
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_SPACE] and not self.jumping:
            self.velocity_y = -15
            self.jumping = True

        # تطبيق الجاذبية
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # التحقق من الأرض
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity_y = 0
            self.jumping = False

class Game:
    def __init__(self):
        self.player = Player()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.current_level = 1
        self.font = pygame.font.Font(None, 36)

    def draw_text(self, text, x, y):
        # معالجة النص العربي
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        text_surface = self.font.render(bidi_text, True, BLACK)
        screen.blit(text_surface, (x, y))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # تحديث
            self.all_sprites.update()

            # الرسم
            screen.fill(WHITE)
            self.all_sprites.draw(screen)
            self.draw_text(f"المرحلة: {self.current_level}", 10, 10)

            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit() 