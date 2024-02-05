import pygame
import random

FRUIT = True
PIT = False
INIT_PITS = 4

def createNewPlayer(SCREEN_SIZE):
    player_size = 25
    startingX = int(SCREEN_SIZE[0] / 2 - player_size)
    startingY = int(SCREEN_SIZE[1] / 2)
    player_rect = pygame.Rect(startingX, startingY, player_size, player_size)
    return player_rect

def moveRect(key, player_rect):
    """If the keyboard input is an arrow key, move the player 
    rectangle in the corresponding direction

    Parameters:
    key (pygame.key.getpressed()): keyboard input in pygame
    player_rect (pygame.Rect): player rectangle
    """

    if key[pygame.K_LEFT] == True:
        player_rect.move_ip(-5,0)
    if key[pygame.K_RIGHT] == True:
        player_rect.move_ip(5,0)
    if key[pygame.K_UP] == True:
        player_rect.move_ip(0,-5)
    if key[pygame.K_DOWN] == True:
        player_rect.move_ip(0,5)

def checkWallCollision(player_rect, SCREEN_SIZE, state):
    if player_rect.left == 0:
        state[1] = False
        state[2] = True
    elif player_rect.left == SCREEN_SIZE[0] - player_rect.width:
        state[1] = False
        state[2] = True
    elif player_rect.top == 0:
        state[1] = False
        state[2] = True
    elif player_rect.top == SCREEN_SIZE[1] - player_rect.height:
        state[1] = False
        state[2] = True
    
    
    return state

def checkHighScore(high_score, high_time, score, total_time):
    if score >= high_score:
        high_score = score
        high_time = total_time
        return score, total_time
    
    return high_score, high_time


def add_new_rect(SCREEN_SIZE, fruit_size, fruits, pit_size, pits, player_rect, which_rect):
    i = 0
    while i < 1000:
        if which_rect:
            rect_size = fruit_size
        else:
            rect_size = pit_size
        
        x_rand = random.randint(10, SCREEN_SIZE[0] - (2 * rect_size))
        y_rand = random.randint(10, SCREEN_SIZE[1] - (2 * rect_size))
        newRect = pygame.Rect(x_rand, y_rand, rect_size, rect_size)
        
        # Check for overlap with existing rectangles
        overlaps = False
        for fruit_rect in fruits:
            if newRect.colliderect(fruit_rect):
                overlaps = True
                break
        for pit_rect in pits:
            if newRect.colliderect(pit_rect):
                overlaps = True
                break

        if len(pits) <= INIT_PITS:
            if newRect.colliderect(player_rect):
                overlaps = True

        if not overlaps:
            if which_rect:
                fruits.append(newRect)
            else:
                pits.append(newRect)
            break