from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.ppo import MlpPolicy
from Fruit2D import FruitEnvironment



env = FruitEnvironment(render_mode="human")

model = PPO.load("ppo_fruit_model.zip", env=env)

observation, _ = env.reset()
for _ in range(10000):
    action, _ = model.predict(observation)
    observation, reward, done, terminated, info = env.step(int(action))
    if terminated:
        observation, _ = env.reset()
    env.render()
