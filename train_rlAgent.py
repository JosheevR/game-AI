import numpy as np
import pygame
import gymnasium as gym
from gymnasium import spaces
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.ppo import MlpPolicy
from Fruit2D import FruitEnvironment

env = FruitEnvironment()
env = DummyVecEnv([lambda: env])

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
env.close()