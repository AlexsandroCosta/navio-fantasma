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
pirate = Actor('pirate/pirate-front')

walls = []
monsters = []
monter_frames = ['monster/monster1', 'monster/monster2', 'monster/monster3', 'monster/monster4', 'monster/monster5', 'monster/monster6']
treasures = []

pirate_frames = {
    'idle_down': 'pirate/pirate-front',
    'idle_up':   'pirate/pirate-back',
    'up': ['pirate/pirate-back1', 'pirate/pirate-back2'],
    'down': ['pirate/pirate-front1', 'pirate/pirate-front2'],
    'right': ['pirate/pirate1', 'pirate/pirate2', 'pirate/pirate3', 'pirate/pirate4'],
    'left':['pirate/pirate1e', 'pirate/pirate2e', 'pirate/pirate3e', 'pirate/pirate4e']
}

# Música de fundo
sounds.crying_out_in_the_darkness.play(-1)

def setup_game():
    for y, row in enumerate(GAME_MAP):
        for x, tile in enumerate(row):
            pos_x = MARGIN_X + x * TILE_SIZE + TILE_SIZE // 2
            pos_y = MARGIN_Y + y * TILE_SIZE + TILE_SIZE // 2

            if tile == '#':
                wall = Actor('bone', center=(pos_x, pos_y))
                wall.angle = 0
                walls.append(wall)
            elif tile == '|':
                wall = Actor('bone', center=(pos_x, pos_y))
                wall.angle = 90
                walls.append(wall)
            elif tile == 'm':
                monster = Actor('monster/monster', center=(pos_x, pos_y))
                monster.vx = 1
                monster.frame = 0
                monsters.append(monster)
            elif tile == 't':
                treasure = Actor('treasure', center=(pos_x, pos_y))
                treasures.append(treasure)
            elif tile == 'p':
                pirate.center = (pos_x, pos_y)
                pirate.direction = 'down'
                pirate.frame = 0
                pirate.image = pirate_frames['idle_down']

def draw_game():
    game_background.draw()
    
    for wall in walls:
        wall.draw()

    for monster in monsters:
        monster.draw()

    for treasure in treasures:
        treasure.draw()

    pirate.draw()

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

            if monster.collidelist(walls) != -1 or monster.collidelist(treasures) != -1 or monster.right > WIDTH or monster.left < 0 :
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

def animate_pirate():
    current_anim = pirate_frames[pirate.direction]

    # Verifica se é uma LISTA (animação de andar)
    if isinstance(current_anim, list):
        pirate.frame += 1
        pirate.frame = pirate.frame % len(current_anim)
        pirate.image = current_anim[int(pirate.frame)]
        
    # Se não for lista, é TEXTO (imagem parada)
    else:
        pirate.image = current_anim
        pirate.frame = 0

def on_key_down(key):
    global GAME_STATE, walls, monsters, treasures

    if GAME_STATE == 'game':
        moved = False

        if key == keys.S:
            pirate.y += TILE_SIZE/2
            pirate.direction = 'down'
            moved = True
        elif key == keys.W:
            pirate.y -= TILE_SIZE/2
            pirate.direction = 'up'
            moved = True
        elif key == keys.A:
            pirate.x -= TILE_SIZE/2
            pirate.direction = 'left'
            moved = True
        elif key == keys.D:
            pirate.x += TILE_SIZE/2
            pirate.direction = 'right'
            moved = True

        if moved:
            animate_pirate()
        
        if pirate.collidelist(walls) != -1 or pirate.right > WIDTH or pirate.left < 0 or pirate.bottom > HEIGHT-50 or pirate.top < 50:
            if key == keys.S:
                pirate.y -= TILE_SIZE/2
            elif key == keys.W:
                pirate.y += TILE_SIZE/2
            elif key == keys.A:
                pirate.x += TILE_SIZE/2
            elif key == keys.D:
                pirate.x -= TILE_SIZE/2

        if pirate.collidelist(monsters) != -1:
            sounds.male_death_sound.play()
            walls = []
            monsters = []
            treasures = []
            GAME_STATE = 'menu'

        if pirate.collidelist(treasures) != -1:
            sounds.short_success_sound_glockenspiel_treasure_video_game.play()
            
            collided_index = pirate.collidelist(treasures)
            del treasures[collided_index]

            if len(treasures) == 0:
                sounds.victory.play()
                walls = []
                monsters = []
                treasures = []
                GAME_STATE = 'menu'
            
def on_key_up(key):
    if GAME_STATE == 'game':
        
        if key == keys.W:
            pirate.direction = 'idle_up'
        elif key == keys.S:
            pirate.direction = 'idle_down'
        elif key == keys.A or key == keys.D:
            pirate.direction = 'idle_down'
        
        animate_pirate()