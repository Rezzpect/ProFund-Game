WIN_WIDTH = 640 #640/32 = 20 rows
WIN_HEIGHT = 480 #480/32 = 15 columns
TILESIZE = 32
FPS = 60

PLAYER_LAYER = 6
BLOCK_LAYER = 2
GROUND_LAYER = 1
ENEMY_LAYER = 4
TEXT_LAYER = 7
WARN_LAYER = 3
EN_ATK_LAYER = 5

PLAYER_SPEED = 3
ENEMY_SPEED = 2
BALL_SPEED = 5

RED = (255,0,0)
BLACK = (0,0,0)
BLUE = (0,0,255)
WHITE=(255,255,255)

#tilemap
tilemap =[
    '....................',
    '....................',
    '....................',
    '...BBB........BBB...',
    '...B............B...',
    '...B............B...',
    '..........P.........',
    '....................',
    '....................',
    '...B............B...',
    '...B............B...',
    '...BBB....V...BBB...',
    '....................',
    '....................',
    '....................',
    ]
#we doing wall surrounding out player we gonna let B represent a wall and . represent nothing and P represent a Player
#then we make a Block class which is basically a wall in sprite.py