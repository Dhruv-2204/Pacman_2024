# MULTIPLE png for pacman...leads to smoother mouth opening motion
import copy

import pygame 
from boards import boards
import math  # to draw arcs

pygame.init()
pygame.font.init()

SCREEN_WIDTH = 730
SCREEN_HEIGHT = 780
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA) #used to display pause menu
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
level = copy.deepcopy(boards)
color = "white"  # colour of walls
pi = math.pi
player_images = []
direction = 0
counter = 0
flicker = False  # make the big circles flicker

pause = False  # for pause menu
replay = False  # for restarting the game

valid_turns = [False, False, False, False]  # RIGHT, LEFT, UP, DOWN
direction_command = 0

# Size and Direction of Ghosts
# The ghosts are in a scrambled order
redG_x = 45
redG_y = 47
redG_direction = 2
pinkG_x = 642
pinkG_y = 645
pinkG_direction = 2
blueG_x = 350
blueG_y = 300
blueG_direction = 2
oranG_x = 350
oranG_y = 340
oranG_direction = 2

for i in range(1, 5):  # iterating the images
    # Scaling down the images
    player_images.append(pygame.transform.scale(pygame.image.load(f"assets/pacs/frame {i}.png"), (32, 32)))

# GHOST images
redG = pygame.transform.scale(pygame.image.load(f"assets/ghost_images/red.png"), (32, 32))
pinkG = pygame.transform.scale(pygame.image.load(f"assets/ghost_images/pink.png"), (32, 32))
blueG = pygame.transform.scale(pygame.image.load(f"assets/ghost_images/blue.png"), (32, 32))
oranG = pygame.transform.scale(pygame.image.load(f"assets/ghost_images/orange.png"), (32, 32))

ragedG = pygame.transform.scale(pygame.image.load(f"assets/ghost_images/powerup.png"), (32, 32))
DEADG = pygame.transform.scale(pygame.image.load(f"assets/ghost_images/dead.png"), (32, 32))

# starting position of tuPAC
player_x = 345
player_y = 523

player_speed = 2
score = 0

power_counter = 0
super_powerup = False
eaten_ghosts = [False, False, False, False]

# Ghosts targets...what tile they are aiming for
targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]
# Variables to check if they are dead or no
redG_dead = False
blueG_dead = False
pinkG_dead = False
oranG_dead = False
redG_box = False
blueG_box = False
pinkG_box = False
oranG_box = False

ghost_speeds = [2, 2, 2, 2]

startup_counter = 0
moving = False

lives = 3
game_over = False
game_won = False


class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direction, dead, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22  # ADJUSTMENT for ghosts
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.dead = dead
        self.direction = direction
        self.in_box = box
        self.id = id

        # variables needed as it is being used by tuPAC
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()

    def draw(self):

        if (not super_powerup and not self.dead) or (eaten_ghosts[self.id] and super_powerup and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))  # situation where we have to draw the normal ghosts
        elif super_powerup and not self.dead and not eaten_ghosts[self.id]:
            screen.blit(ragedG, (self.x_pos, self.y_pos))  # situation where we spooked mode
        else:
            screen.blit(DEADG, (self.x_pos, self.y_pos))  # situation where we are dead

        #  building a hitbox for ghosts...before collisions
        ghost_rect = pygame.rect.Rect((self.center_x - 16, self.center_y - 16), (32, 32))
        return ghost_rect

    def check_collisions(self):

        # Right, Left, Up, Down
        num1 = (SCREEN_HEIGHT - 50) // 32
        num2 = SCREEN_WIDTH // 30
        num3 = 11  # to correct end error...not actual size of GHOSTs
        self.turns = [False, False, False, False]
        if 0 < self.center_x // 30 < 29:
            # Checking if there is a ghost door
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            # checking if we can go left
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or (
                    level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (self.in_box or self.dead)):
                self.turns[1] = True
            # checking if we can go right
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or (
                    level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (self.in_box or self.dead)):
                self.turns[0] = True
            # Go Down
            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True
            # checking to go UP
            if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True

            # SCENARIOS FOR DIFFERENT DIRECTIONS
            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18: # checking if tuPAC is in the middle
                    if level[(self.center_y + num3)//num1][self.center_x//num2] < 3 \
                        or (level[(self.center_y + num3)//num1][self.center_x//num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True  # DOWN
                if level[(self.center_y - num3)//num1][self.center_x//num2] < 3 \
                        or (level[(self.center_y - num3)//num1][self.center_x//num2] == 9 and (
                            self.in_box or self.dead)):
                            self.turns[2] = True  # UP
                if 12 <= self.center_x % num1 <= 18:
                    if level[self.center_y//num1][(self.center_x - num2)//num2] < 3 \
                            or (level[self.center_y//num1][(self.center_x - num2)//num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True  # LEft
                    if level[self.center_y//num1][(self.center_x + num2)//num2] < 3 \
                            or (level[self.center_y//num1][(self.center_x + num2)//num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True  # LEft

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3)//num1][self.center_x//num2] < 3 \
                            or (level[(self.center_y + num3)//num1][self.center_x//num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True  # DOWN
                if level[(self.center_y - num3)//num1][self.center_x//num2] < 3 \
                        or (level[(self.center_y - num3)//num1][self.center_x//num2] == 9 and (
                        self.in_box or self.dead)):
                    self.turns[2] = True  # UP
                if 12 <= self.center_x % num1 <= 18:
                    if level[self.center_y//num1][(self.center_x - num3)//num2] < 3 \
                            or (level[self.center_y//num1][(self.center_x - num3)//num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True  # LEft
                    if level[self.center_y//num1][(self.center_x + num3)//num2] < 3 \
                            or (level[self.center_y//num1][(self.center_x + num3)//num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True  # LEft


        else:
            self.turns[0] = True
            self.turns[1] = True

        # Checking constantly if we are in the box
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480: # RECHECK...PARAMETERES OF GHOSTS
            self.in_box = True
        else:
            self.in_box = False


        return self.turns, self.in_box

    def move_red(self): # Movement pattern for red ghosts
        #  R, L, U, D
        # red will move whenever he is in advantage
        if self.direction == 0: # Going right...target is a pair of x/y coord
            if self.target[0] > self.x_pos and self.turns[0]: # keep going right as long as possible
                self.x_pos += self.speed
            elif not self.turns[0]: # means there is a collision to your right
                if self.target[1] > self.y_pos and self.turns[3]:  # target is below me and im able to turn down
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:  # target is higher and ive collided with something on the right
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:  # target is behind me and im allowed to go left
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            # Can still go right but target is not there
            elif self.turns[0]: # able to turn right
                if self.target[1] > self.y_pos and self.turns[3]: # target is below
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed # can go up and down ...but prioritisng right

        # Going left
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]: # check if we can go Down
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]: # going left and target is to my left...keep going left
                self.x_pos -= self.speed
            elif not self.turns[1]: # If collided with something
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]: # can go RIGHT right
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed # prioritising left

        # Go UP
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]: # already going up ..keep following target UP
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                # Up and Down checker
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]: # check if able to go DOWN
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]: # if target is right go Right
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]: # if target is left Go left
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed # Else keep going UP

        # Go Down
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]: # Check to see if we keep going DOWN
                self.y_pos += self.speed
            elif not self.turns[3]: # Not able to go down
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed # Go UPWARDS
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed # keep go DOWN

        # MOVE OUT OF SCREEEN
        if self.x_pos < -30:  # going off-screen to the left
            self.x_pos = SCREEN_WIDTH
        elif self.x_pos > SCREEN_WIDTH:
            self.x_pos -= 30

        # Return x/y position and direction
        return self.x_pos, self.y_pos, self.direction

    def move_orange(self): # Movement pattern for red ghosts
        #  R, L, U, D
        # orange will move whenever collide with wall//else go straight
        if self.direction == 0: # Going right...target is a pair of x/y coord
            if self.target[0] > self.x_pos and self.turns[0]: # keep going right as long as possible
                self.x_pos += self.speed
            elif not self.turns[0]: # means there is a collision to your right
                if self.target[1] > self.y_pos and self.turns[3]:  # target is below me and im able to turn down
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:  # target is higher and ive collided with something on the right
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:  # target is behind me and im allowed to go left
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            # Can still go right but target is not there
            elif self.turns[0]: # able to turn right
                self.x_pos += self.speed # can go up and down ...but prioritisng right

        # Going left
        elif self.direction == 1:

            if self.target[0] < self.x_pos and self.turns[1]: # going left and target is to my left...keep going left
                self.x_pos -= self.speed
            elif not self.turns[1]: # If collided with something
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]: # can go RIGHT right
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed # prioritising left

        # Go UP
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]: # already going up ..keep following target UP
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                # Up and Down checker
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]: # check if able to go DOWN
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed # Else keep going UP

        # Go Down
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]: # Check to see if we keep going DOWN
                self.y_pos += self.speed
            elif not self.turns[3]: # Not able to go down
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed # Go UPWARDS
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[3]:
                self.y_pos += self.speed # keep go DOWN

        # MOVE OUT OF SCREEEN
        if self.x_pos < -30:  # going off-screen to the left
            self.x_pos = SCREEN_WIDTH
        elif self.x_pos > SCREEN_WIDTH:
            self.x_pos -= 30

        # Return x/y position and direction
        return self.x_pos, self.y_pos, self.direction

    def move_blue(self): # Movement pattern for red ghosts
        #  R, L, U, D
        # blue will move down and up while chasing but turn left and right on colliding
        if self.direction == 0: # Going right...target is a pair of x/y coord
            if self.target[0] > self.x_pos and self.turns[0]: # keep going right as long as possible
                self.x_pos += self.speed
            elif not self.turns[0]: # means there is a collision to your right
                if self.target[1] > self.y_pos and self.turns[3]:  # target is below me and im able to turn down
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:  # target is higher and ive collided with something on the right
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:  # target is behind me and im allowed to go left
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            # Can still go right but target is not there
            elif self.turns[0]: # able to turn right
                if self.target[1] > self.y_pos and self.turns[3]: # target is below
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed # can go up and down ...but prioritisng right

        # Going left stays same as red
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]: # check if we can go Down
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]: # going left and target is to my left...keep going left
                self.x_pos -= self.speed
            elif not self.turns[1]: # If collided with something
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]: # can go RIGHT right
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed # prioritising left

        # Go UP
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]: # already going up ..keep following target UP
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                # Up and Down checker
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]: # check if able to go DOWN
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed # Else keep going UP as long we are able to

        # Go Down
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]: # Check to see if we keep going DOWN
                self.y_pos += self.speed
            elif not self.turns[3]: # Not able to go down
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed # Go UPWARDS
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                self.y_pos += self.speed  # keep go DOWN

        # MOVE OUT OF SCREEEN
        if self.x_pos < -30:  # going off-screen to the left
            self.x_pos = SCREEN_WIDTH
        elif self.x_pos > SCREEN_WIDTH:
            self.x_pos -= 30

        # Return x/y position and direction
        return self.x_pos, self.y_pos, self.direction

    def move_pink(self): # Movement pattern for red ghosts
        #  R, L, U, D
        # pink will turn left or right but up/down on collision
        if self.direction == 0: # Going right...target is a pair of x/y coord
            if self.target[0] > self.x_pos and self.turns[0]: # keep going right as long as possible
                self.x_pos += self.speed
            elif not self.turns[0]: # means there is a collision to your right
                if self.target[1] > self.y_pos and self.turns[3]:  # target is below me and im able to turn down
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:  # target is higher and ive collided with something on the right
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:  # target is behind me and im allowed to go left
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            # Can still go right but target is not there
            elif self.turns[0]: # able to turn right
                self.x_pos += self.speed # can go up and down ...but prioritisng right

        # Going left
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]: # check if we can go Down
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]: # going left and target is to my left...keep going left
                self.x_pos -= self.speed
            elif not self.turns[1]: # If collided with something
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]: # can go RIGHT right
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed # prioritising left

        # Go UP
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]: # already going up ..keep following target UP
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                # Up and Down checker
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]: # check if able to go DOWN
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]: # if target is right go Right
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]: # if target is left Go left
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed # Else keep going UP

        # Go Down
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]: # Check to see if we keep going DOWN
                self.y_pos += self.speed
            elif not self.turns[3]: # Not able to go down
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed # Go UPWARDS
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed # keep go DOWN

        # MOVE OUT OF SCREEEN
        if self.x_pos < -30:  # going off-screen to the left
            self.x_pos = SCREEN_WIDTH
        elif self.x_pos > SCREEN_WIDTH:
            self.x_pos -= 30

        # Return x/y position and direction
        return self.x_pos, self.y_pos, self.direction



def draw_miscellaneaous():
    score_text = font.render(f'SCORE: {score}', True, 'white')
    screen.blit(score_text, (110, SCREEN_HEIGHT - 40))
    if super_powerup:
        pygame.draw.circle(screen, 'cyan', (90, SCREEN_WIDTH + 18), 10)
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (25, 25)), (450 + i * 40, SCREEN_HEIGHT - 45))
    # Drawing the win/lose window
    if game_over:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Game over! Space bar to restart!', True, 'red')
        screen.blit(gameover_text, (100, 300))
    if game_won:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Victory! Space bar to restart!', True, 'green')
        screen.blit(gameover_text, (100, 300))

def check_collisions(score_1, power_count, super_power, eaten_ghost):
    num1 = (SCREEN_HEIGHT - 50) // 32
    num2 = SCREEN_WIDTH // 30

    # checking if it has eaten a cell
    if 0 < player_x < 730:
        if level[center_y // num1][center_x // num2] == 1:  # if its eating the small dot
            level[center_y // num1][center_x // num2] = 0  # then change it to a black spot after eating
            score_1 += 10
        if level[center_y // num1][center_x // num2] == 2:  # if its eating the small dot
            level[center_y // num1][center_x // num2] = 0  # then change it to a black spot after eating
            score_1 += 50
            super_power = True
            power_count = 0
            eaten_ghost = [False, False, False, False]

        # returning the live values
    return score_1, power_count, super_power, eaten_ghost

def draw_pause():
    pygame.draw.rect(surface,(128,128,128,150), [0,0, SCREEN_WIDTH,SCREEN_HEIGHT])
    pygame.draw.rect(surface, 'dark gray', [200 , 100 , 280, 50], 0, 10)
    reset = pygame.draw.rect(surface, 'white', [200 , 200 , 280, 50], 0, 10)
    exit = pygame.draw.rect(surface, 'white', [200 , 300 , 280, 50], 0, 10)
    surface.blit(font.render("Game Paused",True,'black'), (280,115))
    surface.blit(font.render("Restart",True,'black'), (310,215))
    surface.blit(font.render("Exit",True,'black'), (325,315))
    screen.blit(surface,(0,0))
    return reset, exit


def draw_board():
    # defining how high and wide each tiles would be
    num1 = ((SCREEN_HEIGHT - 50) // 32)  # TILE HEIGHT
    num2 = ((SCREEN_WIDTH) // 30)  # double slash for making integer when dividing

    for i in range(len(level)):  # iterate through every single row in the level
        for j in range(len(level[i])):  # iterate through every single column of that specific row
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'green', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'green', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 8)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                 (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)

            if level[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.45)), (i * num1 + (0.5 * num1)), num2, num1],
                                0, pi / 2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1],
                                pi / 2, pi, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color,
                                [(j * num2 + (num2 * 0.5)), (i * num1 - (0.45 * num1) + 1.5), num2, num1],
                                pi, (1.5 * pi), 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color,
                                [(j * num2 - (num2 * 0.5) + 1), (i * num1 - (0.4 * num1)) - 1, num2, num1],
                                (1.5 * pi), (2 * pi), 2)

            if level[i][j] == 9:
                pygame.draw.line(screen, "grey", (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)


def draw_player():
    if direction == 0:  # RIGHT
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))


def check_position(centerX, centerY):
    turns = [False, False, False, False]

    num1 = (SCREEN_HEIGHT - 50) // 32
    num2 = SCREEN_WIDTH // 30
    num3 = 11  # to correct end error...not actual size of tuPAC

    # check actual collisions based on center x and y +/- end ERROR
    if centerX // 30 < 29:  #  while not going through the walls

        # these 4 lines allow to turn backwards
        if direction == 0:  # RIGHT
            if level[centerY // num1][
                (centerX - num3) // num2] < 3:  # CHECKING IF piece right behind is black, small dot or big dot
                turns[1] = True  # opposite direction is TRUE
        if direction == 1:  # LEFT
            if level[centerY // num1][
                (centerX + num3) // num2] < 3:  # CHECKING IF piece right behind is black, small dot or big dot
                turns[0] = True
        if direction == 2:  # UP
            if level[(centerY + num3) // num1][
                centerX // num2] < 3:  # CHECKING IF piece right behind is black, small dot or big dot
                turns[3] = True
        if direction == 3:  # DOWN
            if level[(centerY - num3) // num1][
                centerX // num2] < 3:  # CHECKING IF piece right behind is black, small dot or big dot
                turns[2] = True

        # check if going up or down
        if direction == 2 or direction == 3:
            # Check we can turn UP and DOWN
            if 12 <= centerX % num2 <= 18:  # being roughly at the middle of a tile
                if level[(centerY + num3) // num1][
                    centerX // num2] < 3:  # if position that is directly below me is open... allow to turn DOWN
                    turns[3] = True  # DOWN
                if level[(centerY - num3) // num1][
                    centerX // num2] < 3:  # if position that is directly above me is open... allow to turn UP
                    turns[2] = True  # UP
            # Check we can turn LEFT and RIGHT
            if 12 <= centerY % num1 <= 18:  # being roughly at the middle of a tile
                if level[centerY // num1][(
                                                  centerX - num2) // num2] < 3:  # if position that is directly behind me is open... allow to turn LEFT
                    turns[1] = True  # LEFT
                if level[centerY // num1][(
                                                  centerX + num2) // num2] < 3:  # if position that is directly in front of me is open... allow to turn RIGHT
                    turns[0] = True  # RIGHT

        # check if going left or right
        if direction == 0 or direction == 1:
            # Check we can turn UP and DOWN
            if 12 <= centerX % num2 <= 18:  # being roughly at the middle of a tile
                if level[(centerY + num1) // num1][
                    centerX // num2] < 3:  # if position that is directly below me is open... allow to turn DOWN
                    turns[3] = True  # DOWN
                if level[(centerY - num1) // num1][
                    centerX // num2] < 3:  # if position that is directly above me is open... allow to turn UP
                    turns[2] = True  # UP
            # Check we can turn LEFT and RIGHT
            if 12 <= centerY % num1 <= 18:  # being roughly at the middle of a tile
                if level[centerY // num1][(
                                                  centerX - num3) // num2] < 3:  # num3 is used to simulate colliding with wall more longer/realistically
                    turns[1] = True  #  LEFT
                if level[centerY // num1][(
                                                  centerX + num3) // num2] < 3:  # if position that is directly in front of me is open... allow to turn RIGHT
                    turns[0] = True  #  RIGHT




    else:
        turns[0] = True
        turns[1] = True

    return turns


def move_player(play_x, play_y):
    # R, L, U, D

    if direction == 0 and valid_turns[0] and not pause:  # current direction is pointed right and we are allowed to go right
        play_x += player_speed
    elif direction == 1 and valid_turns[1] and not pause:  # LEFT
        play_x -= player_speed
    elif direction == 2 and valid_turns[2] and not pause:  # UP
        play_y -= player_speed
    elif direction == 3 and valid_turns[3] and not pause:  # Down...we increase it
        play_y += player_speed
    return play_x, play_y


def get_targets(red_x, red_y, pink_x, pink_y, blue_x, blue_y, oran_x, oran_y):
    
    # Get away from player if powerUP is active
    if player_x < SCREEN_WIDTH//2:
        runaway_x = SCREEN_WIDTH
    else:
        runaway_x = 0
    if player_y < SCREEN_HEIGHT//2:
        runaway_y = SCREEN_HEIGHT
    else:
        runaway_y = 0
    # return inside the grid jail
    return_target = (320,300)


    # IF powerUP on
    if super_powerup:
        if not red_ghost.dead and not eaten_ghosts[0]:
            redG_target = (runaway_x, runaway_y)
        elif not red_ghost.dead and eaten_ghosts[0]:
            if red_ghost.in_box:
                redG_target = (400, 100)
            else:
                redG_target = (player_x, player_y)
        else:
            redG_target = return_target
        if not blue_ghost.dead and not eaten_ghosts[1]:
            blueG_target = (player_x, runaway_y)
        elif not blue_ghost.dead and eaten_ghosts[2]:
            if blue_ghost.in_box:
                blueG_target = (400, 100)
            else:
                blueG_target = (player_x, player_y)
        else:
            blueG_target = return_target
        if not pink_ghost.dead and not eaten_ghosts[2]:
            pinkG_target = (runaway_x, player_y)
        elif not pink_ghost.dead and eaten_ghosts[2]:
            if pink_ghost.in_box:
                pinkG_target = (400, 100)
            else:
                pinkG_target = (player_x, player_y)
        else:
            pinkG_target = return_target
        if not orange_ghost.dead and not eaten_ghosts[3]:
            oranG_target = (450, 200)
        elif not orange_ghost.dead and eaten_ghosts[3]:
            if orange_ghost.in_box:
                oranG_target = (400, 100)
            else:
                oranG_target = (player_x, player_y)
        else:
            oranG_target = return_target

    else: # check if we are in the box or NOT
        if not red_ghost.dead:
            if red_ghost.in_box:
                # Get out of box
                redG_target = (350, 100)
            else:
                redG_target = (player_x, player_y)
        else:
            redG_target = return_target
        if not blue_ghost.dead:
            if blue_ghost.in_box:
                blueG_target = (350, 100)
            else:
                blueG_target = (player_x, player_y)
        else:
            blueG_target = return_target
        if not pink_ghost.dead:
            if pink_ghost.in_box:
                pinkG_target = (350, 100)
            else:
                pinkG_target = (player_x, player_y)
        else:
            pinkG_target = return_target
        if not orange_ghost.dead:
            if orange_ghost.in_box:
                oranG_target = (350, 100)
            else:
                oranG_target = (player_x, player_y)
        else:
            oranG_target = return_target



    # returning list of targets
    return [redG_target, blueG_target, pinkG_target, oranG_target]


run = True

while run:
    timer.tick(fps)

    # DOING STUFF RELATED TO time

    # this 4 lines control a 20 sec counter,,,,making tuPAC munch
    if counter < 19:
        counter += 1
        if counter > 6:
            flicker = False  # Make circles flicker for 3 sec
    else:
        counter = 0
        flicker = True

    # For powerup functionality
    if super_powerup and power_counter < 600:
        power_counter += 1
    elif super_powerup and power_counter >= 600:
        power_counter = 0
        super_powerup = False
        eaten_ghosts = [False, False, False, False]

    # Implementing a startup/ countdwon counter
    if startup_counter < 100 and not game_over and not game_won and not pause:
        moving = False
        startup_counter += 1
    else:
        moving = True




    screen.fill("black")  # BACKGROUND COLOUR
    draw_board()
    # Center/ midpoint of the tuPAC
    center_x = player_x + 17
    center_y = player_y + 17
    #pygame.draw.circle(screen, 'white', (center_x, center_y), 2)

    # increasing speed of ghost when dead and slowing it down during powerUP
    if super_powerup:
        ghost_speeds = [1, 1, 1, 1]
    else:
        ghost_speeds = [2, 2, 2, 2]
    # if eaten a ghosts, speed will be 2
    if eaten_ghosts[0]:
        ghost_speeds[0] = 2
    if eaten_ghosts[1]:
        ghost_speeds[1] = 2
    if eaten_ghosts[2]:
        ghost_speeds[2] = 2
    if eaten_ghosts[3]:
        ghost_speeds[3] = 2
    if redG_dead:
        ghost_speeds[0] = 4
    if blueG_dead:
        ghost_speeds[1] = 4
    if pinkG_dead:
        ghost_speeds[2] = 4
    if oranG_dead:
        ghost_speeds[3] = 4

    draw_player()

    # to know the player hit box
    player_circle = pygame.draw.circle(screen, 'black', (center_x, center_y), 16, 2)

    red_ghost = Ghost(redG_x, redG_y, targets[0], ghost_speeds[0], redG, redG_direction, redG_dead, redG_box, 0)
    pink_ghost = Ghost(pinkG_x, pinkG_y, targets[0], ghost_speeds[1], pinkG, pinkG_direction, pinkG_dead, pinkG_box, 0)
    blue_ghost = Ghost(blueG_x, blueG_y, targets[0], ghost_speeds[2], blueG, blueG_direction, blueG_dead, blueG_box, 0)
    orange_ghost = Ghost(oranG_x, oranG_y, targets[0], ghost_speeds[3], oranG, oranG_direction, oranG_dead, oranG_box, 0)

    draw_miscellaneaous()
    targets = get_targets(redG_x, redG_y, pinkG_x, pinkG_y, blueG_x, blueG_y, oranG_x, oranG_y)



    # To know valid turns
    valid_turns = check_position(center_x, center_y)

    # if moving is true at the start of the GAME after 3 sec counter...get 3 sec to regather after being eaten
    if moving and not pause:
        player_x, player_y = move_player(player_x, player_y)
        if not redG_dead and not red_ghost.in_box: # scenario when ghosts roaming around
            redG_x, redG_y, redG_direction = red_ghost.move_red()
        else:
            redG_x, redG_y, redG_direction = red_ghost.move_orange()
        if not blueG_dead and not blue_ghost.in_box:
            blueG_x, blueG_y, blueG_direction = blue_ghost.move_blue()
        else:
            blueG_x, blueG_y, blueG_direction = blue_ghost.move_orange()
        if not pinkG_dead and not pink_ghost.in_box:
            pinkG_x, pinkG_y, pinkG_direction = pink_ghost.move_pink()
        else:
            pinkG_x, pinkG_y, pinkG_direction = pink_ghost.move_orange()

        oranG_x, oranG_y, oranG_direction = orange_ghost.move_red()

    score, power_counter, super_powerup, eaten_ghosts = check_collisions(score, power_counter, super_powerup,eaten_ghosts)

    # TO KNOW WHEN player hit box hits a ghost // collisions + EATING THEM
    if not super_powerup:
        if (player_circle.colliderect(red_ghost.rect) and not red_ghost.dead) or \
            (player_circle.colliderect(blue_ghost.rect) and not blue_ghost.dead) or \
            (player_circle.colliderect(pink_ghost.rect) and not pink_ghost.dead) or \
            (player_circle.colliderect(orange_ghost.rect) and not orange_ghost.dead) :
            # life checker
            if lives > 0:
                super_powerup = False
                power_counter = 0
                # CAN USE A FUNCTION FOR REPETITIVE THINGS
                lives -= 1
                startup_counter = 0 # reset counter

            # reset everything else positing/direction
                player_x = 345
                player_y = 523
                direction = 0
                direction_command = 0
                redG_x = 45
                redG_y = 47
                redG_direction = 2
                pinkG_x = 642
                pinkG_y = 645
                pinkG_direction = 2
                blueG_x = 350
                blueG_y = 300
                blueG_direction = 2
                oranG_x = 350
                oranG_y = 340
                oranG_direction = 2
                # reset death commands
                eaten_ghosts = [False, False, False, False]
                redG_dead = False
                blueG_dead = False
                pinkG_dead = False
                oranG_dead = False
    if super_powerup and player_circle.colliderect(red_ghost.rect) and eaten_ghosts[0] and not red_ghost.dead:
        if lives > 0:
            super_powerup = False
            power_counter = 0
            # CAN USE A FUNCTION FOR REPETITIVE THINGS
            lives -= 1
            startup_counter = 0 # reset counter

            # reset everything else positing/direction
            player_x = 345
            player_y = 523
            direction = 0
            direction_command = 0
            redG_x = 45
            redG_y = 47
            redG_direction = 2
            pinkG_x = 642
            pinkG_y = 645
            pinkG_direction = 2
            blueG_x = 350
            blueG_y = 300
            blueG_direction = 2
            oranG_x = 350
            oranG_y = 340
            oranG_direction = 2
            # reset death commands
            eaten_ghosts = [False, False, False, False]
            redG_dead = False
            blueG_dead = False
            pinkG_dead = False
            oranG_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0

    if super_powerup and player_circle.colliderect(blue_ghost.rect) and eaten_ghosts[1] and not blue_ghost.dead:
        if lives > 0:

            super_powerup = False
            power_counter = 0
            # CAN USE A FUNCTION FOR REPETITIVE THINGS
            lives -= 1
            startup_counter = 0 # reset counter

            # reset everything else positing/direction
            player_x = 345
            player_y = 523
            direction = 0
            direction_command = 0
            redG_x = 45
            redG_y = 47
            redG_direction = 2
            pinkG_x = 642
            pinkG_y = 645
            pinkG_direction = 2
            blueG_x = 350
            blueG_y = 300
            blueG_direction = 2
            oranG_x = 350
            oranG_y = 340
            oranG_direction = 2
            # reset death commands
            eaten_ghosts = [False, False, False, False]
            redG_dead = False
            blueG_dead = False
            pinkG_dead = False
            oranG_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0

    if super_powerup and player_circle.colliderect(pink_ghost.rect) and eaten_ghosts[2] and not pink_ghost.dead:
        if lives > 0:
            super_powerup = False
            power_counter = 0
            # CAN USE A FUNCTION FOR REPETITIVE THINGS
            lives -= 1
            startup_counter = 0 # reset counter

            # reset everything else positing/direction
            player_x = 345
            player_y = 523
            direction = 0
            direction_command = 0
            redG_x = 45
            redG_y = 47
            redG_direction = 2
            pinkG_x = 642
            pinkG_y = 645
            pinkG_direction = 2
            blueG_x = 350
            blueG_y = 300
            blueG_direction = 2
            oranG_x = 350
            oranG_y = 340
            oranG_direction = 2
            # reset death commands
            eaten_ghosts = [False, False, False, False]
            redG_dead = False
            blueG_dead = False
            pinkG_dead = False
            oranG_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0

    if super_powerup and player_circle.colliderect(orange_ghost.rect) and eaten_ghosts[3] and not orange_ghost.dead:
        if lives > 0:
            super_powerup = False
            power_counter = 0
            # CAN USE A FUNCTION FOR REPETITIVE THINGS
            lives -= 1
            startup_counter = 0 # reset counter

            # reset everything else positing/direction
            player_x = 345
            player_y = 523
            direction = 0
            direction_command = 0
            redG_x = 45
            redG_y = 47
            redG_direction = 2
            pinkG_x = 642
            pinkG_y = 645
            pinkG_direction = 2
            blueG_x = 350
            blueG_y = 300
            blueG_direction = 2
            oranG_x = 350
            oranG_y = 340
            oranG_direction = 2
            # reset death commands
            eaten_ghosts = [False, False, False, False]
            redG_dead = False
            blueG_dead = False
            pinkG_dead = False
            oranG_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0

    if super_powerup and player_circle.colliderect(red_ghost.rect) and not red_ghost.dead and not eaten_ghosts[0]:
        redG_dead = True
        eaten_ghosts[0] = True
        # Incrementing the score when eating a ghost during powerUP
        score += (2 ** eaten_ghosts.count(True)) * 100  # 2 raised to the power of counter times 100
    if super_powerup and player_circle.colliderect(blue_ghost.rect) and not blue_ghost.dead and not eaten_ghosts[1]:
        blueG_dead = True
        eaten_ghosts[1] = True
        score += (2 ** eaten_ghosts.count(True)) * 100  # 2 raised to the power of counter times 100
    if super_powerup and player_circle.colliderect(pink_ghost.rect) and not pink_ghost.dead and not eaten_ghosts[2]:
        pinkG_dead = True
        eaten_ghosts[2] = True
        score += (2 ** eaten_ghosts.count(True)) * 100
    if super_powerup and player_circle.colliderect(orange_ghost.rect) and not orange_ghost.dead and not eaten_ghosts[3]:
        oranG_dead = True
        eaten_ghosts[3] = True
        score += (2 ** eaten_ghosts.count(True)) * 100
        
    if pause: 
        restart, exit = draw_pause() #calls draw_pause function for pause menu

    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            run = False
            
        #if player clicks on restart or exit button in pause menu
        if event.type == pygame.MOUSEBUTTONDOWN and pause:
            if exit.collidepoint(event.pos):
                pygame.quit()
            
            if restart.collidepoint(event.pos):
                replay = True
            else:
                replay = False
                
        # CHECKING ANYTIME a button is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d and not pause:
                direction_command = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_a and not pause:
                direction_command = 1
            if event.key == pygame.K_UP or event.key == pygame.K_w and not pause:
                direction_command = 2
            if event.key == pygame.K_DOWN or event.key == pygame.K_s and not pause:
                direction_command = 3
                
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                if pause:
                    pause = False
                else:
                    pause = True      
                    
            # SPACE BAR TO RESTART
            if ( event.key == pygame.K_SPACE and (game_over or game_won) ) or replay:
                super_powerup = False
                power_counter = 0
                # CAN USE A FUNCTION FOR REPETITIVE THINGS
                lives -= 1
                startup_counter = 0 # reset counter

                # reset everything else positing/direction
                player_x = 345
                player_y = 523
                direction = 0
                direction_command = 0
                redG_x = 45
                redG_y = 47
                redG_direction = 2
                pinkG_x = 642
                pinkG_y = 645
                pinkG_direction = 2
                blueG_x = 350
                blueG_y = 300
                blueG_direction = 2
                oranG_x = 350
                oranG_y = 340
                oranG_direction = 2
                # reset death commands
                eaten_ghosts = [False, False, False, False]
                redG_dead = False
                blueG_dead = False
                pinkG_dead = False
                oranG_dead = False
                score = 0
                lives = 3
                level = copy.deepcopy(boards)  # reset the board
                game_won = False
                game_over = False
                pause = False

        # Gives a joystick feeling...continual movement
        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction_command == 0:  # continue
                direction_command = direction
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction_command == 1:
                direction_command = direction
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and direction_command == 2:
                direction_command = direction
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction_command == 3:
                direction_command = direction

    # more like joystick personality

    if direction_command == 0 and valid_turns[0]:  # checking if the direction and valid_turn is the same to allow movement
        direction = 0
    if direction_command == 1 and valid_turns[1]:
        direction = 1
    if direction_command == 2 and valid_turns[2]:
        direction = 2
    if direction_command == 3 and valid_turns[3]:
        direction = 3

    # When tuPAC moves outside the screen
    if player_x > SCREEN_WIDTH:
        player_x = -32
    elif player_x < -32:
        player_x = SCREEN_WIDTH - 10

    # when ghosts go inside box..they are no longer dead
    if red_ghost.in_box and red_ghost.dead:
        redG_dead = False
    if blue_ghost.in_box and blue_ghost.dead:
        pinkG_dead = False
    if pink_ghost.in_box and pink_ghost.dead:
        blueG_dead = False
    if orange_ghost.in_box and orange_ghost.dead:
        oranG_dead = False

    pygame.display.flip()
pygame.quit()


# Check going out of box....
# USE FUNCTION FOR REPETITIVE THINGS LIKE lives > 0