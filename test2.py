import pyautogui
import time
time.sleep(6)
pyautogui.move(70,70)
#pyautogui.click()    # click to put drawing program in focus
#time.sleep(3)
#pyautogui.click()
pyautogui.dragRel(60, 0, duration=1)   # move right
time.sleep(1)
pyautogui.move(-70,0)
pyautogui.dragRel(60, 0, duration=1)   # move right
