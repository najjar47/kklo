import pygame
import sys
import arabic_reshaper
from bidi.algorithm import get_display
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import os

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
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, x, y, health):
        super().__init__()
        self.type = enemy_type
        self.health = health
        
        # تحديد حجم ولون العدو حسب نوعه
        if enemy_type == "جندي":
            self.image = pygame.Surface((30, 50))
            self.image.fill(RED)
        elif enemy_type == "قناص":
            self.image = pygame.Surface((20, 40))
            self.image.fill((150, 0, 0))
        elif enemy_type == "دبابة":
            self.image = pygame.Surface((80, 40))
            self.image.fill((100, 100, 100))
        else:
            self.image = pygame.Surface((30, 30))
            self.image.fill(RED)
            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.move_counter = 0

    def update(self):
        # حركة بسيطة للأعداء
        self.rect.x += self.direction
        self.move_counter += 1
        if self.move_counter >= 100:
            self.direction *= -1
            self.move_counter = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((100, 50, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Collectible(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        super().__init__()
        self.type = item_type
        self.image = pygame.Surface((20, 20))
        
        if item_type == "سلاح":
            self.image.fill((255, 215, 0))  # ذهبي
        elif item_type == "ذخيرة":
            self.image.fill((192, 192, 192))  # فضي
        elif item_type == "صحة":
            self.image.fill((0, 255, 0))  # أخضر
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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
        self.health = 100
        self.ammo = 50

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
        self.load_levels()
        self.current_level = 1
        self.setup_level(self.current_level)
        self.font = pygame.font.Font(None, 36)

    def load_levels(self):
        with open('levels.json', 'r', encoding='utf-8') as f:
            self.levels_data = json.load(f)

    def setup_level(self, level_id):
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        
        self.player = Player()
        self.all_sprites.add(self.player)
        
        level = next((l for l in self.levels_data['levels'] if l['id'] == level_id), None)
        if level:
            # إضافة المنصات
            for platform in level.get('platforms', []):
                p = Platform(platform['x'], platform['y'], platform['width'], platform['height'])
                self.platforms.add(p)
                self.all_sprites.add(p)
            
            # إضافة الأعداء
            for enemy in level.get('enemies', []):
                e = Enemy(enemy['type'], enemy['x'], enemy['y'], enemy['health'])
                self.enemies.add(e)
                self.all_sprites.add(e)
            
            # إضافة العناصر القابلة للجمع
            for item in level.get('collectibles', []):
                c = Collectible(item['type'], item['x'], item['y'])
                self.collectibles.add(c)
                self.all_sprites.add(c)

    def draw_text(self, text, x, y):
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        text_surface = self.font.render(bidi_text, True, BLACK)
        screen.blit(text_surface, (x, y))

    def run(self):
        global screen
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("مقاوم القسام")
        clock = pygame.time.Clock()
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:  # للانتقال إلى المرحلة التالية (مؤقتاً للتجربة)
                        self.current_level += 1
                        if self.current_level <= len(self.levels_data['levels']):
                            self.setup_level(self.current_level)

            # تحديث
            self.all_sprites.update()

            # التصادم مع المنصات
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.rect.bottom = hits[0].rect.top
                self.player.velocity_y = 0
                self.player.jumping = False

            # جمع العناصر
            collectible_hits = pygame.sprite.spritecollide(self.player, self.collectibles, True)
            for hit in collectible_hits:
                if hit.type == "صحة":
                    self.player.health = min(100, self.player.health + 20)
                elif hit.type == "ذخيرة":
                    self.player.ammo += 30

            # الرسم
            screen.fill(WHITE)
            self.all_sprites.draw(screen)
            self.draw_text(f"المرحلة: {self.current_level}", 10, 10)
            self.draw_text(f"الصحة: {self.player.health}", 10, 40)
            self.draw_text(f"الذخيرة: {self.player.ammo}", 10, 70)

            pygame.display.flip()
            clock.tick(FPS)

class GameHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/start-game':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "success", "message": "Game started"}
            self.wfile.write(json.dumps(response).encode())
            game_thread = threading.Thread(target=start_game)
            game_thread.start()
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path == '/levels':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            with open('levels.json', 'r', encoding='utf-8') as f:
                levels_data = json.load(f)
            self.wfile.write(json.dumps(levels_data['levels']).encode())
        else:
            return SimpleHTTPRequestHandler.do_GET(self)

def start_game():
    game = Game()
    game.run()
    pygame.quit()

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, GameHandler)
    print("Server running at http://localhost:8000")
    httpd.serve_forever()

if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nShutting down server...")
        sys.exit(0) 
