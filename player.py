import pygame

class Player:
    def __init__(self, size, screen_size):
        self.move_speed = 5
        self.moveable_area = screen_size
        self.size = size
        self.x = (self.moveable_area[0] - size) / 2
        self.y = (self.moveable_area[1] - size) / 2

    def reset(self):
        self.x = (self.moveable_area[0] - self.size) / 2
        self.y = (self.moveable_area[1] - self.size) / 2
    
    def getPlayer(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)
    
    def moveUp(self):
        if self.y - self.move_speed >= 0:
            self.y -= self.move_speed

    def moveDown(self):
        if self.y + self.move_speed <= self.moveable_area[1] - self.size:
            self.y += self.move_speed

    def moveLeft(self):
        if self.x - self.move_speed >= 0:
            self.x -= self.move_speed

    def moveRight(self):
        if self.x + self.move_speed <= self.moveable_area[0] - self.size:
            self.x += self.move_speed