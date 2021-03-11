import pygame, random, sys, os.path
from os import path

# initialize the pygame
pygame.init()
clock = pygame.time.Clock()

# colors
BLACK = (0,0,0)
YELLOW = (255,255,0)
GREEN = (0,200,0)
BRIGHT_GREEN = (0,255,0)
RED = (200,0,0)
BRIGHT_RED = (255,0,0)

# create the screen 
# HEIGHT = 800, WIDTH = 1000 and dont change
HEIGHT = 800 
WIDTH = 1000
SCREEN_SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(SCREEN_SIZE)
BACKGROUND_COLOR = BLACK

# intro
INTRO_BACKGROUND = (255,255,255)
IntroFont = pygame.font.SysFont("monospace", 60)
IntroStartEndFond = pygame.font.SysFont("monospace", 30)
START_COLOR = GREEN
MARKED_START_COLOR = BRIGHT_GREEN
QUIT_COLOR = RED
MARKED_QUIT_COLOR = BRIGHT_RED

# Title
pygame.display.set_caption("Walls Evading")

# Player
player_img = pygame.image.load('spaceship.png')
player_img_size = 64
player_size = 50
player_x = player_size
player_y = HEIGHT - 2*player_size
player_x_change = 0
player_y_change = 0
player_movement_speed = player_size / 20
player_pos = [player_x, player_y]

# Score
file_name = 'highest_score.txt'
highest_score = 0
if path.exists("highest_score.txt"):
    with open (file_name, 'r') as f:
        for line in f:
            tmp_list = line.split()
            highest_score = int(tmp_list[1])
else:
    f = open("highest_score.txt","w+")
    f.write('highest_score '+ str(0))
    f.close()
score = 0
ScoreFont = pygame.font.SysFont("monospace", 35)
SCORES_COLOR = YELLOW 

# Difficulty
difficulty_factor = 1.1
spot_change = 0 #'''used to increase lvl each 10 score'''


# Blocks:
BLOCK_COLOR = (255,0,0)
BLOCKS_SPEED = player_size / 40
B_HEIGHT = 50
block1_pos = [0,0]
block2_pos = [0,0]
gap = WIDTH / 2
MARGIN = 3


def player(player_pos):
    if legit_boundaries(player_pos[0],player_pos[1]):
        screen.blit(player_img, player_pos)

def blocks(score):
    if block1_pos[1] >= HEIGHT:
        score += 1
        block1_pos[1] = 0
        block2_pos[1] = 0
        global gap
        gap = random.randint(0,WIDTH-2*player_size)
    rect1 = (block1_pos[0], block1_pos[1], gap, player_size)
    block2_pos[0] = gap + MARGIN*player_size
    rect2 = (block2_pos[0], block2_pos[1], WIDTH-gap-MARGIN*player_size, player_size)
    pygame.draw.rect(screen, BLOCK_COLOR, rect1)
    pygame.draw.rect(screen, BLOCK_COLOR, rect2)
    return score

def fall_blocks():
    if block1_pos[1] <= HEIGHT and block2_pos[1] <= HEIGHT:
        block1_pos[1] += BLOCKS_SPEED 
        block2_pos[1] += BLOCKS_SPEED 

def legit_boundaries(x,y):
    if (x >= 0 and x <= WIDTH - player_img_size) and (y <= HEIGHT - player_img_size and y >= 0):
        return True
    return False

def detect_collision(player_pos,block1_pos,block2_pos):
    p_X = player_pos[0]
    p_Y = player_pos[1]
    b1_X = block1_pos[0]
    b1_Y = block1_pos[1]
    b2_X = block2_pos[0]
    b2_Y = block2_pos[1]

    if p_X >= 0 and p_X < b2_X - MARGIN*player_size or p_X > b2_X - player_size:
        if (b1_Y >= p_Y and b1_Y < p_Y + player_size) or (b1_Y <= p_Y and b1_Y + player_size > p_Y):
            return True 
    return False

def print_scores(score,highest_score):
    text1 = "Highest Score:" + str(highest_score)
    text2 = "Score:" + str(score)
    label_highest_score = ScoreFont.render(text1, 1, SCORES_COLOR)
    label_score = ScoreFont.render(text2, 1, SCORES_COLOR)
    screen.blit(label_highest_score, (WIDTH-350, HEIGHT-50))
    screen.blit(label_score, (WIDTH-183, HEIGHT-80))

def enhance_difficulty(score):
    global spot_change
    if score > 0 and score%10 == 0 and spot_change == 0:
        spot_change = 1
        return BLOCKS_SPEED*difficulty_factor
    if score % 10 == 9:
        spot_change = 0
    return BLOCKS_SPEED

def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
                break
        screen.fill(INTRO_BACKGROUND)
        intro_text = "-----Walls Evading-----"
        start_text = "Start"
        quit_text = "Quit"
        label = IntroFont.render(intro_text, 1, BACKGROUND_COLOR)
        label_start = IntroStartEndFond.render(start_text, 1, BACKGROUND_COLOR)
        label_quit = IntroStartEndFond.render(quit_text, 1, BACKGROUND_COLOR)
        screen.blit(label,(WIDTH/13,HEIGHT/3))
        start_x = WIDTH/8
        start_y = HEIGHT-HEIGHT/8
        start_len = 100
        quit_x = WIDTH - WIDTH/4
        quit_y = HEIGHT-HEIGHT/8
        quit_len = 100
        button_height = 50
        intro1 = button(start_text, start_x, start_y, start_len, button_height, START_COLOR, MARKED_START_COLOR, intro, "start")
        intro2 = button(quit_text, quit_x, quit_y, quit_len, button_height, QUIT_COLOR, MARKED_QUIT_COLOR, intro, "quit")
        if intro1 == False or intro2 == False:
            intro = False
        pygame.display.update()

def button(msg, x, y, w, h, ic, ac, intro, action = None):
    global game_over
    label = IntroStartEndFond.render(msg, 1, BACKGROUND_COLOR)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x,y,w,h))
        if click[0] == 1 and action != None:
            if action == "start":
                return False
            elif action == "quit":
                game_over = True
                return False
    else:
        pygame.draw.rect(screen, ic, (x,y,w,h))
    screen.blit(label, (x,y))
    return True

# Game Loop:
game_over = False 
game_intro()
while not game_over:
    screen.fill((0,0,0))
    player(player_pos)
    score = blocks(score)
    print_scores(score,highest_score)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True 
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -player_movement_speed   
            elif event.key == pygame.K_RIGHT:
                player_x_change = player_movement_speed            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0
    if legit_boundaries(player_pos[0] + player_x_change, player_pos[1] + player_y_change):
        player_pos[0] += player_x_change 
    fall_blocks()
    if detect_collision(player_pos,block1_pos,block2_pos):
        game_over = True
        if score > highest_score:
            with open (file_name, 'w') as f:
                f.write('highest_score '+str(score))

    BLOCKS_SPEED = enhance_difficulty(score)
    pygame.display.update()

