import pgzero
from pgzero.rect import Rect

# Configurações da janela
WIDTH   = 800
HEIGHT  = 600
TITLE   = 'O Navio Fantasma'

# Configurações do grid
TILE_SIZE   = 50
MAP_WIDTH   = 14    # Número de tiles na largura
MAP_HEIGHT  = 10    # Número de tiles na altura

MARGIN_X = (WIDTH - (MAP_WIDTH * TILE_SIZE)) // 2
MARGIN_Y = (HEIGHT - (MAP_HEIGHT * TILE_SIZE)) // 2

# Estado do som
SOUND_ON = True

# Estado do jogo
GAME_STATE = 'menu'

# Mapa do jogo (. = chão, # = rachadura, p = pirata, m = mostro, t = tesouro)
GAME_MAP = [
    "p.............",
    ".###.####..###",
    ".|......|.....",
    ".|......|....t",
    ".|.m..........",
    ".|t.........m.",
    ".#####..#.###.",
    "...m..........",
    ".##..##t.##...",
    ".............."
]

# Atores
menu_background = Actor('menu_background', center=(WIDTH/2, HEIGHT/2))
game_background = Actor('game_background', center=(WIDTH/2, HEIGHT/2))
title = Actor('title_image', center=(WIDTH/2, 150))
start_button = Actor('start_button', center=(WIDTH/2, 400))
exit_button = Actor('exit_button', center=(WIDTH/2, 470))
sound_button = Actor('sound_on', topright=(WIDTH-740, 10))

walls = []
monsters = []
monter_frames = ['monster/monster1', 'monster/monster2', 'monster/monster3', 'monster/monster4', 'monster/monster5', 'monster/monster6']
treasures = []

# Música de fundo
sounds.crying_out_in_the_darkness.play(-1)

def setup_game():
    for y, row in enumerate(GAME_MAP):
        for x, tile in enumerate(row):
            pos_x = MARGIN_X + x * TILE_SIZE + TILE_SIZE // 2
            pos_y = MARGIN_Y + y * TILE_SIZE + TILE_SIZE // 2

            if tile == '#':
                wall = Actor('bone', center=(pos_x, pos_y))
                walls.append(wall)
                wall.angle = 0
                wall.draw()
            elif tile == '|':
                wall = Actor('bone', center=(pos_x, pos_y))
                walls.append(wall)
                wall.angle = 90
                wall.draw()
            elif tile == 'm':
                monster = Actor('monster/monster', center=(pos_x, pos_y))
                monster.vx = 1
                monster.frame = 0
                monsters.append(monster)
                monster.draw()
            elif tile == 't':
                treasure = Actor('treasure', center=(pos_x, pos_y))
                treasures.append(treasure)
                treasure.draw()
            # elif tile == 'p':
            #     Actor('pirate', center=(pos_x, pos_y)).draw()

def draw_game():
    game_background.draw()
    
    for wall in walls:
        wall.draw()

    for monster in monsters:
        monster.draw()

    for treasure in treasures:
        treasure.draw()


def draw_menu():
    menu_background.draw()
    title.draw()
    start_button.draw()
    exit_button.draw()
    sound_button.draw()

def draw():
    screen.clear()

    if GAME_STATE == 'menu':
        draw_menu()
    elif GAME_STATE == 'game':
        draw_game()

def update():
    if GAME_STATE == 'game':
        for monster in monsters:
            monster.x += monster.vx

            if monster.right > WIDTH or monster.left < 0:
                monster.vx = -monster.vx  # Inverter direção ao sair da tela
        
            if monster.collidelist(walls) != -1 or monster.collidelist(treasures) != -1:
                monster.vx = -monster.vx  # Inverter direção ao colidir com parede

            monster.frame += 0.1

            if monster.frame >= len(monter_frames):
                monster.frame = 0
            
            if monster.vx > 0:
                monster.image = monter_frames[int(monster.frame)]
            else:
                monster.image = monter_frames[int(monster.frame)] + 'e'

def on_mouse_down(pos):
    global SOUND_ON, GAME_STATE

    if start_button.collidepoint(pos):
        setup_game()
        GAME_STATE = 'game'

    elif exit_button.collidepoint(pos):
        quit()
    
    elif sound_button.collidepoint(pos):
        SOUND_ON = not SOUND_ON

        if SOUND_ON:
            sound_button.image = 'sound_on'
            sounds.crying_out_in_the_darkness.play(-1)
        else:
            sound_button.image = 'sound_off'
            sounds.crying_out_in_the_darkness.stop()
