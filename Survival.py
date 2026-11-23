import os
import pgzrun
import pygame
from pgzero.actor import Actor
from pgzero.animation import animate
from random import randint
from datetime import datetime
import threading
import input
import map

# Set the environment variable to center the screen
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.mixer.init()

WIDTH = 600
HEIGHT = 660

player = Actor("pacman_o")
player.status = 0
SPEED = 5
pacDots = []
ghosts = []
moveGhostsFlag = 4
score = 0
lives = 3
start_time = datetime.now()
game_paused = False

# Load images and sounds
colourmap_image = pygame.image.load('images/colourmap.png')
blinky_image = pygame.transform.scale(pygame.image.load('images/survival4.png'), (600, 100))
eat_dot_sound = pygame.mixer.Sound('pacman_chomp.wav')
lose_life_sound = pygame.mixer.Sound('pacman-phonk-bounce.mp3')

# High score handling
high_score_file = "survival_highscore"
high_score = 0

# Read current high score from file
if os.path.exists(high_score_file):
    with open(high_score_file, 'r') as f:
        try:
            high_score = int(f.read().strip())
        except ValueError:
            high_score = 0

# Lock for thread-safe access to shared resources
lock = threading.Lock()

def draw():
    global pacDots, player, score, lives, start_time, game_paused, high_score
    screen.clear()
    screen.blit(blinky_image, (0, 0))
    screen.blit(colourmap_image, (0, 80))
    pacDotsLeft = 0
    for dot in pacDots:
        if dot.status == 0:
            dot.draw()
            pacDotsLeft += 1
        if dot.collidepoint((player.x, player.y)):
            dot.status = 1
            with lock:
                score += 10
                # Check for new high score
                if score > high_score:
                    high_score = score
            eat_dot_sound.play()
    if pacDotsLeft == 0:
        player.status = 2
    drawGhosts()
    getPlayerImage()
    player.draw()
    if player.status == 1:
        screen.draw.text("GAME OVER", center=(300, 480), owidth=0.5, ocolor=(255, 255, 255), color=(255, 64, 0), fontsize=60)
    if player.status == 2:
        screen.draw.text("YOU WIN!", center=(300, 484), owidth=0.5, ocolor=(255, 255, 255), color=(255, 64, 0), fontsize=60)

    # Draw the score and high score
    screen.draw.text(f"Score: {score}", topleft=(10, 10), fontsize=30, color=(255, 255, 255))
    screen.draw.text(f"High Score: {high_score}", topright=(590, 10), fontsize=30, color=(255, 255, 255))

    # Draw the lives
    screen.draw.text(f"Lives: {lives}", topright=(590, 50), fontsize=30, color=(255, 255, 255))

    # Draw the time elapsed
    elapsed_time = datetime.now() - start_time
    minutes, seconds = divmod(elapsed_time.seconds, 60)
    time_display = f"Time: {minutes:02}:{seconds:02}"
    screen.draw.text(time_display, topleft=(10, 50), fontsize=30, color=(255, 255, 255))

    if game_paused:
        screen.draw.text("PAUSED", center=(300, 330), fontsize=40, color=(255, 64, 0))
        screen.draw.text("P: Resume", center=(300, 370), fontsize=30, color=(255, 255, 255))
        screen.draw.text("R: Restart   Q: Quit", center=(300, 410), fontsize=30, color=(255, 255, 255))

def update():
    global player, moveGhostsFlag, ghosts, game_paused, lives
    if game_paused:
        return
    if player.status == 0:
        if moveGhostsFlag == 4:
            moveGhosts()
        collided = False
        for ghost in ghosts:
            if ghost.collidepoint((player.x, player.y)):
                collided = True
                break
        if collided:
            with lock:
                lives -= 1
            lose_life_sound.play()
            if lives > 0:
                reset_player_position()
            else:
                player.status = 1
        if player.inputActive:
            input.checkInput(player)
            map.checkMovePoint(player)
            if player.movex or player.movey:
                inputLock()
                animate(player, pos=(player.x + player.movex, player.y + player.movey), duration=1 / SPEED, tween='linear', on_finished=inputUnLock)

def on_key_down(key):
    global game_paused
    if key == keys.P:
        game_paused = not game_paused
    elif key == keys.R and game_paused:
        restart_game()
    elif key == keys.Q and game_paused:
        quit_game()

def reset_player_position():
    global player
    player.x = 290
    player.y = 570
    player.movex = player.movey = 0
    inputUnLock()

def restart_game():
    global player, score, lives, start_time, game_paused
    initDots()
    initGhosts()
    player.status = 0
    score = 0
    lives = 3
    start_time = datetime.now()
    game_paused = False
    reset_player_position()

def quit_game():
    # Write the high score to the file before quitting
    with open(high_score_file, 'w', encoding="utf-8") as file:
        file.write(str(high_score))
    raise SystemExit

def init():
    global player
    initDots()
    initGhosts()
    reset_player_position()
    inputUnLock()

def getPlayerImage():
    global player
    dt = datetime.now()
    a = player.angle
    tc = dt.microsecond % (500000 / SPEED) / (100000 / SPEED)
    if tc > 2.5 and (player.movex != 0 or player.movey != 0):
        if a != 180:
            player.image = "pacman_c"
        else:
            player.image = "pacman_cr"
    else:
        if a != 180:
            player.image = "pacman_o"
        else:
            player.image = "pacman_or"
    player.angle = a

def drawGhosts():
    for ghost in ghosts:
        if ghost.x > player.x:
            ghost.image = "ghost" + str(ghosts.index(ghost) + 1) + "r"
        else:
            ghost.image = "ghost" + str(ghosts.index(ghost) + 1)
        ghost.draw()

def moveGhosts():
    global moveGhostsFlag
    dmoves = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    moveGhostsFlag = 0
    for ghost in ghosts:
        dirs = map.getPossibleDirection(ghost)
        if ghostCollided(ghost) and randint(0, 3) == 0:
            ghost.dir = 3
        if dirs[ghost.dir] == 0 or randint(0, 50) == 0:
            d = -1
            while d == -1:
                rd = randint(0, 3)
                if dirs[rd] == 1:
                    d = rd
            ghost.dir = d
        animate(ghost, pos=(ghost.x + dmoves[ghost.dir][0] * 20, ghost.y + dmoves[ghost.dir][1] * 20), duration=1 / SPEED, tween='linear', on_finished=flagMoveGhosts)

def flagMoveGhosts():
    global moveGhostsFlag
    moveGhostsFlag += 1

def ghostCollided(ga):
    for ghost in ghosts:
        if ghost.colliderect(ga) and ghost != ga:
            return True
    return False

def initDots():
    global pacDots
    pacDots = []
    a = 0
    for x in range(30):
        for y in range(29):
            if map.checkDotPoint(10 + x * 20, 10 + y * 20):
                pacDots.append(Actor("dot", (10 + x * 20, 90 + y * 20)))
                pacDots[a].status = 0
                a += 1

def initGhosts():
    global ghosts, moveGhostsFlag
    moveGhostsFlag = 4
    ghosts = []
    for g in range(4):
        ghosts.append(Actor("ghost" + str(g + 1), (270 + (g * 20), 370)))
        ghosts[g].dir = randint(0, 3)

def inputLock():
    global player
    player.inputActive = False

def inputUnLock():
    global player
    player.movex = player.movey = 0
    player.inputActive = True

init()
pgzrun.go()
