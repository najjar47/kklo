import pygame
import os

class QassamFighter:
    def __init__(self):
        # تحميل صور البطل
        self.scale = 2
        self.animation_count = 0
        self.facing_right = True
        
        # الموقع والحركة
        self.x = 100
        self.y = 500
        self.width = 40
        self.height = 60
        self.vel_y = 0
        self.vel_x = 0
        self.jumping = False
        self.on_ground = True
        
        # خصائص البطل
        self.health = 100
        self.ammo = 50
        self.score = 0
        
        # مؤقت إطلاق النار
        self.shoot_cooldown = 0
        self.shoot_cooldown_max = 15

        # صندوق التصادم
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect.x = self.x
        self.rect.y = self.y

    def handle_movement(self, keys):
        # الحركة الأفقية
        if keys[pygame.K_LEFT]:
            self.vel_x = -8
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            self.vel_x = 8
            self.facing_right = True
        else:
            self.vel_x = 0

        # القفز
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -15
            self.on_ground = False
            self.jumping = True

    def apply_gravity(self):
        # تطبيق الجاذبية
        self.vel_y += 0.8
        
        # تحديد السرعة القصوى للسقوط
        if self.vel_y > 15:
            self.vel_y = 15

    def update(self):
        # تحديث الموقع
        self.move(self.vel_x, self.vel_y)
        
        # تحديث مؤقت إطلاق النار
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        # تحريك الشخصية
        keys = pygame.key.get_pressed()
        self.handle_movement(keys)
        self.apply_gravity()

        # التحقق من الأرض (مؤقتاً)
        if self.y > 500:
            self.y = 500
            self.vel_y = 0
            self.on_ground = True
            self.jumping = False

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = self.shoot_cooldown_max
            self.ammo -= 1
            # إرجاع موقع إطلاق النار
            bullet_x = self.x + self.width if self.facing_right else self.x
            return Bullet(bullet_x, self.y + self.height // 2, self.facing_right)
        return None

    def draw(self, screen):
        # رسم صندوق التصادم مؤقتاً (يمكن استبداله بالصور لاحقاً)
        color = (0, 255, 0) if self.health > 50 else (255, 165, 0)
        pygame.draw.rect(screen, color, self.rect)
        
        # رسم شريط الصحة
        health_width = 50 * (self.health / 100)
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y - 10, 50, 5))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y - 10, health_width, 5))

class Bullet:
    def __init__(self, x, y, facing_right):
        self.x = x
        self.y = y
        self.facing_right = facing_right
        self.speed = 15
        self.width = 10
        self.height = 5
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def move(self):
        direction = 1 if self.facing_right else -1
        self.x += self.speed * direction
        self.rect.x = self.x

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 0), self.rect) 
