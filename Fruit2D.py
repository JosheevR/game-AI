import numpy as np
import pygame
import gymnasium as gym
from gymnasium import spaces

class FruitEnvironment(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 30}

    def __init__(self, render_mode=None, window_size=200, player_size=30, fruit_size=20):
        """
        Define self.observation_space, self.action_space, and additional game attributes
        """
        self.window = None
        self.clock = None
        self.window_size = window_size
        self.player_size = player_size
        self.fruit_size = fruit_size
        self.player_rect = None
        self.fruit_rect = None
        self.prev_distance = None
        self.done = False

        # valid actions:
        #     0 = up
        #     1 = down
        #     2 = left
        #     3 = right
        self.action_space = spaces.Discrete(4)
        self._action_to_direction = {
            0: np.array([0, -5]),
            1: np.array([0, 5]),
            2: np.array([-5, 0]),
            3: np.array([5, 0]),
        }

        self.observation_space = spaces.Box(
            low=0, 
            high=self.window_size - 1, 
            shape=(4,), 
            dtype=np.float32
        )

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self._agent_location = np.array([window_size / 2, window_size / 2], dtype=np.float32)
        self._target_location = np.array([window_size / 2, window_size / 2], dtype=np.float32)

        if self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.window_size, self.window_size))
            self.clock = pygame.time.Clock()


    def __get_observation(self):
        return np.concatenate((self._agent_location, self._target_location)).astype(np.float32) / self.window_size
    
    def __get_info(self):
        return {
            "distance": np.linalg.norm(
                self._agent_location - self._target_location, ord=1
            )
        }


    def reset(self, seed=None, options=None):
        """
        Returns: the observation of the initial state
        Reset the environment to initial state so that a new episode (independent of previous ones) may start
        """
        super().reset(seed=seed)

        self._agent_location = self.np_random.uniform(self.player_size, self.window_size - self.player_size, size=2).astype(np.float32)
        self._target_location = self.np_random.uniform(self.fruit_size, self.window_size - self.fruit_size, size=2).astype(np.float32)

        self.prev_distance = np.linalg.norm(self._agent_location - self._target_location, ord=1)

        return self.__get_observation(), self.__get_info()
    

    def step(self, action):
        direction = self._action_to_direction[action]

        self._agent_location = np.clip(
            self._agent_location + direction,
            self.player_size / 2,
            self.window_size - self.player_size / 2
        )

        current_distance = np.linalg.norm(self._agent_location - self._target_location, ord=1)

        reward = self.prev_distance - current_distance
        terminated = False

        if np.linalg.norm(self._agent_location - self._target_location) <= self.player_size:
            reward += 1000
            terminated = True
        
        self.prev_distance = current_distance
        return self.__get_observation(), reward, self.done, terminated, self.__get_info()


    def render(self):
        """
        Return: None
        Show the current environment state e.g. the graphical window for pygame
        This method must be implmeneted, but it is OK to have an empty implmentation is rendering is not important
        """

        if self.render_mode == "human":
            if self.window is None:
                pygame.init()
                pygame.display.init()
                self.window = pygame.display.set_mode((self.window_size, self.window_size))
                self.clock = pygame.time.Clock()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                    self.done = True
                    return

            self.window.fill((255, 255, 255))

            fruit_rect = pygame.Rect(
                self._target_location[0] - self.fruit_size / 2,
                self._target_location[1] - self.fruit_size / 2,
                self.fruit_size,
                self.fruit_size,
            )
            player_rect = pygame.Rect(
                self._agent_location[0] - self.player_size / 2,
                self._agent_location[1] - self.player_size / 2,
                self.player_size,
                self.player_size,
            )

            pygame.draw.rect(self.window, (255, 0, 0), fruit_rect)
            pygame.draw.rect(self.window, (0, 0, 0), player_rect)

            pygame.display.flip()
            self.clock.tick(self.metadata["render_fps"])

        elif self.render_mode == "rgb_array":
            frame = np.ones((self.window_size, self.window_size, 3), dtype=np.uint8) * 255
            frame[
                int(self._target_location[1] - self.fruit_size / 2):int(self._target_location[1] + self.fruit_size / 2),
                int(self._target_location[0] - self.fruit_size / 2):int(self._target_location[0] + self.fruit_size / 2),
                :
            ] = [255, 0, 0]
            frame[
                int(self._agent_location[1] - self.player_size / 2):int(self._agent_location[1] + self.player_size / 2),
                int(self._agent_location[0] - self.player_size / 2):int(self._agent_location[0] + self.player_size / 2),
                :
            ] = [0, 0, 0]
            return frame
        
    def close(self):
        """
        Returns: None
        This method is optional. Used to cleanup all resources (graphical window)
        """
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
            self.window = None
            self.clock = None
