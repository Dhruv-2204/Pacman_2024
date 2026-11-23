#CREATED BY: DHRUV RAMACHUNDRAh (M01012616), AAYUSH LOCHUN (M01004726), NIVESH HURRILL (M01013576)
#cREATED ON:29/05/2024
#LAST MODFIED:15/07/2024

import sys
import tkinter as tk
from tkinter import *
import itertools

#import Int
from PIL import Image, ImageTk
import time


# IMPORT FOR CLASSIC
from boards import boards
import math


# IMPORT FOR INTERMEDIATE
from random import randrange
import random
import copy


# IMPORT FOR SURVIVAL
import os
import pgzrun
import pygame
from pgzero.actor import Actor
from pgzero.animation import animate
from random import randint
from datetime import datetime
import threading
import subprocess
import input
import map

# DECLARATION OF PYGAME MODULE
pygame.init()
image_list = []
gif_duration = 0

# DECLARATION AND INITIALISATION OF HIGHSCORE LIST
h1score = [0]
h2score = [0]
h3score = [0]


# CLASS FOR BOUNCING EMOTES ANIMATION
class bounceI:

    # DECLARATION OF FUNCTION FOR EMOTES
    def __init__(self, canvas, xc, yc, xcspeed, ycspeed, imgfile):
        self.canvas = canvas
        self.photo_img = tk.PhotoImage(file=imgfile)
        self.image = canvas.create_image(xc, yc, image=self.photo_img, anchor=tk.NW)
        self.xcspeed = xcspeed
        self.ycspeed = ycspeed
        self.stop_event = threading.Event()

    # DECLARATION OF FUNCTION TO MOVE EMOTES
    def move(self):
        if self.stop_event.is_set():
            return

        coordinates = self.canvas.coords(self.image)
        if coordinates and (
            coordinates[0] + self.photo_img.width() >= self.canvas.winfo_width()
            or coordinates[0] < 0
        ):
            self.xcspeed = -self.xcspeed
        if coordinates and (
            coordinates[1] + self.photo_img.height() >= self.canvas.winfo_height()
            or coordinates[1] < 0
        ):
            self.ycspeed = -self.ycspeed

        self.canvas.move(self.image, self.xcspeed, self.ycspeed)
        self.canvas.after(10, self.move)

    # DECLARATION OF FUNCTION FOR STARTING ANIMATION
    def threadmove(self):
        self.move()

    # DECLARATION OF FUNCTION TO STOP ANIMATION
    def stop(self):
        self.stop_event.set()


# DECLARATION OF FUNCTION FOR CLASSIC MODE
def classic():
    pacman.withdraw()
    # DECLARATION OF PYGAME MODULE
    pygame.init()
    pygame.font.init()

    # INITIALISATION OF SCREEN SIZE
    SCREEN_WIDTH = 730
    SCREEN_HEIGHT = 780
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)  # used to display pause menu
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
                        level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                        self.in_box or self.dead)):
                    self.turns[1] = True
                # checking if we can go right
                if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                        or (
                        level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                        self.in_box or self.dead)):
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
                    if 12 <= self.center_x % num2 <= 18:  # checking if tuPAC is in the middle
                        if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                                or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                                self.in_box or self.dead)):
                            self.turns[3] = True  # DOWN
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True  # UP
                    if 12 <= self.center_x % num1 <= 18:
                        if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                                or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (
                                self.in_box or self.dead)):
                            self.turns[1] = True  # LEft
                        if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                                or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (
                                self.in_box or self.dead)):
                            self.turns[0] = True  # LEft

                if self.direction == 0 or self.direction == 1:
                    if 12 <= self.center_x % num2 <= 18:
                        if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                                or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                                self.in_box or self.dead)):
                            self.turns[3] = True  # DOWN
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True  # UP
                    if 12 <= self.center_x % num1 <= 18:
                        if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                                or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                                self.in_box or self.dead)):
                            self.turns[1] = True  # LEft
                        if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                                or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                                self.in_box or self.dead)):
                            self.turns[0] = True  # LEft


            else:
                self.turns[0] = True
                self.turns[1] = True

            # Checking constantly if we are in the box
            if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:  # RECHECK...PARAMETERES OF GHOSTS
                self.in_box = True
            else:
                self.in_box = False

            return self.turns, self.in_box

        def move_red(self):  # Movement pattern for red ghosts
            #  R, L, U, D
            # red will move whenever he is in advantage
            if self.direction == 0:  # Going right...target is a pair of x/y coord
                if self.target[0] > self.x_pos and self.turns[0]:  # keep going right as long as possible
                    self.x_pos += self.speed
                elif not self.turns[0]:  # means there is a collision to your right
                    if self.target[1] > self.y_pos and self.turns[3]:  # target is below me and im able to turn down
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.target[1] < self.y_pos and self.turns[
                        2]:  # target is higher and ive collided with something on the right
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
                elif self.turns[0]:  # able to turn right
                    if self.target[1] > self.y_pos and self.turns[3]:  # target is below
                        self.direction = 3
                        self.y_pos += self.speed
                    if self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    else:
                        self.x_pos += self.speed  # can go up and down ...but prioritisng right

            # Going left
            elif self.direction == 1:
                if self.target[1] > self.y_pos and self.turns[3]:  # check if we can go Down
                    self.direction = 3
                elif self.target[0] < self.x_pos and self.turns[
                    1]:  # going left and target is to my left...keep going left
                    self.x_pos -= self.speed
                elif not self.turns[1]:  # If collided with something
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.target[0] > self.x_pos and self.turns[0]:  # can go RIGHT right
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
                        self.x_pos -= self.speed  # prioritising left

            # Go UP
            elif self.direction == 2:
                if self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:  # already going up ..keep following target UP
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
                    elif self.target[1] > self.y_pos and self.turns[3]:  # check if able to go DOWN
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
                    if self.target[0] > self.x_pos and self.turns[0]:  # if target is right go Right
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:  # if target is left Go left
                        self.direction = 1
                        self.x_pos -= self.speed
                    else:
                        self.y_pos -= self.speed  # Else keep going UP

            # Go Down
            elif self.direction == 3:
                if self.target[1] > self.y_pos and self.turns[3]:  # Check to see if we keep going DOWN
                    self.y_pos += self.speed
                elif not self.turns[3]:  # Not able to go down
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed  # Go UPWARDS
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
                        self.y_pos += self.speed  # keep go DOWN

            # MOVE OUT OF SCREEEN
            if self.x_pos < -30:  # going off-screen to the left
                self.x_pos = SCREEN_WIDTH
            elif self.x_pos > SCREEN_WIDTH:
                self.x_pos -= 30

            # Return x/y position and direction
            return self.x_pos, self.y_pos, self.direction

        def move_orange(self):  # Movement pattern for red ghosts
            #  R, L, U, D
            # orange will move whenever collide with wall//else go straight
            if self.direction == 0:  # Going right...target is a pair of x/y coord
                if self.target[0] > self.x_pos and self.turns[0]:  # keep going right as long as possible
                    self.x_pos += self.speed
                elif not self.turns[0]:  # means there is a collision to your right
                    if self.target[1] > self.y_pos and self.turns[3]:  # target is below me and im able to turn down
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.target[1] < self.y_pos and self.turns[
                        2]:  # target is higher and ive collided with something on the right
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
                elif self.turns[0]:  # able to turn right
                    self.x_pos += self.speed  # can go up and down ...but prioritisng right

            # Going left
            elif self.direction == 1:

                if self.target[0] < self.x_pos and self.turns[
                    1]:  # going left and target is to my left...keep going left
                    self.x_pos -= self.speed
                elif not self.turns[1]:  # If collided with something
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.target[0] > self.x_pos and self.turns[0]:  # can go RIGHT right
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
                    self.x_pos -= self.speed  # prioritising left

            # Go UP
            elif self.direction == 2:
                if self.target[1] < self.y_pos and self.turns[2]:  # already going up ..keep following target UP
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
                    elif self.target[1] > self.y_pos and self.turns[3]:  # check if able to go DOWN
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
                    self.y_pos -= self.speed  # Else keep going UP

            # Go Down
            elif self.direction == 3:
                if self.target[1] > self.y_pos and self.turns[3]:  # Check to see if we keep going DOWN
                    self.y_pos += self.speed
                elif not self.turns[3]:  # Not able to go down
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed  # Go UPWARDS
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
                    self.y_pos += self.speed  # keep go DOWN

            # MOVE OUT OF SCREEEN
            if self.x_pos < -30:  # going off-screen to the left
                self.x_pos = SCREEN_WIDTH
            elif self.x_pos > SCREEN_WIDTH:
                self.x_pos -= 30

            # Return x/y position and direction
            return self.x_pos, self.y_pos, self.direction

        def move_blue(self):  # Movement pattern for red ghosts
            #  R, L, U, D
            # blue will move down and up while chasing but turn left and right on colliding
            if self.direction == 0:  # Going right...target is a pair of x/y coord
                if self.target[0] > self.x_pos and self.turns[0]:  # keep going right as long as possible
                    self.x_pos += self.speed
                elif not self.turns[0]:  # means there is a collision to your right
                    if self.target[1] > self.y_pos and self.turns[3]:  # target is below me and im able to turn down
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.target[1] < self.y_pos and self.turns[
                        2]:  # target is higher and ive collided with something on the right
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
                elif self.turns[0]:  # able to turn right
                    if self.target[1] > self.y_pos and self.turns[3]:  # target is below
                        self.direction = 3
                        self.y_pos += self.speed
                    if self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    else:
                        self.x_pos += self.speed  # can go up and down ...but prioritisng right

            # Going left stays same as red
            elif self.direction == 1:
                if self.target[1] > self.y_pos and self.turns[3]:  # check if we can go Down
                    self.direction = 3
                elif self.target[0] < self.x_pos and self.turns[
                    1]:  # going left and target is to my left...keep going left
                    self.x_pos -= self.speed
                elif not self.turns[1]:  # If collided with something
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.target[0] > self.x_pos and self.turns[0]:  # can go RIGHT right
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
                        self.x_pos -= self.speed  # prioritising left

            # Go UP
            elif self.direction == 2:
                if self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:  # already going up ..keep following target UP
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
                    elif self.target[1] > self.y_pos and self.turns[3]:  # check if able to go DOWN
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
                    self.y_pos -= self.speed  # Else keep going UP as long we are able to

            # Go Down
            elif self.direction == 3:
                if self.target[1] > self.y_pos and self.turns[3]:  # Check to see if we keep going DOWN
                    self.y_pos += self.speed
                elif not self.turns[3]:  # Not able to go down
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed  # Go UPWARDS
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

        def move_pink(self):  # Movement pattern for red ghosts
            #  R, L, U, D
            # pink will turn left or right but up/down on collision
            if self.direction == 0:  # Going right...target is a pair of x/y coord
                if self.target[0] > self.x_pos and self.turns[0]:  # keep going right as long as possible
                    self.x_pos += self.speed
                elif not self.turns[0]:  # means there is a collision to your right
                    if self.target[1] > self.y_pos and self.turns[3]:  # target is below me and im able to turn down
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.target[1] < self.y_pos and self.turns[
                        2]:  # target is higher and ive collided with something on the right
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
                elif self.turns[0]:  # able to turn right
                    self.x_pos += self.speed  # can go up and down ...but prioritisng right

            # Going left
            elif self.direction == 1:
                if self.target[1] > self.y_pos and self.turns[3]:  # check if we can go Down
                    self.direction = 3
                elif self.target[0] < self.x_pos and self.turns[
                    1]:  # going left and target is to my left...keep going left
                    self.x_pos -= self.speed
                elif not self.turns[1]:  # If collided with something
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.target[0] > self.x_pos and self.turns[0]:  # can go RIGHT right
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
                    self.x_pos -= self.speed  # prioritising left

            # Go UP
            elif self.direction == 2:
                if self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:  # already going up ..keep following target UP
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
                    elif self.target[1] > self.y_pos and self.turns[3]:  # check if able to go DOWN
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
                    if self.target[0] > self.x_pos and self.turns[0]:  # if target is right go Right
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:  # if target is left Go left
                        self.direction = 1
                        self.x_pos -= self.speed
                    else:
                        self.y_pos -= self.speed  # Else keep going UP

            # Go Down
            elif self.direction == 3:
                if self.target[1] > self.y_pos and self.turns[3]:  # Check to see if we keep going DOWN
                    self.y_pos += self.speed
                elif not self.turns[3]:  # Not able to go down
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed  # Go UPWARDS
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
                        self.y_pos += self.speed  # keep go DOWN

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
        controls_text = font.render('P / ESC: PAUSE', True, 'white')
        screen.blit(controls_text, (520, SCREEN_HEIGHT - 40))
        if super_powerup:
            pygame.draw.circle(screen, 'cyan', (90, SCREEN_WIDTH + 18), 10)
        for i in range(lives):
            screen.blit(pygame.transform.scale(player_images[0], (25, 25)), (450 + i * 40, SCREEN_HEIGHT - 45))
        # Drawing the win/lose window
        if game_over:
            pygame.draw.rect(screen, 'white', [50, 200, 800, 300], 0, 10)
            pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
            gameover_text = font.render('Game over! Space bar to restart!', True, 'red')
            screen.blit(gameover_text, (100, 300))
        if game_won:
            pygame.draw.rect(screen, 'white', [50, 200, 800, 300], 0, 10)
            pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
            gameover_text = font.render('Victory! Space bar to restart!', True, 'green')
            screen.blit(gameover_text, (100, 300))

    def check_collisions(score_1, power_count, super_power, eaten_ghost):
        num1 = (SCREEN_HEIGHT - 50) // 32
        num2 = SCREEN_WIDTH // 30

        # checking if it has eaten a cell
        if 0 < player_x < 730:
            row = min(max(center_y // num1, 0), len(level) - 1)
            col = min(max(center_x // num2, 0), len(level[row]) - 1)
            if level[row][col] == 1:  # if its eating the small dot
                level[row][col] = 0  # then change it to a black spot after eating
                score_1 += 10
            if level[row][col] == 2:  # if its eating the small dot
                level[row][col] = 0  # then change it to a black spot after eating
                score_1 += 50
                super_power = True
                power_count = 0
                eaten_ghost = [False, False, False, False]

            # returning the live values
        return score_1, power_count, super_power, eaten_ghost

    def draw_pause():
        pygame.draw.rect(surface, (128, 128, 128, 150), [0, 0, SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.draw.rect(surface, 'dark gray', [200, 100, 280, 50], 0, 10)
        reset = pygame.draw.rect(surface, 'white', [200, 200, 280, 50], 0, 10)
        exit = pygame.draw.rect(surface, 'white', [200, 300, 280, 50], 0, 10)
        surface.blit(font.render("Game Paused", True, 'black'), (280, 115))
        surface.blit(font.render("Restart", True, 'black'), (310, 215))
        surface.blit(font.render("Exit", True, 'black'), (325, 315))
        screen.blit(surface, (0, 0))
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

        centerX = min(max(centerX, 0), SCREEN_WIDTH - 1)
        centerY = min(max(centerY, 0), SCREEN_HEIGHT - 1)
        row = centerY // num1
        col = centerX // num2

        def open_at(target_row, target_col):
            if target_row < 0 or target_row >= len(level):
                return False
            if target_col < 0 or target_col >= len(level[target_row]):
                return False
            return level[target_row][target_col] < 3

        if open_at(row, col + 1):
            turns[0] = True
        if open_at(row, col - 1):
            turns[1] = True
        if open_at(row - 1, col):
            turns[2] = True
        if open_at(row + 1, col):
            turns[3] = True

        if direction == 0:
            turns[1] = open_at(row, col - 1)
        elif direction == 1:
            turns[0] = open_at(row, col + 1)
        elif direction == 2:
            turns[3] = open_at(row + 1, col)
        elif direction == 3:
            turns[2] = open_at(row - 1, col)

        return turns

    def move_player(play_x, play_y):
        # R, L, U, D

        if direction == 0 and valid_turns[
            0] and not pause:  # current direction is pointed right and we are allowed to go right
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
        if player_x < SCREEN_WIDTH // 2:
            runaway_x = SCREEN_WIDTH
        else:
            runaway_x = 0
        if player_y < SCREEN_HEIGHT // 2:
            runaway_y = SCREEN_HEIGHT
        else:
            runaway_y = 0
        # return inside the grid jail
        return_target = (320, 300)

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

        else:  # check if we are in the box or NOT
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
        # pygame.draw.circle(screen, 'white', (center_x, center_y), 2)

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
        pink_ghost = Ghost(pinkG_x, pinkG_y, targets[0], ghost_speeds[1], pinkG, pinkG_direction, pinkG_dead, pinkG_box,
                           0)
        blue_ghost = Ghost(blueG_x, blueG_y, targets[0], ghost_speeds[2], blueG, blueG_direction, blueG_dead, blueG_box,
                           0)
        orange_ghost = Ghost(oranG_x, oranG_y, targets[0], ghost_speeds[3], oranG, oranG_direction, oranG_dead,
                             oranG_box, 0)

        draw_miscellaneaous()
        targets = get_targets(redG_x, redG_y, pinkG_x, pinkG_y, blueG_x, blueG_y, oranG_x, oranG_y)

        # To know valid turns
        valid_turns = check_position(center_x, center_y)

        # if moving is true at the start of the GAME after 3 sec counter...get 3 sec to regather after being eaten
        if moving and not pause:
            player_x, player_y = move_player(player_x, player_y)
            if not redG_dead and not red_ghost.in_box:  # scenario when ghosts roaming around
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

        score, power_counter, super_powerup, eaten_ghosts = check_collisions(score, power_counter, super_powerup,
                                                                             eaten_ghosts)

        # TO KNOW WHEN player hit box hits a ghost // collisions + EATING THEM
        if not super_powerup:
            if (player_circle.colliderect(red_ghost.rect) and not red_ghost.dead) or \
                    (player_circle.colliderect(blue_ghost.rect) and not blue_ghost.dead) or \
                    (player_circle.colliderect(pink_ghost.rect) and not pink_ghost.dead) or \
                    (player_circle.colliderect(orange_ghost.rect) and not orange_ghost.dead):
                # life checker
                if lives > 0:
                    super_powerup = False
                    power_counter = 0
                    # CAN USE A FUNCTION FOR REPETITIVE THINGS
                    lives -= 1
                    startup_counter = 0  # reset counter

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
                startup_counter = 0  # reset counter

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
                startup_counter = 0  # reset counter

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
                startup_counter = 0  # reset counter

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
                startup_counter = 0  # reset counter

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
        if super_powerup and player_circle.colliderect(orange_ghost.rect) and not orange_ghost.dead and not \
        eaten_ghosts[3]:
            oranG_dead = True
            eaten_ghosts[3] = True
            score += (2 ** eaten_ghosts.count(True)) * 100

        if pause:
            restart, exit = draw_pause()  # calls draw_pause function for pause menu

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # if player clicks on restart or exit button in pause menu
            if event.type == pygame.MOUSEBUTTONDOWN and pause:
                if exit.collidepoint(event.pos):
                    run = False

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
                if (event.key == pygame.K_SPACE and (game_over or game_won)) or replay:
                    super_powerup = False
                    power_counter = 0
                    # CAN USE A FUNCTION FOR REPETITIVE THINGS
                    lives -= 1
                    startup_counter = 0  # reset counter

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

        if direction_command == 0 and valid_turns[
            0]:  # checking if the direction and valid_turn is the same to allow movement
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

        if not game_won and not any(cell in (1, 2) for row in level for cell in row):
            game_won = True
            moving = False

    pygame.quit()
    pacman.deiconify()


def intermediate():
    pacman.withdraw()

    global gameBoard

    # initialisation
    pygame.font.init()
    font = pygame.font.Font('freesansbold.ttf', 20)
    surface = pygame.Surface((800, 400), pygame.SRCALPHA)  # used to display pause menu
    
    # path for files
    board_images = "Assets/BoardImages/"
    element_images = "Assets/ElementImages/"
    text_images = "Assets/TextImages/"
    highscoreFile = "Assets/Data/"
    soundtrack = "Assets/Music/"

    pygame.mixer.init()
    pygame.init()
    # print(pygame.mixer.music.get_busy())

    # 28 Across 31 Tall 1: Empty Space 2: Tic-TaC 3: Wall 4: Ghost safe-space 5: Unique Tic-TaC
    originalGameBoard = [
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
        [3, 2, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3],
        [3, 6, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 6, 3],
        [3, 2, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3],
        [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
        [3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 2, 3],
        [3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 2, 3],
        [3, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 3],
        [3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 1, 3, 3, 1, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 1, 3, 3, 1, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 3, 4, 4, 4, 4, 4, 4, 3, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
        [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3, 4, 4, 4, 4, 4, 4, 3, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1],  # Middle Lane Row: 14
        [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 3, 4, 4, 4, 4, 4, 4, 3, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 2, 3, 3, 3, 3, 3, 3],
        [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
        [3, 2, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3],
        [3, 2, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3],
        [3, 6, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 6, 3],
        [3, 3, 3, 2, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 2, 3, 3, 3],
        [3, 3, 3, 2, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 2, 3, 3, 3],
        [3, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 3],
        [3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3],
        [3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3],
        [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    ]
    gameBoard = copy.deepcopy(originalGameBoard)
    spriteRatio = 3 / 2
    square = 24  # Size of each unit square
    spriteOffset = square * (1 - spriteRatio) * (1 / 2)
    (width, height) = (len(gameBoard[0]) * square, len(gameBoard) * square)  # Game screen
    screen = pygame.display.set_mode((width, height))
    pygame.display.flip()
    musicPlaying = 0  # 0: Chomp, 1: Important, 2: Siren
    # foodColour = (165, 93, 53)
    # foodColour = (222, 161, 133)
    foodColour = "light yellow"

    BINDS = {
        "up": [pygame.K_w, pygame.K_UP],
        "down": [pygame.K_s, pygame.K_DOWN],
        "right": [pygame.K_d, pygame.K_RIGHT],
        "left": [pygame.K_a, pygame.K_LEFT]
    }

    pause = False  # for pause menu
    replay = False  # for restarting the game

    class Game:
        def __init__(self, level, score):
            self.paused = True
            self.ghostUpdateDelay = 1
            self.ghostUpdateCount = 0
            self.pacmanUpdateDelay = 1
            self.pacmanUpdateCount = 0
            self.tictakChangeDelay = 10
            self.tictakChangeCount = 0
            self.ghostsAttacked = False
            self.highScore = self.getHighest()
            self.score = score
            self.level = level
            self.lives = 3
            self.ghosts = [Ghost(14.0, 13.5, "red", 0), Ghost(17.0, 11.5, "blue", 1), Ghost(17.0, 13.5, "pink", 2),
                           Ghost(17.0, 15.5, "orange", 3)]
            self.pacman = Pacman(26.0, 13.5)  # Center of Second Last Row
            self.total = self.getCount()
            self.ghostScore = 200
            self.levels = [[350, 250], [150, 450], [150, 450], [0, 600]]
            random.shuffle(self.levels)
            # Level index and Level Progress
            self.ghostStates = [[1, 0], [0, 0], [1, 0], [0, 0]]
            index = 0
            for state in self.ghostStates:
                state[0] = randrange(2)
                state[1] = randrange(self.levels[index][state[0]] + 1)
                index += 1
            self.collected = 0
            self.started = False
            self.gameOver = False
            self.gameOverCounter = 0
            self.points = []
            self.pointsTimer = 10
            # Berry Spawn Time, Berry Death Time, Berry Eaten
            self.berryState = [200, 400, False]
            self.berryLocation = [20.0, 13.5]
            self.berries = ["tile080.png", "tile081.png", "tile082.png", "tile083.png", "tile084.png", "tile085.png",
                            "tile086.png", "tile087.png"]
            self.berriesCollected = []
            self.levelTimer = 0
            self.berryScore = 100
            self.lockedInTimer = 100
            self.lockedIn = True
            self.extraLifeGiven = False
            self.musicPlaying = 0

        # Driver method: The games primary update method
        def update(self):
            # pygame.image.unload()
            # print(self.ghostStates)
            if self.gameOver:
                self.gameOverFunc()
                return
            if self.paused or not self.started:
                self.drawTilesAround(21, 10)
                self.drawTilesAround(21, 11)
                self.drawTilesAround(21, 12)
                self.drawTilesAround(21, 13)
                self.drawTilesAround(21, 14)
                self.drawReady()
                pygame.display.update()
                return

            self.levelTimer += 1
            self.ghostUpdateCount += 1
            self.pacmanUpdateCount += 1
            self.tictakChangeCount += 1
            self.ghostsAttacked = False

            if self.score >= 10000 and not self.extraLifeGiven:
                self.lives += 1
                self.extraLifeGiven = True
                self.forcePlayMusic("pacman_extrapac.wav")

            # Draw tiles around ghosts and pacman
            self.clearBoard()
            for ghost in self.ghosts:
                if ghost.attacked:
                    self.ghostsAttacked = True

            # Check if the ghost should chase pacman
            index = 0
            for state in self.ghostStates:
                state[1] += 1
                if state[1] >= self.levels[index][state[0]]:
                    state[1] = 0
                    state[0] += 1
                    state[0] %= 2
                index += 1

            # checking ghost status
            index = 0
            for ghost in self.ghosts:
                if not ghost.attacked and not ghost.dead and self.ghostStates[index][0] == 0:
                    ghost.target = [self.pacman.row, self.pacman.col]
                index += 1

            if self.levelTimer == self.lockedInTimer:
                self.lockedIn = False

            self.checkSurroundings
            if self.ghostUpdateCount == self.ghostUpdateDelay:
                for ghost in self.ghosts:
                    ghost.update()
                self.ghostUpdateCount = 0

            if self.tictakChangeCount == self.tictakChangeDelay:
                # Changes the colour of special Tic-Taks
                self.flipcolour()
                self.tictakChangeCount = 0

            if self.pacmanUpdateCount == self.pacmanUpdateDelay:
                self.pacmanUpdateCount = 0
                self.pacman.update()
                self.pacman.col %= len(gameBoard[0])
                if self.pacman.row % 1.0 == 0 and self.pacman.col % 1.0 == 0:
                    if gameBoard[int(self.pacman.row)][int(self.pacman.col)] == 2:
                        self.playMusic("munch_1.wav")
                        gameBoard[int(self.pacman.row)][int(self.pacman.col)] = 1
                        self.score += 10
                        self.collected += 1
                        # Fill tile with black
                        pygame.draw.rect(screen, (0, 0, 0),
                                         (self.pacman.col * square, self.pacman.row * square, square, square))
                    elif gameBoard[int(self.pacman.row)][int(self.pacman.col)] == 5 or gameBoard[int(self.pacman.row)][
                        int(self.pacman.col)] == 6:
                        self.forcePlayMusic("power_pellet.wav")
                        gameBoard[int(self.pacman.row)][int(self.pacman.col)] = 1
                        self.collected += 1
                        # Fill tile with black
                        pygame.draw.rect(screen, (0, 0, 0),
                                         (self.pacman.col * square, self.pacman.row * square, square, square))
                        self.score += 50
                        self.ghostScore = 200
                        for ghost in self.ghosts:
                            ghost.attackedCount = 0
                            ghost.setAttacked(True)
                            ghost.setTarget()
                            self.ghostsAttacked = True
            self.checkSurroundings()
            self.highScore = max(self.score, self.highScore)

            global running
            if self.collected == self.total:
                # print("New Level")
                win_text = font.render('press SPACE to pause/play', True, 'green')
                screen.blit(win_text, (150, 520))
                self.forcePlayMusic("intermission.wav")
                self.level += 1
                self.newLevel()

            if self.level - 1 == 8:  # (self.levels[0][0] + self.levels[0][1]) // 50:
                # print("You win", self.level, len(self.levels))

                running = False
            self.softRender()

        # Rendering method
        def render(self):
            screen.fill((0, 0, 0))  # Flushes the screen
            # Draws game elements
            currentTile = 0
            self.displayLives()
            self.displayScore()
            for i in range(3, len(gameBoard) - 2):
                for j in range(len(gameBoard[0])):
                    if gameBoard[i][j] == 3:  # Draw wall
                        imageName = str(currentTile)
                        if len(imageName) == 1:
                            imageName = "00" + imageName
                        elif len(imageName) == 2:
                            imageName = "0" + imageName
                        # Get image of desired tile
                        imageName = "tile" + imageName + ".png"
                        tileImage = pygame.image.load(board_images + imageName)
                        tileImage = pygame.transform.scale(tileImage, (square, square))

                        # Display image of tile
                        screen.blit(tileImage, (j * square, i * square, square, square))

                        # pygame.draw.rect(screen, (0, 0, 255),(j * square, i * square, square, square)) # (x, y, width, height)
                    elif gameBoard[i][j] == 2:  # Draw Tic-Tak
                        pygame.draw.circle(screen, foodColour, (j * square + square // 2, i * square + square // 2),
                                           square // 4)
                    elif gameBoard[i][j] == 5:  # Black Special Tic-Tak
                        pygame.draw.circle(screen, (0, 0, 0), (j * square + square // 2, i * square + square // 2),
                                           square // 2)
                    elif gameBoard[i][j] == 6:  # White Special Tic-Tak
                        pygame.draw.circle(screen, foodColour, (j * square + square // 2, i * square + square // 2),
                                           square // 2)

                    currentTile += 1
            # Draw Sprites
            for ghost in self.ghosts:
                ghost.draw()
            self.pacman.draw()
            # Updates the screen
            pygame.display.update()

        def softRender(self):
            pointsToDraw = []
            for point in self.points:
                if point[3] < self.pointsTimer:
                    pointsToDraw.append([point[2], point[0], point[1]])
                    point[3] += 1
                else:
                    self.points.remove(point)
                    self.drawTilesAround(point[0], point[1])

            for point in pointsToDraw:
                self.drawPoints(point[0], point[1], point[2])

            # Draw Sprites
            for ghost in self.ghosts:
                ghost.draw()
            self.pacman.draw()
            self.displayScore()
            self.displayBerries()
            self.displayLives()
            # for point in pointsToDraw:
            
            self.drawBerry()
            # Updates the screen
            pygame.display.update()

        def playMusic(self, music):
            # return False 
            # Remove comment to disable music
            global musicPlaying
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.unload()
                pygame.mixer.music.load(soundtrack + music)
                pygame.mixer.music.queue(soundtrack + music)
                pygame.mixer.music.play()
                if music == "munch_1.wav":
                    musicPlaying = 0
                elif music == "siren_1.wav":
                    musicPlaying = 2
                else:
                    musicPlaying = 1

        def forcePlayMusic(self, music):
            # return False # Uncomment to disable music
            pygame.mixer.music.unload()
            pygame.mixer.music.load(soundtrack + music)
            pygame.mixer.music.play()
            global musicPlaying
            musicPlaying = 1

        def clearBoard(self):
            # Draw tiles around ghosts and pacman
            for ghost in self.ghosts:
                self.drawTilesAround(ghost.row, ghost.col)
            self.drawTilesAround(self.pacman.row, self.pacman.col)
            self.drawTilesAround(self.berryLocation[0], self.berryLocation[1])
            # Clears Ready! Label
            self.drawTilesAround(20, 10)
            self.drawTilesAround(20, 11)
            self.drawTilesAround(20, 12)
            self.drawTilesAround(20, 13)
            self.drawTilesAround(20, 14)

        def checkSurroundings(self):
            # Check if pacman got killed
            for ghost in self.ghosts:
                if self.touchingPacman(ghost.row, ghost.col) and not ghost.attacked:
                    if self.lives == 1:
                        print("You lose")
                        self.forcePlayMusic("death_1.wav")
                        self.gameOver = True
                        # Removes the ghosts from the screen
                        for ghost in self.ghosts:
                            self.drawTilesAround(ghost.row, ghost.col)
                        self.drawTilesAround(self.pacman.row, self.pacman.col)
                        self.pacman.draw()
                        pygame.display.update()
                        pause(10000000)
                        return
                    self.started = False
                    self.forcePlayMusic("pacman_death.wav")
                    reset()
                elif self.touchingPacman(ghost.row, ghost.col) and ghost.isAttacked() and not ghost.isDead():
                    ghost.setDead(True)
                    ghost.setTarget()
                    ghost.ghostSpeed = 1
                    ghost.row = math.floor(ghost.row)
                    ghost.col = math.floor(ghost.col)
                    self.score += self.ghostScore
                    self.points.append([ghost.row, ghost.col, self.ghostScore, 0])
                    self.ghostScore *= 2
                    self.forcePlayMusic("eat_ghost.wav")
                    pause(10000000)
            if self.touchingPacman(self.berryLocation[0], self.berryLocation[1]) and not self.berryState[
                2] and self.levelTimer in range(self.berryState[0], self.berryState[1]):
                self.berryState[2] = True
                self.score += self.berryScore
                self.points.append([self.berryLocation[0], self.berryLocation[1], self.berryScore, 0])
                self.berriesCollected.append(self.berries[(self.level - 1) % 8])
                self.forcePlayMusic("eat_fruit.wav")

        # Displays the user current score
        def displayScore(self):
            textOneUp = ["tile033.png", "tile021.png", "tile016.png"]
            textHighScore = ["tile007.png", "tile008.png", "tile006.png", "tile007.png", "tile015.png", "tile019.png",
                             "tile002.png", "tile014.png", "tile018.png", "tile004.png"]
            index = 0
            scoreStart = 5
            highScoreStart = 11
            for i in range(scoreStart, scoreStart + len(textOneUp)):
                tileImage = pygame.image.load(text_images + textOneUp[index])
                tileImage = pygame.transform.scale(tileImage, (square, square))
                screen.blit(tileImage, (i * square, 4, square, square))
                index += 1
            score = str(self.score)
            if score == "0":
                score = "00"
            index = 0
            for i in range(0, len(score)):
                digit = int(score[i])
                tileImage = pygame.image.load(text_images + "tile0" + str(32 + digit) + ".png")
                tileImage = pygame.transform.scale(tileImage, (square, square))
                screen.blit(tileImage, ((scoreStart + 2 + index) * square, square + 4, square, square))
                index += 1

            index = 0
            for i in range(highScoreStart, highScoreStart + len(textHighScore)):
                tileImage = pygame.image.load(text_images + textHighScore[index])
                tileImage = pygame.transform.scale(tileImage, (square, square))
                screen.blit(tileImage, (i * square, 4, square, square))
                index += 1

            highScore = str(self.highScore)
            if highScore == "0":
                highScore = "00"
            index = 0
            for i in range(0, len(highScore)):
                digit = int(highScore[i])
                tileImage = pygame.image.load(text_images + "tile0" + str(32 + digit) + ".png")
                tileImage = pygame.transform.scale(tileImage, (square, square))
                screen.blit(tileImage, ((highScoreStart + 6 + index) * square, square + 4, square, square))
                index += 1
            score_text = font.render('Dhruv playing ...', True, 'white')
            screen.blit(score_text, (410, 830))

        def drawBerry(self):
            if self.levelTimer in range(self.berryState[0], self.berryState[1]) and not self.berryState[2]:
                # print("here")
                berryImage = pygame.image.load(element_images + self.berries[(self.level - 1) % 8])
                berryImage = pygame.transform.scale(berryImage, (int(square * spriteRatio), int(square * spriteRatio)))
                screen.blit(berryImage,
                            (self.berryLocation[1] * square, self.berryLocation[0] * square, square, square))

        def drawPoints(self, points, row, col):
            pointStr = str(points)
            index = 0
            for i in range(len(pointStr)):
                digit = int(pointStr[i])
                tileImage = pygame.image.load(text_images + "tile" + str(224 + digit) + ".png")
                tileImage = pygame.transform.scale(tileImage, (square // 2, square // 2))
                screen.blit(tileImage,
                            ((col) * square + (square // 2 * index), row * square - 20, square // 2, square // 2))
                index += 1

        def drawReady(self):
            ready = ["tile274.png", "tile260.png", "tile256.png", "tile259.png", "tile281.png", "tile283.png"]
            for i in range(len(ready)):
                letter = pygame.image.load(text_images + ready[i])
                letter = pygame.transform.scale(letter, (int(square), int(square)))
                screen.blit(letter, ((11 + i) * square, 20 * square, square, square))

        def gameOverFunc(self):
            global running
            if self.gameOverCounter == 12:
                running = False
                self.recordHighScore()
                return

            # Resets the screen around pacman
            self.drawTilesAround(self.pacman.row, self.pacman.col)

            # Draws new image
            pacmanImage = pygame.image.load(element_images + "tile" + str(116 + self.gameOverCounter) + ".png")
            pacmanImage = pygame.transform.scale(pacmanImage, (int(square * spriteRatio), int(square * spriteRatio)))
            screen.blit(pacmanImage, (
            self.pacman.col * square + spriteOffset, self.pacman.row * square + spriteOffset, square, square))
            pygame.display.update()
            pause(5000000)
            self.gameOverCounter += 1

        # lives counter for player
        def displayLives(self):
            # 33 rows || 28 cols
            # Lives[[31, 5], [31, 3], [31, 1]]
            livesLoc = [[34, 3], [34, 1]]
            for i in range(self.lives - 1):
                lifeImage = pygame.image.load(element_images + "tile054.png")
                lifeImage = pygame.transform.scale(lifeImage, (int(square * spriteRatio), int(square * spriteRatio)))
                screen.blit(lifeImage,
                            (livesLoc[i][1] * square, livesLoc[i][0] * square - spriteOffset, square, square))

        # display of berries across map
        def displayBerries(self):
            firstBerrie = [34, 26]
            for i in range(len(self.berriesCollected)):
                berrieImage = pygame.image.load(element_images + self.berriesCollected[i])
                berrieImage = pygame.transform.scale(berrieImage,
                                                     (int(square * spriteRatio), int(square * spriteRatio)))
                screen.blit(berrieImage,
                            ((firstBerrie[1] - (2 * i)) * square, firstBerrie[0] * square + 5, square, square))

        # collision detection
        def touchingPacman(self, row, col):
            if row - 0.5 <= self.pacman.row and row >= self.pacman.row and col == self.pacman.col:
                return True
            elif row + 0.5 >= self.pacman.row and row <= self.pacman.row and col == self.pacman.col:
                return True
            elif row == self.pacman.row and col - 0.5 <= self.pacman.col and col >= self.pacman.col:
                return True
            elif row == self.pacman.row and col + 0.5 >= self.pacman.col and col <= self.pacman.col:
                return True
            elif row == self.pacman.row and col == self.pacman.col:
                return True
            return False

        # generate new level
        def newLevel(self):
            reset()
            self.lives += 1
            self.collected = 0
            self.started = False
            self.berryState = [200, 400, False]
            self.levelTimer = 0
            self.lockedIn = True
            for level in self.levels:
                level[0] = min((level[0] + level[1]) - 100, level[0] + 50)
                level[1] = max(100, level[1] - 50)
            random.shuffle(self.levels)
            index = 0
            for state in self.ghostStates:
                state[0] = randrange(2)
                state[1] = randrange(self.levels[index][state[0]] + 1)
                index += 1
            global gameBoard
            gameBoard = copy.deepcopy(originalGameBoard)
            self.render()

        # updating the tiles
        def drawTilesAround(self, row, col):
            row = math.floor(row)
            col = math.floor(col)
            for i in range(row - 2, row + 3):
                for j in range(col - 2, col + 3):
                    if i >= 3 and i < len(gameBoard) - 2 and j >= 0 and j < len(gameBoard[0]):
                        imageName = str(((i - 3) * len(gameBoard[0])) + j)
                        if len(imageName) == 1:
                            imageName = "00" + imageName
                        elif len(imageName) == 2:
                            imageName = "0" + imageName
                        # Get image of desired tile
                        imageName = "tile" + imageName + ".png"
                        tileImage = pygame.image.load(board_images + imageName)
                        tileImage = pygame.transform.scale(tileImage, (square, square))
                        # Display image of tile
                        screen.blit(tileImage, (j * square, i * square, square, square))

                        if gameBoard[i][j] == 2:  # Draw Tic-Tak
                            pygame.draw.circle(screen, foodColour, (j * square + square // 2, i * square + square // 2),
                                               square // 4)
                        elif gameBoard[i][j] == 5:  # Black Special Tic-Tak
                            pygame.draw.circle(screen, (0, 0, 0), (j * square + square // 2, i * square + square // 2),
                                               square // 2)
                        elif gameBoard[i][j] == 6:  # White Special Tic-Tak
                            pygame.draw.circle(screen, foodColour, (j * square + square // 2, i * square + square // 2),
                                               square // 2)

        # Flips colour of Special Tic-Taks
        def flipcolour(self):
            global gameBoard
            for i in range(3, len(gameBoard) - 2):
                for j in range(len(gameBoard[0])):
                    if gameBoard[i][j] == 5:
                        gameBoard[i][j] = 6
                        pygame.draw.circle(screen, foodColour, (j * square + square // 2, i * square + square // 2),
                                           square // 2)
                    elif gameBoard[i][j] == 6:
                        gameBoard[i][j] = 5
                        pygame.draw.circle(screen, (0, 0, 0), (j * square + square // 2, i * square + square // 2),
                                           square // 2)

        # counts score of player
        def getCount(self):
            total = 0
            for i in range(3, len(gameBoard) - 2):
                for j in range(len(gameBoard[0])):
                    if gameBoard[i][j] == 2 or gameBoard[i][j] == 5 or gameBoard[i][j] == 6:
                        total += 1
            return total

        # highscore getter
        def getHighest(self):
            try:
                with open(highscoreFile + "HighScore.txt", "r", encoding="utf-8") as file:
                    return int(file.read().strip())
            except (FileNotFoundError, ValueError):
                return 0

        # setting highscore to file
        def recordHighScore(self):
            os.makedirs(highscoreFile, exist_ok=True)
            with open(highscoreFile + "HighScore.txt", "w", encoding="utf-8") as file:
                file.write(str(self.highScore))

            if self.highScore > h2score[0]:
                h2score[0] = self.highScore

    class Pacman:
        def __init__(self, row, col):
            self.row = row
            self.col = col
            self.mouthOpen = False
            self.pacSpeed = 1 / 4
            self.mouthChangeDelay = 5
            self.mouthChangeCount = 0
            self.dir = 0  # 0:Up 1: Right 2: Down 3: Left
            self.newDir = 0

        # updating position + direction of pacman
        def update(self):
            if self.newDir == 0:
                if canMove(math.floor(self.row - self.pacSpeed), self.col) and self.col % 1.0 == 0:
                    self.row -= self.pacSpeed
                    self.dir = self.newDir
                    return
            elif self.newDir == 1:
                if canMove(self.row, math.ceil(self.col + self.pacSpeed)) and self.row % 1.0 == 0:
                    self.col += self.pacSpeed
                    self.dir = self.newDir
                    return
            elif self.newDir == 2:
                if canMove(math.ceil(self.row + self.pacSpeed), self.col) and self.col % 1.0 == 0:
                    self.row += self.pacSpeed
                    self.dir = self.newDir
                    return
            elif self.newDir == 3:
                if canMove(self.row, math.floor(self.col - self.pacSpeed)) and self.row % 1.0 == 0:
                    self.col -= self.pacSpeed
                    self.dir = self.newDir
                    return

            if self.dir == 0:
                if canMove(math.floor(self.row - self.pacSpeed), self.col) and self.col % 1.0 == 0:
                    self.row -= self.pacSpeed
            elif self.dir == 1:
                if canMove(self.row, math.ceil(self.col + self.pacSpeed)) and self.row % 1.0 == 0:
                    self.col += self.pacSpeed
            elif self.dir == 2:
                if canMove(math.ceil(self.row + self.pacSpeed), self.col) and self.col % 1.0 == 0:
                    self.row += self.pacSpeed
            elif self.dir == 3:
                if canMove(self.row, math.floor(self.col - self.pacSpeed)) and self.row % 1.0 == 0:
                    self.col -= self.pacSpeed

        # Draws pacman based on his current state
        def draw(self):
            if not game.started:
                pacmanImage = pygame.image.load(element_images + "tile112.png")
                pacmanImage = pygame.transform.scale(pacmanImage,
                                                     (int(square * spriteRatio), int(square * spriteRatio)))
                screen.blit(pacmanImage,
                            (self.col * square + spriteOffset, self.row * square + spriteOffset, square, square))
                return

            if self.mouthChangeCount == self.mouthChangeDelay:
                self.mouthChangeCount = 0
                self.mouthOpen = not self.mouthOpen
            self.mouthChangeCount += 1
            # pacmanImage = pygame.image.load("Sprites/tile049.png")
            if self.dir == 0:
                if self.mouthOpen:
                    pacmanImage = pygame.image.load(element_images + "tile049.png")
                else:
                    pacmanImage = pygame.image.load(element_images + "tile051.png")
            elif self.dir == 1:
                if self.mouthOpen:
                    pacmanImage = pygame.image.load(element_images + "tile052.png")
                else:
                    pacmanImage = pygame.image.load(element_images + "tile054.png")
            elif self.dir == 2:
                if self.mouthOpen:
                    pacmanImage = pygame.image.load(element_images + "tile053.png")
                else:
                    pacmanImage = pygame.image.load(element_images + "tile055.png")
            elif self.dir == 3:
                if self.mouthOpen:
                    pacmanImage = pygame.image.load(element_images + "tile048.png")
                else:
                    pacmanImage = pygame.image.load(element_images + "tile050.png")

            pacmanImage = pygame.transform.scale(pacmanImage, (int(square * spriteRatio), int(square * spriteRatio)))
            screen.blit(pacmanImage,
                        (self.col * square + spriteOffset, self.row * square + spriteOffset, square, square))

    class Ghost:
        def __init__(self, row, col, colour, changeFeetCount):
            self.row = row
            self.col = col
            self.attacked = False
            self.colour = colour
            self.dir = randrange(4)
            self.dead = False
            self.changeFeetCount = changeFeetCount
            self.changeFeetDelay = 5
            self.target = [-1, -1]
            self.ghostSpeed = 1 / 4
            self.lastLoc = [-1, -1]
            self.attackedTimer = 240
            self.attackedCount = 0
            self.deathTimer = 120
            self.deathCount = 0

        # update ghost position and direction in game
        def update(self):
            # print(self.row, self.col)
            if self.target == [-1, -1] or (self.row == self.target[0] and self.col == self.target[1]) or \
                    gameBoard[int(self.row)][int(self.col)] == 4 or self.dead:
                self.setTarget()
            self.setDir()
            self.move()

            if self.attacked:
                self.attackedCount += 1

            if self.attacked and not self.dead:
                self.ghostSpeed = 1 / 8

            if self.attackedCount == self.attackedTimer and self.attacked:
                if not self.dead:
                    self.ghostSpeed = 1 / 4
                    self.row = math.floor(self.row)
                    self.col = math.floor(self.col)

                self.attackedCount = 0
                self.attacked = False
                self.setTarget()

            if self.dead and gameBoard[self.row][self.col] == 4:
                self.deathCount += 1
                self.attacked = False
                if self.deathCount == self.deathTimer:
                    self.deathCount = 0
                    self.dead = False
                    self.ghostSpeed = 1 / 4

        def draw(self):  # Ghosts states: Alive, Attacked, Dead Attributes: colour, Direction, Location
            ghostImage = pygame.image.load(element_images + "tile152.png")
            currentDir = ((self.dir + 3) % 4) * 2
            if self.changeFeetCount == self.changeFeetDelay:
                self.changeFeetCount = 0
                currentDir += 1
            self.changeFeetCount += 1
            if self.dead:
                tileNum = 152 + currentDir
                ghostImage = pygame.image.load(element_images + "tile" + str(tileNum) + ".png")
            elif self.attacked:
                if self.attackedTimer - self.attackedCount < self.attackedTimer // 3:
                    if (self.attackedTimer - self.attackedCount) % 31 < 26:
                        ghostImage = pygame.image.load(
                            element_images + "tile0" + str(70 + (currentDir - (((self.dir + 3) % 4) * 2))) + ".png")
                    else:
                        ghostImage = pygame.image.load(
                            element_images + "tile0" + str(72 + (currentDir - (((self.dir + 3) % 4) * 2))) + ".png")
                else:
                    ghostImage = pygame.image.load(
                        element_images + "tile0" + str(72 + (currentDir - (((self.dir + 3) % 4) * 2))) + ".png")
            else:
                if self.colour == "blue":
                    tileNum = 136 + currentDir
                    ghostImage = pygame.image.load(element_images + "tile" + str(tileNum) + ".png")
                elif self.colour == "pink":
                    tileNum = 128 + currentDir
                    ghostImage = pygame.image.load(element_images + "tile" + str(tileNum) + ".png")
                elif self.colour == "orange":
                    tileNum = 144 + currentDir
                    ghostImage = pygame.image.load(element_images + "tile" + str(tileNum) + ".png")
                elif self.colour == "red":
                    tileNum = 96 + currentDir
                    if tileNum < 100:
                        ghostImage = pygame.image.load(element_images + "tile0" + str(tileNum) + ".png")
                    else:
                        ghostImage = pygame.image.load(element_images + "tile" + str(tileNum) + ".png")

            ghostImage = pygame.transform.scale(ghostImage, (int(square * spriteRatio), int(square * spriteRatio)))
            screen.blit(ghostImage,
                        (self.col * square + spriteOffset, self.row * square + spriteOffset, square, square))

        def isValidTwo(self, cRow, cCol, dist, visited):
            if cRow < 3 or cRow >= len(gameBoard) - 5 or cCol < 0 or cCol >= len(gameBoard[0]) or gameBoard[cRow][
                cCol] == 3:
                return False
            elif visited[cRow][cCol] <= dist:
                return False
            return True

        def isValid(self, cRow, cCol):
            if cCol < 0 or cCol > len(gameBoard[0]) - 1:
                return True
            for ghost in game.ghosts:
                if ghost.colour == self.colour:
                    continue
                if ghost.row == cRow and ghost.col == cCol and not self.dead:
                    return False
            if not ghostGate.count([cRow, cCol]) == 0:
                if self.dead and self.row < cRow:
                    return True
                elif self.row > cRow and not self.dead and not self.attacked and not game.lockedIn:
                    return True
                else:
                    return False
            if gameBoard[cRow][cCol] == 3:
                return False
            return True

        def setDir(self):
            dirs = [[0, -self.ghostSpeed, 0],
                    [1, 0, self.ghostSpeed],
                    [2, self.ghostSpeed, 0],
                    [3, 0, -self.ghostSpeed]
                    ]
            random.shuffle(dirs)
            best = 10000
            bestDirection = -1
            for newDir in dirs:
                if self.calculateDistance(self.target, [self.row + newDir[1], self.col + newDir[2]]) < best:
                    if not (self.lastLoc[0] == self.row + newDir[1] and self.lastLoc[1] == self.col + newDir[2]):
                        if newDir[0] == 0 and self.col % 1.0 == 0:
                            if self.isValid(math.floor(self.row + newDir[1]), int(self.col + newDir[2])):
                                bestDirection = newDir[0]
                                best = self.calculateDistance(self.target, [self.row + newDir[1], self.col + newDir[2]])
                        elif newDir[0] == 1 and self.row % 1.0 == 0:
                            if self.isValid(int(self.row + newDir[1]), math.ceil(self.col + newDir[2])):
                                bestDirection = newDir[0]
                                best = self.calculateDistance(self.target, [self.row + newDir[1], self.col + newDir[2]])
                        elif newDir[0] == 2 and self.col % 1.0 == 0:
                            if self.isValid(math.ceil(self.row + newDir[1]), int(self.col + newDir[2])):
                                bestDirection = newDir[0]
                                best = self.calculateDistance(self.target, [self.row + newDir[1], self.col + newDir[2]])
                        elif newDir[0] == 3 and self.row % 1.0 == 0:
                            if self.isValid(int(self.row + newDir[1]), math.floor(self.col + newDir[2])):
                                bestDirection = newDir[0]
                                best = self.calculateDistance(self.target, [self.row + newDir[1], self.col + newDir[2]])
            self.dir = bestDirection

        def calculateDistance(self, a, b):
            dR = a[0] - b[0]
            dC = a[1] - b[1]
            return math.sqrt((dR * dR) + (dC * dC))

        def setTarget(self):
            if gameBoard[int(self.row)][int(self.col)] == 4 and not self.dead:
                self.target = [ghostGate[0][0] - 1, ghostGate[0][1] + 1]
                return
            elif gameBoard[int(self.row)][int(self.col)] == 4 and self.dead:
                self.target = [self.row, self.col]
            elif self.dead:
                self.target = [14, 13]
                return

            # Records the quadrants of each ghost's target
            quads = [0, 0, 0, 0]
            for ghost in game.ghosts:
                # if ghost.target[0] == self.row and ghost.col == self.col:
                #     continue
                if ghost.target[0] <= 15 and ghost.target[1] >= 13:
                    quads[0] += 1
                elif ghost.target[0] <= 15 and ghost.target[1] < 13:
                    quads[1] += 1
                elif ghost.target[0] > 15 and ghost.target[1] < 13:
                    quads[2] += 1
                elif ghost.target[0] > 15 and ghost.target[1] >= 13:
                    quads[3] += 1

            # Finds a target that will keep the ghosts dispersed
            while True:
                self.target = [randrange(31), randrange(28)]
                quad = 0
                if self.target[0] <= 15 and self.target[1] >= 13:
                    quad = 0
                elif self.target[0] <= 15 and self.target[1] < 13:
                    quad = 1
                elif self.target[0] > 15 and self.target[1] < 13:
                    quad = 2
                elif self.target[0] > 15 and self.target[1] >= 13:
                    quad = 3
                if not gameBoard[self.target[0]][self.target[1]] == 3 and not gameBoard[self.target[0]][
                                                                                  self.target[1]] == 4:
                    break
                elif quads[quad] == 0:
                    break

        def move(self):
            # print(self.target)
            self.lastLoc = [self.row, self.col]
            if self.dir == 0:
                self.row -= self.ghostSpeed
            elif self.dir == 1:
                self.col += self.ghostSpeed
            elif self.dir == 2:
                self.row += self.ghostSpeed
            elif self.dir == 3:
                self.col -= self.ghostSpeed

            # Incase they go through the middle tunnel
            self.col = self.col % len(gameBoard[0])
            if self.col < 0:
                self.col = len(gameBoard[0]) - 0.5

        def setAttacked(self, isAttacked):
            self.attacked = isAttacked

        def isAttacked(self):
            return self.attacked

        def setDead(self, isDead):
            self.dead = isDead

        def isDead(self):
            return self.dead

    game = Game(1, 0)
    ghostsafeArea = [15, 13]  # The location the ghosts escape to when attacked
    ghostGate = [[15, 13], [15, 14]]

    def draw_pause():
        pygame.draw.rect(surface, (128, 128, 128, 150), [0, 0, 800, 1000])
        pygame.draw.rect(surface, 'dark gray', [200, 100, 280, 50], 0, 10)
        reset = pygame.draw.rect(surface, 'white', [200, 200, 280, 50], 0, 10)
        exit = pygame.draw.rect(surface, 'white', [200, 300, 280, 50], 0, 10)
        surface.blit(font.render("Game Paused", True, 'black'), (280, 115))
        surface.blit(font.render("Restart", True, 'black'), (310, 215))
        surface.blit(font.render("Exit", True, 'black'), (325, 315))
        screen.blit(surface, (0, 0))
        return reset, exit

    def canMove(row, col):
        if col == -1 or col == len(gameBoard[0]):
            return True
        if gameBoard[int(row)][int(col)] != 3:
            return True
        return False

    # Reset after death
    def reset():
        global game
        game.ghosts = [Ghost(14.0, 13.5, "red", 0), Ghost(17.0, 11.5, "blue", 1), Ghost(17.0, 13.5, "pink", 2),
                       Ghost(17.0, 15.5, "orange", 3)]
        for ghost in game.ghosts:
            ghost.setTarget()
        game.pacman = Pacman(26.0, 13.5)
        game.lives -= 1
        game.paused = True
        game.render()



    def displayLaunchScreen(username, game_mode):
        # Set up the screen
        screen = pygame.display.set_mode((670, 860))  # Adjust size as needed
        pygame.display.set_caption("Pacman Launch Screen")

        # Load custom font
        font_path = "freesansbold.ttf"  # Replace with your font file
        large_font = pygame.font.Font(font_path, 74)
        medium_font = pygame.font.Font(font_path, 50)
        small_font = pygame.font.Font(font_path, 36)

        # Background color
        screen.fill((0, 0, 0))  # Fill the screen with black

        # Draw Pacman Title
        pacmanTitle = large_font.render("PACMAN", True, (255, 255, 0))
        screen.blit(pacmanTitle, (150, 50))  # Adjust position as needed

        # Draw Character / Nickname
        characterTitle = medium_font.render("Character / Nickname", True, (255, 255, 255))
        screen.blit(characterTitle, (150, 150))  # Adjust position as needed

        # Display welcome message with game mode
        welcomeMessage = medium_font.render(f"Welcome to {game_mode} mode", True, (255, 255, 255))
        screen.blit(welcomeMessage, (100, 250))  # Adjust position as needed

        # Display hi message with username
        hiMessage = medium_font.render(f"Hi {username}", True, (255, 255, 255))
        screen.blit(hiMessage, (300, 300))  # Adjust position as needed

        # Press Space to Play
        instructions = small_font.render("Press SPACE to start", True, (255, 255, 255))
        screen.blit(instructions, (250, 400))  # Adjust position as needed

        pygame.display.update()

    # Fetch Username
    username = "Dhruv"
    game_mode = "Classic mode"
    displayLaunchScreen(username, game_mode)

    running = True
    onLaunchScreen = True
    # displayLaunchScreen(username, game_mode)
    clock = pygame.time.Clock()

    def pause(time):
        current = 0
        while not current == time:
            current += 1

    def start_game():
        game = Game()
        ghost = Ghost()
        pacman = Pacman()

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game.recordHighScore()
            elif event.type == pygame.KEYDOWN:
                if onLaunchScreen:
                    if event.key == pygame.K_SPACE:
                        onLaunchScreen = False
                        game.paused = False
                        game.started = True
                        game.render()
                        pygame.mixer.music.load(soundtrack + "pacman_beginning.wav")
                        pygame.mixer.music.play()
                        musicPlaying = 1
                    continue

                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    running = False
                    game.recordHighScore()
                    continue

                if event.key in (pygame.K_SPACE, pygame.K_p):
                    game.paused = not game.paused
                    continue

                game.started = True
                if event.key in BINDS["up"]:
                    game.pacman.newDir = 0
                elif event.key in BINDS["right"]:
                    game.pacman.newDir = 1
                elif event.key in BINDS["down"]:
                    game.pacman.newDir = 2
                elif event.key in BINDS["left"]:
                    game.pacman.newDir = 3

        if not onLaunchScreen:
            game.update()

    pygame.quit()
    pacman.deiconify()

def survival():
    pacman.withdraw()

    try:
        process = subprocess.Popen(
            [sys.executable, os.path.join(os.getcwd(), "Survival.py")],
            cwd=os.getcwd()
        )

        def restore_launcher():
            if process.poll() is not None:
                pacman.deiconify()
            else:
                pacman.after(500, restore_launcher)

        pacman.after(500, restore_launcher)
    except Exception as error:
        pacman.deiconify()
        messagebox.showerror("Survival failed", str(error))

    return

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

    # Load sounds
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

    # Drawing the map using png image
    def draw():
        global pacDots, player, score, lives, start_time, game_paused, high_score
        screen.clear()
        blinky_img = pygame.transform.scale(pygame.image.load('images/survival4.png'), (600, 100))
        screen.blit(blinky_img, (0, 0))
        screen.blit('colourmap', (0, 80))
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
            screen.draw.text("GAME OVER", center=(300, 480), owidth=0.5, ocolor=(255, 255, 255), color=(255, 64, 0),
                             fontsize=60)
        if player.status == 2:
            screen.draw.text("YOU WIN!", center=(300, 484), owidth=0.5, ocolor=(255, 255, 255), color=(255, 64, 0),
                             fontsize=60)

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

        # displaying message when game paused
        if game_paused:
            screen.draw.text("PAUSED", center=(300, 330), fontsize=40, color=(255, 64, 0))
            screen.draw.text("Press 'R' to Restart", center=(300, 370), fontsize=30, color=(255, 255, 255))
            screen.draw.text("Press 'Q' to Quit", center=(300, 410), fontsize=30, color=(255, 255, 255))

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
                    animate(player, pos=(player.x + player.movex, player.y + player.movey), duration=1 / SPEED,
                            tween='linear', on_finished=inputUnLock)

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
            animate(ghost, pos=(ghost.x + dmoves[ghost.dir][0] * 20, ghost.y + dmoves[ghost.dir][1] * 20),
                    duration=1 / SPEED, tween='linear', on_finished=flagMoveGhosts)

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

    try:
        process = subprocess.Popen([sys.executable, os.path.join(os.getcwd(), "Survival.py")], cwd=os.getcwd())

        def restore_launcher():
            if process.poll() is not None:
                pacman.deiconify()
            else:
                pacman.after(500, restore_launcher)

        pacman.after(500, restore_launcher)
    except Exception as error:
        messagebox.showerror("Survival failed", str(error))



def show_menu():
    pygame.mixer.music.stop()
    pygame.mixer.music.load("gif/main menu.mp3")
    pygame.mixer.music.play(-1)
    welcome_frame.pack_forget()
    page1_frame.pack_forget()
    page2_frame.pack_forget()

    menu_frame.pack(fill=BOTH, expand=True)


def show_welcome():
    menu_frame.pack_forget()  # hides previous frame
    welcome_frame.pack(fill=BOTH, expand=True)

    pacman.after(3000, show_menu)  # Show the menu after 2 seconds
    animate()


def lvls():
    menu_frame.pack_forget()
    pygame.mixer.music.load("gif/level menu sond.mp3")
    pygame.mixer.music.play(-1)
    page1_frame.pack(fill='both', expand=True)


def show_page2():
    menu_frame.pack_forget()
    pygame.mixer.music.load("gif/option.mp3")
    pygame.mixer.music.play(-1)
    frh.pack_forget()
    guid.pack_forget()
    page2_frame.pack(fill='both', expand=True)


def display():
    pygame.mixer.music.stop()
    pacman.destroy()


# Goodbye page
def exit():
    global bouncing
    menu_frame.pack_forget()  # discards the previous frame
    pygame.mixer.music.stop()
    pygame.mixer.music.load("gif/Goodbye Everyone.mp3")
    pygame.mixer.music.play(-1)
    for image in bouncing:
        image.stop()
    exit_button = tk.Button(exiting,
                            text="GoodBye",
                            font=("Arial", 10, "bold"),
                            fg="black",
                            bg="orange",
                            bd=7,
                            activeforeground="orange",
                            activebackground="black",
                            width=10,
                            height=1,
                            command=display)
    exit_button.place(relx=.5, rely=0.5, anchor=CENTER)
    exiting.pack(fill=BOTH, expand=True)

    # pacman.destroy()


def create_back_button1(frame):
    back_button = tk.Button(frame,
                            text="GO BACK",
                            font=("Arial", 10, "bold"),
                            fg="black",
                            bg="orange",
                            bd=7,
                            activeforeground="orange",
                            activebackground="black",
                            width=10,
                            height=2,
                            command=show_page2)

    back_button.place(relx=0.11, rely=0.2, anchor=CENTER)


# GO BACK button
def create_back_button(frame):
    back_button = tk.Button(frame,
                            text="GO BACK",
                            font=("Arial", 10, "bold"),
                            fg="black",
                            bg="orange",
                            bd=7,
                            activeforeground="orange",
                            activebackground="black",
                            width=10,
                            height=1,
                            command=show_menu)

    back_button.place(relx=0.12, rely=0.08, anchor=SE)


# Class for GIF animation
class AnimatedGif:
    def __init__(self, parent, gif_file):
        self.parent = parent
        self.gif_file = gif_file
        self.frames = self.load_gif()
        self.label = Label(self.parent)
        self.label.pack()
        self.animate2()

    def load_gif(self):
        gif = Image.open(self.gif_file)
        frames = []
        try:
            while True:
                frames.append(ImageTk.PhotoImage(gif.copy()))
                gif.seek(len(frames))  # Go to the next frame
        except EOFError:
            pass  # End of GIF
        return itertools.cycle(frames)  # Create an infinite loop of frames

    def animate2(self):
        self.label.config(image=next(self.frames))
        self.parent.after(100, self.animate2)  # Adjust the delay as needed

# Image thread
threads = []


def animate():
    pygame.mixer.music.load("gif/pacman-phonk-bounce.mp3")
    pygame.mixer.music.play(loops=0)

    for image in bouncing:
        threads.append(image.threadmove())


# Create the main window
pacman = tk.Tk()
pacman.title("Pacman Game")
pacman.geometry("1100x700")
pacman.minsize(900, 620)

# Welcome Page
welcome_frame = tk.Frame(pacman)
welcome_image = PhotoImage(
    file="gif/pacwlcm.png")  # Replace with your image path
pclabel = tk.Label(welcome_frame, image=welcome_image)
pclabel.place(relwidth=1, relheight=1)
label = Label(welcome_frame,
              font=("Arial", 40, "bold"),
              fg="white",
              bg="black",
              text="WELCOME TO THE PACMAN GAME",
              bd=10,
              )
label.pack(pady=80)

# Display enjoy message
labelw = Label(welcome_frame,
              font=("Arial", 20, "bold"),
              fg="pink",
              bg="black",
              text="ENJOY!!!",
              bd=10,
              )
labelw.place(relx=.5,rely=.3,anchor=CENTER)

# Menu Page
menu_frame = tk.Frame(pacman)
frame = tk.Frame(menu_frame, width=1050, height=670)
frame.pack(fill=tk.BOTH, expand=True)

# path of loading ghosts
file1 = "gif/Retro Red Ghost .png"
file2 = "gif/Retro Blue Ghost .png"
file3 = "gif/Retro Pink Ghost .png"
file4 = "gif/Retro Cherry.png"
file5 = "gif/pacopen.png"

canvas = tk.Canvas(frame, width=1050, height=670)
canvas.pack(fill=tk.BOTH, expand=True)

background_photo = tk.PhotoImage(file='gif/welcomingmap.png')
background = canvas.create_image(0, 0, image=background_photo, anchor=NW)

# For menu bouncing animation
bouncing = [
    bounceI(canvas, 50, 450, 7, 4, file1),
    bounceI(canvas, 800, 0, 8, 6, file2),
    bounceI(canvas, 900, 100, 3, 8, file3),
    bounceI(canvas, 700, 200, 3, 7, file4),
    bounceI(canvas, 100, 200, 8, 10, file5)
]

# Start button
button1 = tk.Button(frame,
                    text="START\nGAME",
                    command=lvls,
                    fg="green",
                    bg="black",
                    bd=10,
                    activeforeground="black",
                    activebackground="orange",
                    width=11,
                    height=2,
                    font=("Arial", 20, "bold"))
button1.place(relx=0.5, rely=0.4, anchor=CENTER)

# Options button
button2 = tk.Button(frame,
                    text="OPTIONS",
                    command=show_page2,
                    fg="green",
                    bg="black",
                    bd=10,
                    activeforeground="black",
                    activebackground="light blue",
                    width=11,
                    height=2,
                    font=("Arial", 20, "bold"))
button2.place(relx=0.3, rely=0.6, anchor=CENTER)

# Exit button
button3 = tk.Button(frame,
                    text="EXIT\nGAME",
                    command=exit,
                    fg="green",
                    bg="black",
                    bd=10,
                    activeforeground="black",
                    activebackground="red",
                    width=11,
                    height=2,
                    font=("Arial", 20, "bold"))
button3.place(relx=0.7, rely=0.6, anchor=CENTER)

# Page 1
page1_frame = tk.Frame(pacman)
gif1 = AnimatedGif(page1_frame, "gif/gif1.gif") # background gif

# classic button
lvl1 = tk.Button(page1_frame,
                 text="CLASSIC",
                 command=classic,
                 fg="green",
                 bg="black",
                 bd=10,
                 activeforeground="green",
                 activebackground="black",
                 width=11,
                 height=2,
                 font=("Arial", 20, "bold"))
lvl1.place(relx=0.5, rely=0.3, anchor=CENTER)

# intermediate button
lvl2 = tk.Button(page1_frame,
                 text="INTERMEDIATE",
                 command=intermediate,
                 fg="green",
                 bg="black",
                 bd=10,
                 activeforeground="green",
                 activebackground="black",
                 width=12,
                 height=2,
                 font=("Arial", 20, "bold"))
lvl2.place(relx=0.5, rely=0.5, anchor=CENTER)

# survival button
lvl3 = tk.Button(page1_frame,
                 text="SURVIVAL",
                 command=survival,
                 fg="green",
                 bg="black",
                 bd=10,
                 activeforeground="green",
                 activebackground="black",
                 width=11,
                 height=2,
                 font=("Arial", 20, "bold"))
lvl3.place(relx=0.5, rely=0.7, anchor=CENTER)

# page1_label.pack(fill=tk.BOTH, expand=True)
create_back_button(page1_frame)

# Page 2
page2_frame = tk.Frame(pacman)
gif2 = AnimatedGif(page2_frame, "gif/pacman maz eating.gif")

from tkinter import *

try:
    import win32com.client as win32
except (ImportError, ModuleNotFoundError):
    win32 = None


def send_email(recipient, subject, body):
    if win32 is None:
        messagebox.showwarning("Email unavailable", "Outlook and pywin32 are not available on this system.")
        return False

    try:
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)  # 0: olMailItem
        mail.To = recipient
        mail.Subject = subject
        mail.Body = body
        mail.Send()
        return True
    except Exception as error:
        messagebox.showerror("Email failed", str(error))
        return False

# Email section
from tkinter import messagebox

# Email format
def inputt(cx):
    subject = "PACMAN RESULT"
    body = f"""
    Your High-score for classic is {1330}
    Your High-score for classic is {h2score[0]}
    Your High-score for classic is {2900}
      Well played!!!!!!!!!

    Yours faithfully,
    PACMAN
    """
    return send_email(cx, subject, body)


# Email validation
def btn_click():
    cx = data.get().strip()
    if not cx:
        messagebox.showinfo("SIGNAL", "ENTER THE RIGHT EMAIL")
        return

    if inputt(cx):
        messagebox.showinfo("ACKNOWLEDGE", "EMAIL SENT SUCCESSFULLY")


data = StringVar()


def high():
    page2_frame.pack_forget()

    putl = Label(frh, text="Enter your email:", fg="blue", font=("Arial", 16, "bold"))
    putl.place(relx=.4, rely=.35, anchor=CENTER)

    textbox = Entry(frh, fg="blue", textvariable=data, font=(16))
    textbox.place(relx=.6, rely=.35, anchor=CENTER)

    buttonh = Button(frh, text="Send Email", command=btn_click, fg="blue", font=("Arial", 16, "bold"))
    buttonh.place(relx=.5, rely=.75, anchor=CENTER)
    frh.pack(fill='both', expand=True)


frh = tk.Frame(pacman)
im = PhotoImage(file="gif/pac3ghost.png")  # Replace with your image path
piclabel = tk.Label(frh, image=im)
piclabel.place(relwidth=1, relheight=1)
create_back_button1(frh)


def tuto():
    page2_frame.pack_forget()

    guid.pack(fill="both", expand=True)


guid = tk.Frame(pacman)
ima = PhotoImage(
    file="gif/guide2.png")  # Replace with your image path
piclbl = tk.Label(guid, image=ima)
piclbl.place(relwidth=1, relheight=1)
create_back_button1(guid)

# HighScore button to send mail
hbutton = tk.Button(page2_frame,
                    text="EMAIL THE\nHIGHEST\nSCORE",
                    fg="green",
                    bg="black",
                    bd=10,
                    activeforeground="yellow",
                    activebackground="black",
                    width=10,
                    height=2,
                    command=high,
                    font=("Arial", 20, "bold"),
                    )
hbutton.place(relx=0.4, rely=0.4, anchor=tk.CENTER)

# Guide button
tbutton = tk.Button(page2_frame,
                    text="GUIDE",
                    fg="green",
                    bg="black",
                    bd=10,
                    activeforeground="BLACK",
                    activebackground="YELLOW",
                    width=10,
                    height=2,
                    command=tuto,
                    font=("Arial", 20, "bold"),
                    )
tbutton.place(relx=0.6, rely=0.6, anchor=tk.CENTER)
create_back_button(page2_frame)

# Page 3
exiting = tk.Frame(pacman)
exit_image = PhotoImage(
    file="gif/exit2.png")  # Replace with your image path
piclabel = tk.Label(exiting, image=exit_image)
piclabel.place(relwidth=1, relheight=1)
label = Label(exiting,
              font=("Arial", 40, "bold"),
              fg="white",
              bg="black",
              text="THANK YOU FOR PLAYING",
              bd=10,
              )
label.pack(pady=80)

# Start with the welcome page
show_welcome()

# Run the application
pacman.mainloop()

