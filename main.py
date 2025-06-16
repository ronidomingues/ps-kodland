# Permited libraries to use this code
import random
import math
from pygame import Rect

# PgZero variables
WIDTH = 800
HEIGHT = 600
TITLE = "Dungeon Escape"

# Game States
game_state = 'menu'
sound_on = True

# Music and Sound
music_file = './sounds/background.mp3'
step_sound = './sounds/step.wav'

# Hero and Enemies
hero = lambda id: f'images/hero/hero_walk{id}.png'
enemy = lambda id: f'images/enemy/enemy_idle{id}.png'

# Graphics
TILE_SIZE = 64
ROWS = HEIGHT // TILE_SIZE
COLS = WIDTH // TILE_SIZE

# Entities
hero = Actor(hero(1), (TILE_SIZE, TILE_SIZE))
hero.grid = [1 ,1]
hero.target = hero.grid[:]
hero.frame = 0

enemies = []

def generate_enemies():
    for i in range(3):
        enemy = Actor(enemy(1), (random.randint(2, COLS - 2) * TILE_SIZE, random.randint(2, ROWS - 2) * TILE_SIZE))
        enemy.grid = [enemy.x // TILE_SIZE, enemy.y // TILE_SIZE]
        enemy.dir = random.choice([(0,1),(1,0),(0,-1),(-1,0)])
        enemy.frame = 0
        enemies.append(enemy)
def draw():
    screen.clear()
    if game_state == 'menu':
        screen.draw.text("Dungeon Escape", center=(WIDTH//2, 100), fontsize=50)
        screen.draw.text("1. Start Game", center=(WIDTH//2, 200), fontsize=40)
        screen.draw.text(f"2. Sound: {'On' if sound_on else 'Off'}", center=(WIDTH//2, 260), fontsize=40)
        screen.draw.text("3. Exit", center=(WIDTH//2, 320), fontsize=40)
    elif game_state == 'playing':
        draw_grid()
        hero.draw()
        for enemy in enemies:
            enemy.draw()
    elif game_state == 'gameover':
        screen.draw.text("Game Over!", center=(WIDTH//2, HEIGHT//2), fontsize=60)
def draw_grid():
    for y in range(ROWS):
        for x in range(COLS):
            screen.blit('tile', (x*TILE_SIZE, y*TILE_SIZE))
def update():
    global game_state

    if game_state == 'playing':
        update_hero()
        update_enemies()
        check_collisions()
def update_hero():
    if hero.grid != hero.target:
        dx = (hero.target[0] - hero.grid[0]) * 4
        dy = (hero.target[1] - hero.grid[1]) * 4
        hero.x += dx
        hero.y += dy
        if abs(hero.x - hero.target[0]*TILE_SIZE) < 5 and abs(hero.y - hero.target[1]*TILE_SIZE) < 5:
            hero.grid = hero.target[:]
            hero.x = hero.grid[0] * TILE_SIZE
            hero.y = hero.grid[1] * TILE_SIZE
        hero.frame = (hero.frame + 1) % 30
        hero.image = hero(1) if hero.frame < 15 else hero(2)
def update_enemies():
    for enemy in enemies:
        if random.random() < 0.01:
            enemy.dir = random.choice([(0,1), (1,0), (0,-1), (-1,0)])
        enemy.grid[0] += enemy.dir[0]
        enemy.grid[1] += enemy.dir[1]
        enemy.grid[0] = max(0, min(COLS-1, enemy.grid[0]))
        enemy.grid[1] = max(0, min(ROWS-1, enemy.grid[1]))
        enemy.x = enemy.grid[0] * TILE_SIZE
        enemy.y = enemy.grid[1] * TILE_SIZE
        enemy.frame = (enemy.frame + 1) % 30
        enemy.image = enemy(1) if enemy.frame < 15 else enemy(2)
def check_colisions():
    global game_state
    for enemy in enemies:
        if Rect(hero.x, hero.y, TILE_SIZE, TILE_SIZE).colliderect(Rect(enemy.x, enemy.y, TILE_SIZE, TILE_SIZE)):
            game_state = 'gameover'
def on_key_down(key):
    if game_state != 'playing':
        return
    if hero.grid == hero.target:
        if key == keys.LEFT:
            hero.target[0] = max(0, hero.grid[0] - 1)
        elif key == keys.RIGHT:
            hero.target[0] = min(COLS - 1, hero.grid[0] + 1)
        elif key == keys.UP:
            hero.target[1] = max(0, hero.grid[1] - 1)
        elif key == keys.DOWN:
            hero.target[1] = min(ROWS - 1, hero.grid[1] + 1)
        if sound_on:
            sounds[step_sound].play()
def on_mouse_down(pos):
    global game_state, sound_on
    if game_state == 'menu':
        if 180 < pos[1] < 220:
            game_state = 'playing'
            hero.grid = [1, 1]
            hero.target = [1, 1]
            hero.x = hero.grid[0] * TILE_SIZE
            hero.y = hero.grid[1] * TILE_SIZE
            enemies.clear()
            generate_enemies()
            if sound_on:
                music.play(music_file)
        elif 240 < pos[1] < 280:
            sound_on = not sound_on
            if not sound_on:
                music.stop()
        elif 300 < pos[1] < 340:
            exit()