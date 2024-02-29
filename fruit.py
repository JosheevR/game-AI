import pygame
import random

def add_fruit(SCREEN_SIZE, fruits, player, fruit_size=16):
    x_rand = random.randint(10, SCREEN_SIZE[0] - (2 * fruit_size))
    y_rand = random.randint(10, SCREEN_SIZE[1] - (2 * fruit_size))
    newFruit = pygame.Rect(x_rand, y_rand, fruit_size, fruit_size)
    
    overlaps = False
    for fruit in fruits:
        if newFruit.colliderect(fruit):
            overlaps = True
            break

    for fruit in fruits:
        if newFruit.colliderect(player.getPlayer()):
            overlaps = True
            break

    if not overlaps:
        fruits.append(newFruit)
    
    return fruits

def collect_fruit(fruits, player):
    score_diff = 0
    for fruit in fruits:
        if player.colliderect(fruit):
            fruits.remove(fruit)
            score_diff += 1
    return fruits, score_diff

