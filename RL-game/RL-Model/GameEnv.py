import gymnasium as gym
from gymnasium import spaces
import pygame
import module
import numpy as np

# Global variables
BACKGROUND_COLOR = (200, 200, 200)
SCREEN_SIZE = [1280,720]
MAX_FRUITS = 5
INIT_PITS = 4
FRUIT = True
PIT = False
FRUIT_SIZE = 10
PIT_SIZE = 50


# RL Properties
N_DISCRETE_ACTIONS = 5
N_CHANNELS = 10

	
class GameEnv(gym.Env):
	"""Custom Environment that follows gym interface"""

	def __init__(self):
		super(GameEnv, self).__init__()
		# Define action and observation space
		# They must be gym.spaces objects
		# Example when using discrete actions:
		self.action_space = spaces.Discrete(N_DISCRETE_ACTIONS)
		# Example for using image as input (channel-first; channel-last also works):
		self.observation_space = spaces.Box(low=0, high=255,
											shape=(N_CHANNELS, HEIGHT, WIDTH), dtype=np.float32)

	def step(self, action):
		
		return observation, reward, done, info
	
	def reset(self):
		self.player_rect = module.createNewPlayer(SCREEN_SIZE)
		self.score = 0
		self.current_time = 0
		self.fruits = []
		self.pits = []
		start_time = pygame.time.get_ticks()
		current_run_start_time = pygame.time.get_ticks()
		self.current_time = 0
		for i in range(MAX_FRUITS):
			module.add_new_rect(SCREEN_SIZE, FRUIT_SIZE, self.fruits, PIT_SIZE, self.pits, self.player_rect, FRUIT)
		for i in range(INIT_PITS):
			module.add_new_rect(SCREEN_SIZE, FRUIT_SIZE, self.fruits, PIT_SIZE, self.pits, self.player_rect, PIT)
        
		self.num_fruits = len(self.fruits) 
		self.num_pits = len(self.pits)

		observation = []
		
		return observation  # reward, done, info can't be included
