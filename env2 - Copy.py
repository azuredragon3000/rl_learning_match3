import numpy as np
import pyautogui
import keyboard
import gym
import cv2
from PIL import Image
from gym import spaces
from time import sleep
from convertMatrix3 import image_to_matrix_with_patterns
import easyocr
import random
import time
import os 
from testColor import Matrix77
from potentialX import PotentialX
from potentialY import PotentialY

CELL_SIZE = 75  # Kích thước mỗi ô trong ma trận (tính bằng pixel)
START_X = 1392  # Vị trí x của ô đầu tiên
START_Y = 450   # Vị trí y của ô đầu tiên

ACTIONS = ['right', 'down', 'left', 'up']
def cropImgae(screenshot,l,t,r,b,text):
    # all game image
    crop_box = (l, t, r, b)
    # Cắt vùng ảnh
    cropped_image = screenshot.crop(crop_box)
    # Lưu ảnh đã cắt
    cropped_image.save(text)  

def captureImgae():
    # Chụp toàn màn hình
    screenshot = pyautogui.screenshot()
    # Lưu ảnh (nếu cần)
    screenshot.save("screenshot.png")
    # Mở ảnh chụp màn hình
    screenshot = Image.open("screenshot.png")
    cropImgae(screenshot,1392, 109, 1908, 1006,"cropped_image.png")
    cropImgae(screenshot,1392, 109, 1908, 450,"cropped_image1.png")
    cropImgae(screenshot,1400, 450, 1902, 955,"cropped_image2.png")
    
def stop():
    print("Chương trình tạm dừng. Nhấn Enter để tiếp tục...")
    input()
    print("Đã tiếp tục.")

def position_to_coords(position):
    # Giả sử ma trận 7x7 (7 hàng và 7 cột)
    row = position // 7
    col = position % 7
    
    # Tính toán start_x, start_y từ chỉ số (row, col)
    start_x = START_X + col * CELL_SIZE+35
    start_y = START_Y + row * CELL_SIZE+35
    
    return start_x, start_y,row,col
    
def coords(row,col):
    start_x = START_X + col * CELL_SIZE+35
    start_y = START_Y + row * CELL_SIZE+35
    
    return start_x, start_y
    
def compareMatrix(matrix, matrix_bk):
    # Kiểm tra nếu hai ma trận giống nhau
    if np.array_equal(matrix, matrix_bk):
        reward = -0.1  # Giống nhau
    else:
        reward = 0.3  # Khác nhau
    
    return reward

class Match3MouseEnv:        
    def __init__(self):
        
        # Các hành động: [Right, Down, Left, Up]
        self.action_space = ['right', 'down', 'left', 'up']
        
        # Lấy tọa độ ô trên cùng bên trái
        self.start_x = 1392  # Tọa độ X của ô đầu tiên (tùy chỉnh theo game của bạn)
        self.start_y = 450   # Tọa độ Y của ô đầu tiên
        self.cell_size = 75  # Độ dài mỗi ô
        self.previous_positions = [100] * 49  # Lưu trữ các vị trí trước đó
        self.max_history = 49  # Giới hạn lưu 49 vị trí trước đó
        #di chuyen con chuot ra khoi man hinh game
        pyautogui.moveTo(1392, 200, duration=0.5)
        
        # Tải ma trận ban đầu
        self.matrix = self._calculate_matrix()
        self.matrix_bk = self.matrix
        self.done = False  # Giả định rằng môi trường không bao giờ "kết thúc"
        #self.curPointImg = "point.png"
        
    def _calculate_matrix(self):
        captureImgae()
        # Đường dẫn tới hình ảnh
        image_path = "cropped_image2.png"
        
        pattern_folder = "C:\MyStore\workspace\pt"
        
        # Mở ảnh
        img = Image.open(image_path)
        output_folder = "C:\MyStore\workspace\image"
        os.makedirs(output_folder, exist_ok=True)

        # Resize ảnh về kích thước chuẩn (7x7 ô, mỗi ô có kích thước đồng đều)
        img_width, img_height = img.size
        cell_width = img_width//7 
        cell_height = img_height//7 
        
        matrix = np.zeros((7, 7), dtype=int)

         # Duyệt qua từng ô (7x7)
        for row in range(7):
            for col in range(7):
                # Lấy tọa độ của ô hiện tại
                left = col * cell_width
                upper = row * cell_height
                right = left + cell_width
                lower = upper + cell_height
                
                # Cắt ô từ hình ảnh
                cell = img.crop((left, upper, right, lower))
                
                # Save the cell
                cell_filename = os.path.join(output_folder, f"cell_{row+1}_{col+1}.png")
                cell.save(cell_filename)

        print("wait here")
        matrix = Matrix77()
        print(matrix)
        #input()
        return matrix
        #return image_to_matrix_with_patterns(image_path, pattern_folder)
    
    def resetArray(self):
         self.previous_positions = [100] * self.max_history
         print(self.previous_positions)
   
    def step(self, matches):   
        self.matrix_bk = self.matrix
        
        #position = 0
        #self.start_x, self.start_y = position_to_coords(position)
        #pyautogui.moveTo(self.start_x + 35, self.start_y + 35, duration=0.5)
        #pyautogui.dragRel(0, -self.cell_size, duration=0.5) 
        
        positionXs = []
        positionYs = []
        # In kết quả
        for match in matches:
            direction = match[4]
            position = match[3]
            group = match[2]
            self.start_x, self.start_y,r,l = position_to_coords(position)
            print(f"Match found in {match[0]} at position {position}: value {match[1]} appears in group {group} ({direction})")
            if direction == 'horizontal':
                parts = match[0].split() 
                number_str = parts[1] 
                # Chuyển đổi phần tử thứ 1 từ chuỗi sang số nguyên 
                number = int(number_str)
                
                potential_x = PotentialX(number, position,match[1],r,l)
                #print(potential_x)
                positionXs.append(potential_x)
            elif direction == 'vertical':
                parts = match[0].split() 
                number_str = parts[1] 
                # Chuyển đổi phần tử thứ 1 từ chuỗi sang số nguyên 
                number = int(number_str)
                
                potential_y = PotentialY(number, position,match[1],r,l)
                #print(potential_x)
                positionYs.append(potential_y)
        
        for pos in positionYs: 
            print(pos) 
            for poten in pos.pairs:
                print(" potential : ",poten.x,poten.y ) 
                a, b = coords(poten.x,poten.y)
                pyautogui.moveTo(a, b, duration=0.5)
                sleep(1)
                if poten.h == 1:
                    pyautogui.dragRel(self.cell_size, 0, duration=0.5)
                elif poten.h == 2:
                    pyautogui.dragRel(-self.cell_size, 0, duration=0.5)
                elif poten.h == 3:
                    pyautogui.dragRel(-self.cell_size, 0, duration=0.5)
                elif poten.h == 4:
                    pyautogui.dragRel(self.cell_size, 0, duration=0.5)
        #stop()
        
        for pos in positionXs: 
            print(pos) 
            for poten in pos.pairs:
                print(" potential : ",poten.x,poten.y ) 
                a, b = coords(poten.x,poten.y)
                pyautogui.moveTo(a, b, duration=0.5)
                
                if poten.h == 1:
                    pyautogui.dragRel(0, -self.cell_size, duration=0.5)  
                elif poten.h == 2:
                    pyautogui.dragRel(0, self.cell_size, duration=0.5)
                elif poten.h == 3:
                    pyautogui.dragRel(0, -self.cell_size, duration=0.5) 
                elif poten.h == 4:
                    pyautogui.dragRel(0, self.cell_size, duration=0.5)
        #stop()
        
        self._calculate_matrix()
        reward = 0
        # Quan sát mới (ma trận cập nhật)
        observation = self.matrix
        # Trả về quan sát, reward, và trạng thái done
        return observation, reward, self.done 
        #position = 3
        
        #pyautogui.moveTo(self.start_x, self.start_y, duration=0.5)
        
        
        #if position not in self.previous_positions:
            
             # Chèn giá trị vào vị trí đầu tiên (index 0), đẩy các phần tử khác xuống
            #self.previous_positions.insert(0, position)
            #print(self.previous_positions)
            # Giữ danh sách không vượt quá max_history phần tử
            #if len(self.previous_positions) > self.max_history:
            #    self.previous_positions.pop()  # Loại bỏ phần tử cuối cùng   
        
        
        # for action in ACTIONS:
            # print(f"Action: {action}")
            # # Thực hiện hành động di chuyển và kéo chuột
            # if action == 'right':
                # if self.start_x + self.cell_size > 1908:
                    # self.start_x = 1908
                # else:
                    # pyautogui.moveTo(self.start_x + 35, self.start_y + 35, duration=0.5)
                    # pyautogui.dragRel(self.cell_size, 0, duration=0.5)  # Move right
                    # self.start_x = self.start_x + self.cell_size
            # elif action == 'down':
                # if self.start_y + self.cell_size > 955:
                    # self.start_y = 955
                # else:
                    # pyautogui.moveTo(self.start_x + 35, self.start_y + 35, duration=0.5)
                    # pyautogui.dragRel(0, self.cell_size, duration=0.5)  # Move down
                    # self.start_y = self.start_y + self.cell_size
            # elif action == 'left':
                # if self.start_x - self.cell_size > 1392:
                    # pyautogui.moveTo(self.start_x + 35, self.start_y + 35, duration=0.5)
                    # pyautogui.dragRel(-self.cell_size, 0, duration=0.5)  # Move left
                    # self.start_x = self.start_x - self.cell_size
                # else:
                    # self.start_x = 1392
            # elif action == 'up':
                # if self.start_y - self.cell_size > 450:
                    # pyautogui.moveTo(self.start_x + 35, self.start_y + 35, duration=0.5)
                    # pyautogui.dragRel(0, -self.cell_size, duration=0.5)  # Move up
                    # self.start_y = self.start_y - self.cell_size
                # else:
                    # self.start_y = 450        

            #di chuyen con chuot ra khoi man hinh game
            #pyautogui.moveTo(1392, 200, duration=0.5)
            
            #if self.prePos != position:
            
            #self.matrix = self._calculate_matrix()
            #reward = compareMatrix(self.matrix,self.matrix_bk)
        #else:
        #    reward = -0.1
        #    print(" position is same")
            #input()
        #print(self.previous_positions)
        
    
    def reset(self):
        """Khởi tạo lại môi trường."""
        self.matrix = self._calculate_matrix()
        self.done = False
        return self.matrix
    
    def render(self):
        """Hiển thị ma trận (tạm thời in ra console)."""
        print("Current Matrix:")
        print(self.matrix)


