import numpy as np
import pygame
import gymnasium as gym
from gymnasium import spaces

class FruitEnvironment(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}

    def __init__(self, render_mode=None, window_size=200, player_size=30, fruit_size=20):
        """
        Define self.observation_space, self.action_space, and additional game attributes
        """
        self.window_size = window_size
        self.player_size = player_size
        self.fruit_size = fruit_size
        self.player_rect = None
        self.fruit_rect = None
        self.prev_distance = None

        # valid actions:
        #     0 = up
        #     1 = down
        #     2 = left
        #     3 = right
        self.action_space = spaces.Discrete(4)

        # The following dictionary maps abstract actions from `self.action_space` to the direction we will walk in if that action is taken.
        # I.e. 0 corresponds to "right", 1 to "up" etc.
        self._action_to_direction = {
            0: np.array([5, 0]),
            1: np.array([0, 5]),
            2: np.array([-5, 0]),
            3: np.array([0, -5]),
        }

        # Observations are dictionaries with the agent's and fruit's locations
        # Each location is encodded as an element of {0, ..., window_size}^2 i.e. MultiDiscrete([window_size, window_size])
        # self.observation_space = spaces.Dict(
        #     {
        #         "agent": spaces.Box(0, self.window_size - 1, shape=(2,), dtype=int),
        #         "fruit": spaces.Box(0, self.window_size - 1, shape=(2,), dtype=int)
        #     }
        # )
        self.observation_space = spaces.Box(0, self.window_size - 1, shape=(4,), dtype=int)

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.window = None
        self.clock = None

    def __get_observation(self):
        return np.concatenate((self._agent_location, self._target_location)).astype(np.float32) / self.window_size
        #return {"agent":self._agent_location, "fruit": self._target_location}

    
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

        self._agent_location = np.zeros(shape=(2,), dtype=int) + ((self.window_size + self.player_size) / 2)
        self._target_location = self._agent_location
        while np.array_equal(self._target_location, self._agent_location):
            self._target_location = self.np_random.integers(0, self.window_size - self.fruit_size, size=2, dtype=int)

        self.player_rect = pygame.Rect(
            self._agent_location[0],  # X-coordinate of the top-left corner
            self._agent_location[1],  # Y-coordinate of the top-left corner
            self.player_size,  # Width of the rectangle
            self.player_size,  # Height of the rectangle
        )

        self.fruit_rect = pygame.Rect(
            self._target_location[0],  # X-coordinate of the top-left corner
            self._target_location[1],  # Y-coordinate of the top-left corner
            self.fruit_size,  # Width of the rectangle
            self.fruit_size,  # Height of the rectangle
        )

        self.prev_distance = np.linalg.norm(
            self._agent_location - self._target_location, ord=1
        )

        observation = self.__get_observation()
        info = self.__get_info()

        if self.render_mode == "human":
            self.__render_frame()

        return observation, info

    def step(self, action):
        direction = self._action_to_direction[action]
        next_player_location = np.clip(
            self._agent_location + direction, 0, self.window_size - self.player_size
        )

        self._agent_location = next_player_location

        # Compute the distance to the fruit
        current_distance = np.linalg.norm(
            self._agent_location - self._target_location, ord=1
        )

        # Compute the reward
        reward = 0
        if self.player_rect.colliderect(self.fruit_rect):
            reward = 1000000  # Large positive reward for reaching the fruit
            terminated = True
        else:
            # Encourage movement towards the fruit
            reward = self.prev_distance - current_distance

            # Penalize collisions
            if (self.player_rect.colliderect(self.fruit_rect) or 
                self._agent_location[0] == 0 or 
                self._agent_location[0] == self.window_size - self.player_size or 
                self._agent_location[1] == 0 or 
                self._agent_location[1] == self.window_size - self.player_size):
                reward -= 100  # Large negative reward for collisions

        # Update the previous distance
        self.prev_distance = current_distance
        
        observation = self.__get_observation()
        info = self.__get_info()

        return observation, reward, False, terminated, info



    def step(self, action):
        direction = self._action_to_direction[action]
        next_player_location = np.clip(
            self._agent_location + direction, 0, self.window_size - self.player_size
        )

        self._agent_location = next_player_location
        reward = 0
        terminated = False
        # Compute the distance to the fruit
        current_distance = np.linalg.norm(
            self._agent_location - self._target_location, ord=1
        )

        # Compute the reward
        if self.player_rect.colliderect(self.fruit_rect):
            reward = 1000000  # Large positive reward for reaching the fruit
            terminated = True
        else:
            # Encourage movement towards the fruit
            reward = self.prev_distance - current_distance
            # Penalize collisions
            if self.player_rect.colliderect(self.fruit_rect) or self._agent_location[0] == 0 or self._agent_location[0] == self.window_size - self.player_size or self._agent_location[1] == 0 or self._agent_location[1] == self.window_size - self.player_size:
                reward -= 1000  # Large negative reward for collisions

        # Update the previous distance
        self.prev_distance = current_distance
            
        observation = self.__get_observation()
        info = self.__get_info()

        if terminated:  # Reset the environment if terminated
            observation, _ = self.reset()
            
        if self.render_mode == "human":
            self.__render_frame()

        return observation, reward, terminated, False, info




    def render(self):
        """
        Return: None
        Show the current environment state e.g. the graphical window for pygame
        This method must be implmeneted, but it is OK to have an empty implmentation is rendering is not important
        """
        if self.render_mode == "rgb_array":
            return self.__render_frame()
        
    def __render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.window_size, self.window_size))
            self.clock = pygame.time.Clock()  # Initialize the clock here

        canvas = pygame.Surface((self.window_size, self.window_size))
        canvas.fill((255, 255, 255))
        pix_square_size = 1

        
        self.fruit_rect = pygame.Rect(
            self._target_location[0],  # X-coordinate of the top-left corner
            self._target_location[1],  # Y-coordinate of the top-left corner
            self.fruit_size,  # Width of the rectangle
            self.fruit_size,  # Height of the rectangle
        )
        # Draw the target
        pygame.draw.rect(
            canvas,
            (255, 0, 0),
            self.fruit_rect,
        )

        self.player_rect = pygame.Rect(
            self._agent_location[0],  # X-coordinate of the top-left corner
            self._agent_location[1],  # Y-coordinate of the top-left corner
            self.player_size,  # Width of the rectangle
            self.player_size,  # Height of the rectangle
        )
        # Draw the agent
        pygame.draw.rect(
            canvas,
            (0, 0, 0),  # Black color
            self.player_rect,
    )

        self.window.blit(canvas, canvas.get_rect())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Quit Pygame if the window is closed
                return

        if self.render_mode == "human":
            pygame.event.pump()
            pygame.display.update()
            self.clock.tick(self.metadata["render_fps"])  # Limit the frame rate



    def close(self):
        """
        Returns: None
        This method is optional. Used to cleanup all resources (graphical window)
        """
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()


import numpy as np
import pygame
import gymnasium as gym
from gymnasium import spaces
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.ppo import MlpPolicy

# Create the environment
env = FruitEnvironment()

# Wrap the environment
env = DummyVecEnv([lambda: env])

# Define and train the PPO model
model = PPO(
    MlpPolicy,
    env,
    verbose=1,
    learning_rate=0.01,
    gamma=0.9,
    n_steps=2048,
    batch_size=64,
    n_epochs=100,
)
model.learn(total_timesteps=50000)

# Use the trained model for prediction and rendering
env = FruitEnvironment(render_mode="human")
observation, _ = env.reset()
for _ in range(10000):
    action, _ = model.predict(observation)
    observation, reward, done, terminated, info = env.step(int(action))
    if terminated:
        observation, _ = env.reset()
    env.render()

# Save the model if needed
model.save("ppo_fruit_model")

# Close the environment
env.close()

