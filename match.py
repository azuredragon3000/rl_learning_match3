import pyautogui
import numpy as np
from env2 import Match3MouseEnv
from env2 import find_potential_matches
from env2 import startGame
from time import sleep

EPISODES = 2000
    
if __name__ == "__main__":
    #startGame()
    env = Match3MouseEnv()
    check = False
    for episode in range(EPISODES):
        print(f"Episode {episode + 1}/{EPISODES}")
        #tam thoi nen xoa sau nay
        current_state = env.reset()
        print(env.check)
        if env.check:
            matches = find_potential_matches(current_state, threshold=2)
            env.step(matches)
            print(" ok i done step")