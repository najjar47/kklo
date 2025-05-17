import pygame
import sys
import json
from qassam_fighter import QassamFighter, Bullet
from enemies import Enemy, EnemyBullet

# تهيئة pygame
pygame.init()
pygame.font.init()

# إعدادات الشاشة
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("مقاوم القسام")

# الألوان
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# تحميل الخلفية (مؤقتاً نستخدم لون)
background_color = (100, 150, 255)

class Game:
    def __init__(self):
        self.player = QassamFighter()
        self.current_level = 1
        self.enemies = []
        self.player_bullets = []
        self.enemy_bullets = []
        self.score = 0
        self.font = pygame.font.SysFont('arial', 30)
        self.load_level(self.current_level)

    def load_level(self, level):
        self.enemies.clear()
        self.player_bullets.clear()
        self.enemy_bullets.clear()
        
        # إضافة الأعداء حسب المستوى
        if level == 1:
            self.enemies.append(Enemy(400, 500, "جندي"))
            self.enemies.append(Enemy(600, 500, "جندي"))
        elif level == 2:
            self.enemies.append(Enemy(300, 500, "جندي"))
            self.enemies.append(Enemy(700, 400, "قناص"))
        elif level == 3:
            self.enemies.append(Enemy(500, 500, "دبابة"))
            self.enemies.append(Enemy(300, 500, "جندي"))
            self.enemies.append(Enemy(600, 400, "قناص"))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_CONTROL:
                    bullet = self.player.shoot()
                    if bullet:
                        self.player_bullets.append(bullet)
                elif event.key == pygame.K_n:  # للتجربة: الانتقال للمستوى التالي
                    self.current_level += 1
                    self.load_level(self.current_level)
        return True

    def update(self):
        # تحديث اللاعب
        self.player.update()

        # تحديث الأعداء
        for enemy in self.enemies:
            bullet = enemy.update(self.player.x, self.player.y)
            if bullet:
                self.enemy_bullets.append(bullet)

        # تحديث الرصاص
        for bullet in self.player_bullets[:]:
            bullet.move()
            # التحقق من إصابة العدو
            for enemy in self.enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    if enemy.take_damage(25):
                        self.enemies.remove(enemy)
                        self.score += 100
                    if bullet in self.player_bullets:
                        self.player_bullets.remove(bullet)
                    break

        # تحديث رصاص العدو
        for bullet in self.enemy_bullets[:]:
            bullet.move()
            if bullet.rect.colliderect(self.player.rect):
                self.player.health -= 10
                self.enemy_bullets.remove(bullet)

        # إزالة الرصاص خارج الشاشة
        self.player_bullets = [b for b in self.player_bullets if 0 < b.x < SCREEN_WIDTH]
        self.enemy_bullets = [b for b in self.enemy_bullets if 0 < b.x < SCREEN_WIDTH]

        # التحقق من انتهاء المستوى
        if not self.enemies:
            self.current_level += 1
            self.load_level(self.current_level)

    def draw(self):
        # رسم الخلفية
        screen.fill(background_color)
        
        # رسم اللاعب
        self.player.draw(screen)
        
        # رسم الأعداء
        for enemy in self.enemies:
            enemy.draw(screen)
        
        # رسم الرصاص
        for bullet in self.player_bullets:
            bullet.draw(screen)
        for bullet in self.enemy_bullets:
            bullet.draw(screen)

        # رسم معلومات اللعبة
        score_text = self.font.render(f"النقاط: {self.score}", True, BLACK)
        level_text = self.font.render(f"المرحلة: {self.current_level}", True, BLACK)
        health_text = self.font.render(f"الصحة: {self.player.health}", True, BLACK)
        ammo_text = self.font.render(f"الذخيرة: {self.player.ammo}", True, BLACK)
        
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 40))
        screen.blit(health_text, (10, 70))
        screen.blit(ammo_text, (10, 100))

        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            clock.tick(60)

# تشغيل اللعبة
if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit() 
