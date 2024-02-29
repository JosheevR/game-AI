import pygame
import random
import fruit
import numpy as np
from collections import deque

from fruit import add_fruit, collect_fruit
from player import Player
from agent import DQNAgent

class Environment:
    def __init__(self, screen_size=(600,600), max_fruits=10):
        self.max_fruits = max_fruits
        self.player = Player(size=80, screen_size=screen_size)
        self.fruits = []
        self.score = 0
        self.screen_size = screen_size
        self.agent = DQNAgent(state_shape=(11,), action_size=4)

    def get_state(self):
        player_pos = [self.player.x, self.player.y]
        fruit_positions = [fruit.topleft for fruit in self.fruits]
        state = player_pos + fruit_positions
        return state

    def step(self, action):
        prev_state = self.get_state()
        if action == 0:
            self.player.moveUp()
        elif action == 1:
            self.player.moveDown()
        elif action == 2:
            self.player.moveLeft()
        elif action == 3:
            self.player.moveRight()

        self.fruits, score_diff = collect_fruit(self.fruits, self.player.getPlayer())
        self.score += score_diff
        reward = score_diff
        new_state = self.get_state()
        done = len(self.fruits) == 0
        return np.array(new_state), reward, done, False, {}



    def reset(self):
        self.score = 0
        self.player.reset()
        self.fruits = []
        for i in range(self.max_fruits):
            self.fruits = add_fruit(self.screen_size, self.fruits, self.player)

    def run(self, episodes):
        pygame.init()
        screen = pygame.display.set_mode(self.screen_size)
        clock = pygame.time.Clock()
        running = True
        font = pygame.font.Font(None, 36)

        for i in range(episodes):
            self.reset()
            state = self.get_state()
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                # ============================== #
                #              Game
                # ============================== #
                action = self.agent.act(state)
                prev_state, action, reward, new_state, done = self.step(action)
                self.agent.remember(prev_state, action, reward, new_state, done)
                state = new_state

                # ============================== #
                #             Render
                # ============================== #

                screen.fill("white")
                pygame.draw.rect(screen, "black", self.player.getPlayer())
                for fruit in self.fruits:
                    pygame.draw.rect(screen, "green", fruit)
                score_text = font.render(f'Score: {self.score}', True, (0, 0, 0))
                screen.blit(score_text, (10, 10))

                # ============================== #
                # ============================== #

                pygame.display.flip()
                clock.tick(60)

                if done:
                    print("You collected all the fruit!")
                    break

            self.agent.replay(32)

        pygame.quit()