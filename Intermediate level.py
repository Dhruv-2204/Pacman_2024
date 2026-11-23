# imports

import pygame
import math
from random import randrange
import random
import copy
import os
import sys
import threading

pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 20)
surface = pygame.Surface((800,400), pygame.SRCALPHA) # used to display pause menu

board_images = "Assets/BoardImages/"
element_images = "Assets/ElementImages/"
text_images = "Assets/TextImages/"
highscoreFile = "Assets/Data/"
soundtrack = "Assets/Music/"

pygame.mixer.init()
pygame.init()
#print(pygame.mixer.music.get_busy())

# 28 Across 31 Tall 1: Empty Space 2: Tic-Tak 3: Wall 4: Ghost safe-space 5: Special Tic-Tak
originalGameBoard = [
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [3,2,2,2,2,2,2,2,2,2,2,2,2,3,3,2,2,2,2,2,2,2,2,2,2,2,2,3],
    [3,2,3,3,3,3,2,3,3,3,3,3,2,3,3,2,3,3,3,3,3,2,3,3,3,3,2,3],
    [3,6,3,3,3,3,2,3,3,3,3,3,2,3,3,2,3,3,3,3,3,2,3,3,3,3,6,3],
    [3,2,3,3,3,3,2,3,3,3,3,3,2,3,3,2,3,3,3,3,3,2,3,3,3,3,2,3],
    [3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3],
    [3,2,3,3,3,3,2,3,3,2,3,3,3,3,3,3,3,3,2,3,3,2,3,3,3,3,2,3],
    [3,2,3,3,3,3,2,3,3,2,3,3,3,3,3,3,3,3,2,3,3,2,3,3,3,3,2,3],
    [3,2,2,2,2,2,2,3,3,2,2,2,2,3,3,2,2,2,2,3,3,2,2,2,2,2,2,3],
    [3,3,3,3,3,3,2,3,3,3,3,3,1,3,3,1,3,3,3,3,3,2,3,3,3,3,3,3],
    [3,3,3,3,3,3,2,3,3,3,3,3,1,3,3,1,3,3,3,3,3,2,3,3,3,3,3,3],
    [3,3,3,3,3,3,2,3,3,1,1,1,1,1,1,1,1,1,1,3,3,2,3,3,3,3,3,3],
    [3,3,3,3,3,3,2,3,3,1,3,3,3,3,3,3,3,3,1,3,3,2,3,3,3,3,3,3],
    [3,3,3,3,3,3,2,3,3,1,3,4,4,4,4,4,4,3,1,3,3,2,3,3,3,3,3,3],
    [1,1,1,1,1,1,2,1,1,1,3,4,4,4,4,4,4,3,1,1,1,2,1,1,1,1,1,1], # Middle Lane Row: 14
    [3,3,3,3,3,3,2,3,3,1,3,4,4,4,4,4,4,3,1,3,3,2,3,3,3,3,3,3],
    [3,3,3,3,3,3,2,3,3,1,3,3,3,3,3,3,3,3,1,3,3,2,3,3,3,3,3,3],
    [3,3,3,3,3,3,2,3,3,1,1,1,1,1,1,1,1,1,1,3,3,2,3,3,3,3,3,3],
    [3,3,3,3,3,3,2,3,3,1,3,3,3,3,3,3,3,3,1,3,3,2,3,3,3,3,3,3],
    [3,3,3,3,3,3,2,3,3,1,3,3,3,3,3,3,3,3,1,3,3,2,3,3,3,3,3,3],
    [3,2,2,2,2,2,2,2,2,2,2,2,2,3,3,2,2,2,2,2,2,2,2,2,2,2,2,3],
    [3,2,3,3,3,3,2,3,3,3,3,3,2,3,3,2,3,3,3,3,3,2,3,3,3,3,2,3],
    [3,2,3,3,3,3,2,3,3,3,3,3,2,3,3,2,3,3,3,3,3,2,3,3,3,3,2,3],
    [3,6,2,2,3,3,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,3,3,2,2,6,3],
    [3,3,3,2,3,3,2,3,3,2,3,3,3,3,3,3,3,3,2,3,3,2,3,3,2,3,3,3],
    [3,3,3,2,3,3,2,3,3,2,3,3,3,3,3,3,3,3,2,3,3,2,3,3,2,3,3,3],
    [3,2,2,2,2,2,2,3,3,2,2,2,2,3,3,2,2,2,2,3,3,2,2,2,2,2,2,3],
    [3,2,3,3,3,3,3,3,3,3,3,3,2,3,3,2,3,3,3,3,3,3,3,3,3,3,2,3],
    [3,2,3,3,3,3,3,3,3,3,3,3,2,3,3,2,3,3,3,3,3,3,3,3,3,3,2,3],
    [3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
]
gameBoard = copy.deepcopy(originalGameBoard)
spriteRatio = 3/2
square = 24 # Size of each unit square
spriteOffset = square * (1 - spriteRatio) * (1/2)
(width, height) = (len(gameBoard[0]) * square, len(gameBoard) * square) # Game screen
screen = pygame.display.set_mode((width, height))
pygame.display.flip()
musicPlaying = 0 # 0: Chomp, 1: Important, 2: Siren
#foodColour = (165, 93, 53)
# foodColour = (222, 161, 133)
foodColour = "light yellow"

BINDS = {
    "up":[pygame.K_w, pygame.K_UP],
    "down":[pygame.K_s, pygame.K_DOWN],
    "right":[pygame.K_d, pygame.K_RIGHT],
    "left":[pygame.K_a, pygame.K_LEFT]
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
        self.ghosts = [Ghost(14.0, 13.5, "red", 0), Ghost(17.0, 11.5, "blue", 1), Ghost(17.0, 13.5, "pink", 2), Ghost(17.0, 15.5, "orange", 3)]
        self.pacman = Pacman(26.0, 13.5) # Center of Second Last Row
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
        self.berries = ["tile080.png", "tile081.png", "tile082.png", "tile083.png", "tile084.png", "tile085.png", "tile086.png", "tile087.png"]
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
        #print(self.ghostStates)
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
            #Changes the colour of special Tic-Taks
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
                    pygame.draw.rect(screen, (0, 0, 0), (self.pacman.col * square, self.pacman.row * square, square, square))
                elif gameBoard[int(self.pacman.row)][int(self.pacman.col)] == 5 or gameBoard[int(self.pacman.row)][int(self.pacman.col)] == 6:
                    self.forcePlayMusic("power_pellet.wav")
                    gameBoard[int(self.pacman.row)][int(self.pacman.col)] = 1
                    self.collected += 1
                    # Fill tile with black
                    pygame.draw.rect(screen, (0, 0, 0), (self.pacman.col * square, self.pacman.row * square, square, square))
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
            #print("New Level")
            win_text = font.render('press SPACE to pause/play', True, 'green')
            screen.blit(win_text, (150, 520))
            self.forcePlayMusic("intermission.wav")
            self.level += 1
            self.newLevel()

        if self.level - 1 == 8: #(self.levels[0][0] + self.levels[0][1]) // 50:
            # print("You win", self.level, len(self.levels))

            running = False
        self.softRender()

    # Render method
    def render(self):
        screen.fill((0, 0, 0)) # Flushes the screen
        # Draws game elements
        currentTile = 0
        self.displayLives()
        self.displayScore()
        for i in range(3, len(gameBoard) - 2):
            for j in range(len(gameBoard[0])):
                if gameBoard[i][j] == 3: # Draw wall
                    imageName = str(currentTile)
                    if len(imageName) == 1:
                        imageName = "00" + imageName
                    elif len(imageName) == 2:
                         imageName = "0" + imageName
                    # Get image of desired tile
                    imageName = "tile" + imageName + ".png"
                    tileImage = pygame.image.load(board_images + imageName)
                    tileImage = pygame.transform.scale(tileImage, (square, square))

                    #Display image of tile
                    screen.blit(tileImage, (j * square, i * square, square, square))

                    # pygame.draw.rect(screen, (0, 0, 255),(j * square, i * square, square, square)) # (x, y, width, height)
                elif gameBoard[i][j] == 2: # Draw Tic-Tak
                    pygame.draw.circle(screen, foodColour,(j * square + square//2, i * square + square//2), square//4)
                elif gameBoard[i][j] == 5: #Black Special Tic-Tak
                    pygame.draw.circle(screen, (0, 0, 0),(j * square + square//2, i * square + square//2), square//2)
                elif gameBoard[i][j] == 6: #White Special Tic-Tak
                    pygame.draw.circle(screen, foodColour,(j * square + square//2, i * square + square//2), square//2)

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
        #     self.drawPoints(point[0], point[1], point[2])
        self.drawBerry()
        # Updates the screen
        pygame.display.update()

    def playMusic(self, music):
        # return False # Uncomment to disable music
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
                    #Removes the ghosts from the screen
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
        if self.touchingPacman(self.berryLocation[0], self.berryLocation[1]) and not self.berryState[2] and self.levelTimer in range(self.berryState[0], self.berryState[1]):
            self.berryState[2] = True
            self.score += self.berryScore
            self.points.append([self.berryLocation[0], self.berryLocation[1], self.berryScore, 0])
            self.berriesCollected.append(self.berries[(self.level - 1) % 8])
            self.forcePlayMusic("eat_fruit.wav")
    # Displays the current score
    def displayScore(self):
        textOneUp = ["tile033.png", "tile021.png", "tile016.png"]
        textHighScore = ["tile007.png", "tile008.png", "tile006.png", "tile007.png", "tile015.png", "tile019.png", "tile002.png", "tile014.png", "tile018.png", "tile004.png"]
        index = 0
        scoreStart = 5
        highScoreStart = 11
        for i in range(scoreStart, scoreStart+len(textOneUp)):
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
        for i in range(highScoreStart, highScoreStart+len(textHighScore)):
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
            screen.blit(berryImage, (self.berryLocation[1] * square, self.berryLocation[0] * square, square, square))


    def drawPoints(self, points, row, col):
        pointStr = str(points)
        index = 0
        for i in range(len(pointStr)):
            digit = int(pointStr[i])
            tileImage = pygame.image.load(text_images + "tile" + str(224 + digit) + ".png")
            tileImage = pygame.transform.scale(tileImage, (square//2, square//2))
            screen.blit(tileImage, ((col) * square + (square//2 * index), row * square - 20, square//2, square//2))
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
        screen.blit(pacmanImage, (self.pacman.col * square + spriteOffset, self.pacman.row * square + spriteOffset, square, square))
        pygame.display.update()
        pause(5000000)
        self.gameOverCounter += 1

    def displayLives(self):
        # 33 rows || 28 cols
        # Lives[[31, 5], [31, 3], [31, 1]]
        livesLoc = [[34, 3], [34, 1]]
        for i in range(self.lives - 1):
            lifeImage = pygame.image.load(element_images + "tile054.png")
            lifeImage = pygame.transform.scale(lifeImage, (int(square * spriteRatio), int(square * spriteRatio)))
            screen.blit(lifeImage, (livesLoc[i][1] * square, livesLoc[i][0] * square - spriteOffset, square, square))

    def displayBerries(self):
        firstBerrie = [34, 26]
        for i in range(len(self.berriesCollected)):
            berrieImage = pygame.image.load(element_images + self.berriesCollected[i])
            berrieImage = pygame.transform.scale(berrieImage, (int(square * spriteRatio), int(square * spriteRatio)))
            screen.blit(berrieImage, ((firstBerrie[1] - (2*i)) * square, firstBerrie[0] * square + 5, square, square))

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

    def drawTilesAround(self, row, col):
        row = math.floor(row)
        col = math.floor(col)
        for i in range(row-2, row+3):
            for j in range(col-2, col+3):
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
                    #Display image of tile
                    screen.blit(tileImage, (j * square, i * square, square, square))

                    if gameBoard[i][j] == 2: # Draw Tic-Tak
                        pygame.draw.circle(screen, foodColour,(j * square + square//2, i * square + square//2), square//4)
                    elif gameBoard[i][j] == 5: #Black Special Tic-Tak
                        pygame.draw.circle(screen, (0, 0, 0),(j * square + square//2, i * square + square//2), square//2)
                    elif gameBoard[i][j] == 6: #White Special Tic-Tak
                        pygame.draw.circle(screen, foodColour,(j * square + square//2, i * square + square//2), square//2)

    # Flips colour of Special Tic-Taks
    def flipcolour(self):
        global gameBoard
        for i in range(3, len(gameBoard) - 2):
            for j in range(len(gameBoard[0])):
                if gameBoard[i][j] == 5:
                    gameBoard[i][j] = 6
                    pygame.draw.circle(screen, foodColour,(j * square + square//2, i * square + square//2), square//2)
                elif gameBoard[i][j] == 6:
                    gameBoard[i][j] = 5
                    pygame.draw.circle(screen, (0, 0, 0),(j * square + square//2, i * square + square//2), square//2)

    def getCount(self):
        total = 0
        for i in range(3, len(gameBoard) - 2):
            for j in range(len(gameBoard[0])):
                if gameBoard[i][j] == 2 or gameBoard[i][j] == 5 or gameBoard[i][j] == 6:
                    total += 1
        return total

    def getHighest(self):
        try:
            with open(highscoreFile + "HighScore.txt", "r", encoding="utf-8") as file:
                return int(file.read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def recordHighScore(self):
        os.makedirs(highscoreFile, exist_ok=True)
        with open(highscoreFile + "HighScore.txt", "w", encoding="utf-8") as file:
            file.write(str(self.highScore))

class Pacman:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.mouthOpen = False
        self.pacSpeed = 1/4
        self.mouthChangeDelay = 5
        self.mouthChangeCount = 0
        self.dir = 0  # 0:Up 1: Right 2: Down 3: Left
        self.newDir = 0

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
            pacmanImage = pygame.transform.scale(pacmanImage, (int(square * spriteRatio), int(square * spriteRatio)))
            screen.blit(pacmanImage, (self.col * square + spriteOffset, self.row * square + spriteOffset, square, square))
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
        screen.blit(pacmanImage, (self.col * square + spriteOffset, self.row * square + spriteOffset, square, square))

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
        self.ghostSpeed = 1/4
        self.lastLoc = [-1, -1]
        self.attackedTimer = 240
        self.attackedCount = 0
        self.deathTimer = 120
        self.deathCount = 0

    def update(self):
        # print(self.row, self.col)
        if self.target == [-1, -1] or (self.row == self.target[0] and self.col == self.target[1]) or gameBoard[int(self.row)][int(self.col)] == 4 or self.dead:
            self.setTarget()
        self.setDir()
        self.move()

        if self.attacked:
            self.attackedCount += 1

        if self.attacked and not self.dead:
            self.ghostSpeed = 1/8

        if self.attackedCount == self.attackedTimer and self.attacked:
            if not self.dead:
                self.ghostSpeed = 1/4
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
                self.ghostSpeed = 1/4

    def draw(self): # Ghosts states: Alive, Attacked, Dead Attributes: colour, Direction, Location
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
            if self.attackedTimer - self.attackedCount < self.attackedTimer//3:
                if (self.attackedTimer - self.attackedCount) % 31 < 26:
                    ghostImage = pygame.image.load(element_images + "tile0" + str(70 + (currentDir - (((self.dir + 3) % 4) * 2))) + ".png")
                else:
                    ghostImage = pygame.image.load(element_images + "tile0" + str(72 + (currentDir - (((self.dir + 3) % 4) * 2))) + ".png")
            else:
                ghostImage = pygame.image.load(element_images + "tile0" + str(72 + (currentDir - (((self.dir + 3) % 4) * 2))) + ".png")
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
        screen.blit(ghostImage, (self.col * square + spriteOffset, self.row * square + spriteOffset, square, square))

    def isValidTwo(self, cRow, cCol, dist, visited):
        if cRow < 3 or cRow >= len(gameBoard) - 5 or cCol < 0 or cCol >= len(gameBoard[0]) or gameBoard[cRow][cCol] == 3:
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

    def setDir(self): #Very inefficient || can easily refactor
        # BFS search -> Not best route but a route none the less
        dirs = [[0, -self.ghostSpeed, 0],
                [1, 0, self.ghostSpeed],
                [2, self.ghostSpeed, 0],
                [3, 0, -self.ghostSpeed]
        ]
        random.shuffle(dirs)
        best = 10000
        bestDir = -1
        for newDir in dirs:
            if self.calcDistance(self.target, [self.row + newDir[1], self.col + newDir[2]]) < best:
                if not (self.lastLoc[0] == self.row + newDir[1] and self.lastLoc[1] == self.col + newDir[2]):
                    if newDir[0] == 0 and self.col % 1.0 == 0:
                        if self.isValid(math.floor(self.row + newDir[1]), int(self.col + newDir[2])):
                            bestDir = newDir[0]
                            best = self.calcDistance(self.target, [self.row + newDir[1], self.col + newDir[2]])
                    elif newDir[0] == 1 and self.row % 1.0 == 0:
                        if self.isValid(int(self.row + newDir[1]), math.ceil(self.col + newDir[2])):
                            bestDir = newDir[0]
                            best = self.calcDistance(self.target, [self.row + newDir[1], self.col + newDir[2]])
                    elif newDir[0] == 2 and self.col % 1.0 == 0:
                        if self.isValid(math.ceil(self.row + newDir[1]), int(self.col + newDir[2])):
                            bestDir = newDir[0]
                            best = self.calcDistance(self.target, [self.row + newDir[1], self.col + newDir[2]])
                    elif newDir[0] == 3 and self.row % 1.0 == 0:
                        if self.isValid(int(self.row + newDir[1]), math.floor(self.col + newDir[2])):
                            bestDir = newDir[0]
                            best = self.calcDistance(self.target, [self.row + newDir[1], self.col + newDir[2]])
        self.dir = bestDir

    def calcDistance(self, a, b):
        dR = a[0] - b[0]
        dC = a[1] - b[1]
        return math.sqrt((dR * dR) + (dC * dC))

    def setTarget(self):
        if gameBoard[int(self.row)][int(self.col)] == 4 and not self.dead:
            self.target = [ghostGate[0][0] - 1, ghostGate[0][1]+1]
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
            elif ghost.target[0]> 15 and ghost.target[1] >= 13:
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
            if not gameBoard[self.target[0]][self.target[1]] == 3 and not gameBoard[self.target[0]][self.target[1]] == 4:
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
ghostsafeArea = [15, 13] # The location the ghosts escape to when attacked
ghostGate = [[15, 13], [15, 14]]


def draw_pause():
    pygame.draw.rect(surface,(128,128,128,150), [0,0, 800,1000])
    pygame.draw.rect(surface, 'dark gray', [200 , 100 , 280, 50], 0, 10)
    reset = pygame.draw.rect(surface, 'white', [200 , 200 , 280, 50], 0, 10)
    exit = pygame.draw.rect(surface, 'white', [200 , 300 , 280, 50], 0, 10)
    surface.blit(font.render("Game Paused",True,'black'), (280,115))
    surface.blit(font.render("Restart",True,'black'), (310,215))
    surface.blit(font.render("Exit",True,'black'), (325,315))
    screen.blit(surface,(0,0))
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
    game.ghosts = [Ghost(14.0, 13.5, "red", 0), Ghost(17.0, 11.5, "blue", 1), Ghost(17.0, 13.5, "pink", 2), Ghost(17.0, 15.5, "orange", 3)]
    for ghost in game.ghosts:
        ghost.setTarget()
    game.pacman = Pacman(26.0, 13.5)
    game.lives -= 1
    game.paused = True
    game.render()

"""def displayLaunchScreen():
    # Draw Pacman Title
    pacmanTitle = ["tile016.png", "tile000.png", "tile448.png", "tile012.png", "tile000.png", "tile013.png"]
    for i in range(len(pacmanTitle)):
        letter = pygame.image.load(text_images + pacmanTitle[i])
        letter = pygame.transform.scale(letter, (int(square * 4), int(square * 4)))
        screen.blit(letter, ((2 + 4 * i) * square, 2 * square, square, square))

    # Draw Character / Nickname
    characterTitle = [
        #Character
        "tile002.png", "tile007.png", "tile000.png", "tile018.png", "tile000.png", "tile002.png", "tile020.png", "tile004.png", "tile018.png",
        # /
        "tile015.png", "tile042.png", "tile015.png",
        # Nickname
        "tile013.png", "tile008.png", "tile002.png", "tile010.png", "tile013.png", "tile000.png", "tile012.png", "tile004.png"
    ]
    for i in range(len(characterTitle)):
        letter = pygame.image.load(text_images + characterTitle[i])
        letter = pygame.transform.scale(letter, (int(square), int(square)))
        screen.blit(letter, ((4 + i) * square, 10 * square, square, square))

    #Draw Characters and their Nickname
    characters = [
        # Red Ghost
        [
            "tile449.png", "tile015.png", "tile107.png", "tile015.png", "tile083.png", "tile071.png", "tile064.png", "tile067.png", "tile078.png", "tile087.png",
            "tile015.png", "tile015.png", "tile015.png", "tile015.png",
            "tile108.png", "tile065.png", "tile075.png", "tile072.png", "tile077.png", "tile074.png", "tile089.png", "tile108.png"
        ],
        # Pink Ghost
        [
            "tile450.png", "tile015.png", "tile363.png", "tile015.png", "tile339.png", "tile336.png", "tile324.png", "tile324.png", "tile323.png", "tile345.png",
            "tile015.png", "tile015.png", "tile015.png", "tile015.png",
            "tile364.png", "tile336.png", "tile328.png", "tile333.png", "tile330.png", "tile345.png", "tile364.png"
        ],
        # Blue Ghost
        [
            "tile452.png", "tile015.png", "tile363.png", "tile015.png", "tile193.png", "tile192.png", "tile211.png", "tile199.png", "tile197.png", "tile213.png", "tile203.png",
            "tile015.png", "tile015.png", "tile015.png",
            "tile236.png", "tile200.png", "tile205.png", "tile202.png", "tile217.png", "tile236.png"
        ],
        # Orange Ghost
        [
            "tile451.png", "tile015.png", "tile363.png", "tile015.png", "tile272.png", "tile270.png", "tile266.png", "tile260.png", "tile281.png",
            "tile015.png", "tile015.png", "tile015.png", "tile015.png", "tile015.png",
            "tile300.png", "tile258.png", "tile267.png", "tile281.png", "tile259.png", "tile260.png", "tile300.png"
        ]
    ]
    for i in range(len(characters)):
        for j in range(len(characters[i])):
            if j == 0:
                    letter = pygame.image.load(text_images + characters[i][j])
                    letter = pygame.transform.scale(letter, (int(square * spriteRatio), int(square * spriteRatio)))
                    screen.blit(letter, ((2 + j) * square - square//2, (12 + 2 * i) * square - square//3, square, square))
            else:
                letter = pygame.image.load(text_images + characters[i][j])
                letter = pygame.transform.scale(letter, (int(square), int(square)))
                screen.blit(letter, ((2 + j) * square, (12 + 2 * i) * square, square, square))
    # Draw Pacman and Ghosts
    event = ["tile449.png", "tile015.png", "tile452.png", "tile015.png",  "tile015.png", "tile448.png", "tile453.png", "tile015.png", "tile015.png", "tile015.png",  "tile453.png"]
    for i in range(len(event)):
        character = pygame.image.load(text_images + event[i])
        character = pygame.transform.scale(character, (int(square * 2), int(square * 2)))
        screen.blit(character, ((4 + i * 2) * square, 24 * square, square, square))
    # Draw PlatForm from Pacman and Ghosts
    wall = ["tile454.png", "tile454.png", "tile454.png", "tile454.png", "tile454.png", "tile454.png", "tile454.png", "tile454.png", "tile454.png", "tile454.png", "tile454.png", "tile454.png", "tile454.png", "tile454.png", "tile454.png"]
    for i in range(len(wall)):
        platform = pygame.image.load(text_images + wall[i])
        platform = pygame.transform.scale(platform, (int(square * 2), int(square * 2)))
        screen.blit(platform, ((i * 2) * square, 26 * square, square, square))
    # Credit myself
    credit = ["tile003.png", "tile004.png", "tile022.png", "tile008.png", "tile013.png", "tile015.png", "tile011.png", "tile004.png", "tile000.png", "tile012.png", "tile025.png", "tile015.png", "tile418.png", "tile416.png", "tile418.png", "tile416.png"]
    for i in range(len(credit)):
        letter = pygame.image.load(text_images + credit[i])
        letter = pygame.transform.scale(letter, (int(square), int(square)))
        screen.blit(letter, ((6 + i) * square, 30 * square, square, square))
    # Press Space to Play
    instructions = ["tile016.png", "tile018.png", "tile004.png", "tile019.png", "tile019.png", "tile015.png", "tile019.png", "tile016.png", "tile000.png", "tile002.png", "tile004.png", "tile015.png", "tile020.png", "tile014.png", "tile015.png", "tile016.png", "tile011.png", "tile000.png", "tile025.png"]
    for i in range(len(instructions)):
        letter = pygame.image.load(text_images + instructions[i])
        letter = pygame.transform.scale(letter, (int(square), int(square)))
        screen.blit(letter, ((4.5 + i) * square, 35 * square - 10, square, square))

    pygame.display.update() """


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

# Example usage
username = "Player1"
game_mode = "Classic"
displayLaunchScreen(username, game_mode)


running = True
onLaunchScreen = True
#displayLaunchScreen(username, game_mode)
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
                    game.paused = True
                    game.started = False
                    game.render()
                    pygame.mixer.music.load(soundtrack + "pacman_beginning.wav")
                    pygame.mixer.music.play()
                    musicPlaying = 1
                continue

            game.started = True

            if event.key in (pygame.K_q, pygame.K_ESCAPE):
                running = False
                game.recordHighScore()
                continue

            if event.key in (pygame.K_SPACE, pygame.K_p):
                game.paused = not game.paused
                continue

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
