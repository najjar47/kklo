import pygame
import random

class Enemy:
    def __init__(self, x, y, enemy_type="جندي"):
        self.enemy_type = enemy_type
        self.x = x
        self.y = y
        
        # تحديد خصائص العدو حسب نوعه
        if enemy_type == "جندي":
            self.width = 40
            self.height = 60
            self.health = 50
            self.speed = 2
            self.color = (255, 0, 0)
        elif enemy_type == "قناص":
            self.width = 35
            self.height = 55
            self.health = 40
            self.speed = 1
            self.color = (150, 0, 0)
        elif enemy_type == "دبابة":
            self.width = 80
            self.height = 50
            self.health = 200
            self.speed = 1
            self.color = (100, 100, 100)
        
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.direction = 1
        self.move_counter = 0
        self.shoot_cooldown = 0
        self.shoot_cooldown_max = 60 if enemy_type == "قناص" else 120

    def move(self):
        self.x += self.speed * self.direction
        self.move_counter += 1
        
        # تغيير الاتجاه بعد مسافة معينة
        if self.move_counter >= 100:
            self.direction *= -1
            self.move_counter = 0
        
        self.rect.x = self.x

    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0

    def can_shoot(self):
        return self.enemy_type in ["قناص", "دبابة"] and self.shoot_cooldown == 0

    def shoot(self, player_x, player_y):
        if self.can_shoot():
            self.shoot_cooldown = self.shoot_cooldown_max
            bullet_x = self.x + self.width // 2
            bullet_y = self.y + self.height // 2
            
            # حساب اتجاه الرصاصة نحو اللاعب
            direction = 1 if player_x > self.x else -1
            return EnemyBullet(bullet_x, bullet_y, direction)
        return None

    def update(self, player_x, player_y):
        self.move()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
        # محاولة إطلاق النار إذا كان اللاعب في المدى
        if abs(player_x - self.x) < 300 and abs(player_y - self.y) < 100:
            return self.shoot(player_x, player_y)
        return None

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        
        # رسم شريط الصحة
        max_health = 200 if self.enemy_type == "دبابة" else 50
        health_width = 50 * (self.health / max_health)
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y - 10, 50, 5))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y - 10, health_width, 5))

class EnemyBullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 10
        self.width = 8
        self.height = 4
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def move(self):
        self.x += self.speed * self.direction
        self.rect.x = self.x

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 100, 100), self.rect) 
