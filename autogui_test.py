import pyautogui
import time

width, height = pyautogui.size()
print(width)
print(height)

time.sleep(5)

while True:
    print(pyautogui.position())
    time.sleep(1)






