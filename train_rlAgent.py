import numpy as np
import pygame
import gymnasium as gym
from gymnasium import spaces
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.ppo import MlpPolicy
from Fruit2D import FruitEnvironment

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