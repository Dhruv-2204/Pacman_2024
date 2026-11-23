# MAP PAGE
import pygame
from pygame import image, Color

moveimage = pygame.image.load('images/pacmanmovemap.png')
dotimage = pygame.image.load('images/pacmandotmap.png')

def checkMovePoint(p):
    global moveimage
    if p.x + p.movex < 0:
        p.x = p.x + 600
    if p.x + p.movex > 600:
        p.x = p.x - 600

    pixel_x = int(p.x + p.movex)
    pixel_y = int(p.y + p.movey - 80)
    if pixel_x < 0 or pixel_x >= moveimage.get_width() or pixel_y < 0 or pixel_y >= moveimage.get_height():
        p.movex = p.movey = 0
    elif moveimage.get_at((pixel_x, pixel_y)) != Color('black'):
        p.movex = p.movey = 0

def checkDotPoint(x, y):
    global dotimage
    pixel_x = int(x)
    pixel_y = int(y)
    if pixel_x < 0 or pixel_x >= dotimage.get_width() or pixel_y < 0 or pixel_y >= dotimage.get_height():
        return False
    if dotimage.get_at((pixel_x, pixel_y)) == Color('black'):
        return True
    return False

def _is_move_pixel(x, y):
    pixel_x = int(x)
    pixel_y = int(y)
    return (
        0 <= pixel_x < moveimage.get_width()
        and 0 <= pixel_y < moveimage.get_height()
        and moveimage.get_at((pixel_x, pixel_y)) == Color('black')
    )


def getPossibleDirection(g):
    global moveimage
    if g.x - 20 < 0:
        g.x = g.x + 600
    if g.x + 20 > 600:
        g.x = g.x - 600
    directions = [0, 0, 0, 0]
    if g.x + 20 < 600 and _is_move_pixel(g.x + 20, g.y - 80):
        directions[0] = 1
    if g.x < 600 and g.x >= 0 and _is_move_pixel(g.x, g.y - 60):
        directions[1] = 1
    if g.x - 20 >= 0 and _is_move_pixel(g.x - 20, g.y - 80):
        directions[2] = 1
    if g.x < 600 and g.x >= 0 and _is_move_pixel(g.x, g.y - 100):
        directions[3] = 1
    return directions
