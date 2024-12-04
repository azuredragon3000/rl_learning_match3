import pyautogui
from env2 import Match3MouseEnv
from env2 import find_potential_matches
from env2 import startGame
from time import sleep

EPISODES = 2000
    
if __name__ == "__main__":
    env = Match3MouseEnv() # reset enviroment
    #check = False # 
    # Đường dẫn tới hình ảnh
    image_path = "cropped_image.png"
    pattern_folder = "C:\MyStore\workspace\pt" 
    output_folder = "C:\MyStore\workspace\image"
    screenshot = "screenshot.png"
    cropped_image = "cropped_image.png"
    
    for episode in range(EPISODES):
        print(f"Episode {episode + 1}/{EPISODES}")
        current_state = env.reset(image_path,pattern_folder,output_folder,screenshot,cropped_image) # reset env and return matrix
        matches = find_potential_matches(current_state, threshold=2)
        env.step(matches)
        #print(env.check)
        #if env.check:   
        #print(" ok i done step")
