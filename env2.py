import numpy as np
import pyautogui
import time
import os

from PIL import Image
from time import sleep
from convertMatrix3 import image_to_matrix_with_patterns
from testColor import Matrix77
from potentialX import PotentialX
from potentialY import PotentialY

CELL_SIZE = 75  # Kích thước mỗi ô trong ma trận (tính bằng pixel)
START_X = 1392  # Vị trí x của ô đầu tiên
START_Y = 450   # Vị trí y của ô đầu tiên

def startGame():
    pyautogui.moveTo(1400, 120, duration=0.5)
    #input()
    pyautogui.click()
    pyautogui.moveTo(1545, 614, duration=0.5)
    pyautogui.click()
    pyautogui.moveTo(1069, 961, duration=0.5)
    pyautogui.click()
    sleep(50)
    print("done")
    sleep(2)
    pyautogui.moveTo(1878, 382, duration=0.5)
    pyautogui.click()
    
# Hàm tìm kiếm các nhóm giá trị liên tiếp trong ma trận
def find_potential_matches(matrix, threshold=2):
    matches = []
    try:
        # Tìm kiếm trong các hàng
        for i, row in enumerate(matrix):
            for start in range(len(row) - threshold + 1):
                # Lấy nhóm liên tiếp trong hàng
                group = row[start:start + threshold]
                if len(set(group)) == 1:  # Nếu tất cả các phần tử trong nhóm là giống nhau
                    value = group[0]
                    matches.append((f"Row {i}", value, group, start, "horizontal"))
            
        # Tìm kiếm trong các cột
        for j in range(matrix.shape[1]):
            for start in range(matrix.shape[0] - threshold + 1):
                # Lấy nhóm liên tiếp trong cột
                group = matrix[start:start + threshold, j]
                if len(set(group)) == 1:  # Nếu tất cả các phần tử trong nhóm là giống nhau
                    value = group[0]
                    matches.append((f"Column {j}", value, group, start, "vertical"))

    except Exception as e:
        print(f"Error processing row {i} at start {start}: {e}")
        pyautogui.moveTo(1660, 666, duration=0.5)
        pyautogui.click()
    return matches


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
    
class Match3MouseEnv:        
    def __init__(self):
        self.start_x = 1392  # Tọa độ X của ô đầu tiên (tùy chỉnh theo game của bạn)
        self.start_y = 450   # Tọa độ Y của ô đầu tiên
        self.cell_size = 75  # Độ dài mỗi ô
        pyautogui.moveTo(1392, 200, duration=0.5)
        self.check = False
        self.count = 0
        self.again = 0

    def compare_matrices(self, matrix2):
        return not np.array_equal(matrix1, matrix2)
        
    def testMatrix(self):
        sleep(3)
        cmMatrix = self._calculate_matrix()
        return not np.array_equal(self.matrix, cmMatrix)

    def reset(self):
        """Khởi tạo lại môi trường."""
        
        if self.count > 3:
            self.count =0
            startGame()
        if self.again > 25:
            self.again =0
            startGame()
        self.matrix = self._calculate_matrix()
        self.count =0
        self.again =0
        return self.matrix
        
    def _calculate_matrix(self):
        # capture image
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
        
        try:
            matrix = Matrix77()
            self.check = True
        except Exception as e:
            #print(f"Error processing row {i} at start {start}: {e}")
            pyautogui.moveTo(1660, 666, duration=0.5)
            pyautogui.click()
            self.check = False
            #matrix = Matrix77()
            #self.reset()
            
        #print(matrix)
        #input()
        return matrix
   
    def step(self, matches):   
        self.matrix_bk = self.matrix
        
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
            else:
                print("strange")
                input()
                
        for pos in positionXs: 
            print(pos) 
            for poten in pos.pairs:
                print(" potential : ",poten.x,poten.y ) 
                a, b = coords(poten.x,poten.y)
                value = self.matrix[poten.x][poten.y]
                #pyautogui.moveTo(a, b, duration=0.5)
                sleep(1)
                if poten.h == 1:
                    if value == pos.value:
                        pyautogui.moveTo(a, b, duration=0.5)
                        pyautogui.dragRel(0, -self.cell_size, duration=0.5)  
                        if self.testMatrix():
                            print(" test x cmp h = 1 ");
                            #input();
                            return
                        else:
                            print(" test x cmp h = 1 same ");
                            self.count = self.count + 1
                            print("count: ",self.count)
                            #input();
                    else:
                        self.again = self.again + 1
                        print("again: ",self.again)
                elif poten.h == 2:
                    if value == pos.value:
                        pyautogui.moveTo(a, b, duration=0.5)
                        pyautogui.dragRel(0, self.cell_size, duration=0.5)
                        if self.testMatrix():
                            print(" test x cmp h = 2 ");
                            #input();
                            return
                        else:
                            print(" test x cmp h = 2 same ");
                            self.count = self.count + 1
                            print("count: ",self.count)
                            #input();
                    else:
                        self.again = self.again + 1   
                        print("again: ",self.again)                        
                elif poten.h == 3:
                    if value == pos.value:
                        pyautogui.moveTo(a, b, duration=0.5)
                        pyautogui.dragRel(0, -self.cell_size, duration=0.5) 
                        if self.testMatrix():
                            print(" test x cmp h = 3 ");
                            #input();
                            return
                        else:
                            print(" test x cmp h = 3 same ");
                            self.count = self.count + 1
                            print("count: ",self.count)
                            #input();
                    else:
                        self.again = self.again + 1
                        print("again: ",self.again)
                elif poten.h == 4:
                    if value == pos.value:
                        pyautogui.moveTo(a, b, duration=0.5)
                        pyautogui.dragRel(0, self.cell_size, duration=0.5)
                        if self.testMatrix():
                            print(" test x cmp h = 4 ");
                            #input();
                            return
                        else:
                            print(" test x cmp h = 4 same ");
                            self.count = self.count + 1
                            print("count: ",self.count)
                    else:
                        self.again = self.again + 1
                        print("again: ",self.again)
                elif poten.h == 5:
                    if value == pos.value:
                        pyautogui.moveTo(a, b, duration=0.5)
                        pyautogui.dragRel(-self.cell_size,0, duration=0.5)
                        if self.testMatrix():
                            print(" test x cmp h = 4 ");
                            #input();
                            return
                        else:
                            print(" test x cmp h = 4 same ");
                            self.count = self.count + 1
                            print("count: ",self.count)
                    else:
                        self.again = self.again + 1
                        print("again: ",self.again)
                elif poten.h == 6:
                    if value == pos.value:
                        pyautogui.moveTo(a, b, duration=0.5)
                        pyautogui.dragRel(self.cell_size,0, duration=0.5)
                        if self.testMatrix():
                            print(" test x cmp h = 4 ");
                            #input();
                            return
                        else:
                            print(" test x cmp h = 4 same ");
                            self.count = self.count + 1
                            print("count: ",self.count)
                    else:
                        self.again = self.again + 1
                        print("again: ",self.again)
                else:
                    print("strange")
                    input()
                    
        for pos in positionYs: 
            print(pos) 
            for poten in pos.pairs:
                print(" potential : ",poten.x,poten.y ) 
                a, b = coords(poten.x,poten.y)
                #print(self.matrix)
                #print(self.matrix.shape)
                #print(poten.x,poten.y)
                value = self.matrix[poten.x][poten.y]
                print("value",value,poten.x,poten.y,pos.value)
                #input()
                #
                sleep(1)
                if poten.h == 1:
                    if value == pos.value:
                        pyautogui.moveTo(a, b, duration=0.5)
                        pyautogui.dragRel(self.cell_size, 0, duration=0.5)
                        if self.testMatrix():
                            print(" test y cmp h = 1 ");
                            #input();
                            return
                        else:
                            print(" test y cmp h = 1 same ");
                            #co van de
                            self.count = self.count + 1
                            print("count: ",self.count)
                            #input();
                    else:
                        self.again = self.again + 1
                        print("again",self.again)
                elif poten.h == 2:
                    if value == pos.value:
                        pyautogui.moveTo(a, b, duration=0.5)
                        pyautogui.dragRel(-self.cell_size, 0, duration=0.5)
                        if self.testMatrix():
                            print(" test y cmp h = 2 ");
                            #input();
                            return
                        else:
                            print(" test y cmp h = 2 same ");
                            self.count = self.count + 1
                            print("count: ",self.count)
                            #input();
                    else:
                        self.again = self.again + 1
                        print("again: ",self.again)
                elif poten.h == 3:
                    if value == pos.value:
                        pyautogui.moveTo(a, b, duration=0.5)
                        pyautogui.dragRel(-self.cell_size, 0, duration=0.5)
                        if self.testMatrix():
                            print(" test y cmp h = 3 ");
                            #input();
                            return
                        else:
                            print(" test y cmp h = 3 same ");
                            self.count = self.count + 1
                            print("count: ",self.count)
                            #input();
                    else:
                        self.again = self.again + 1
                        print("again: ",self.again)
                elif poten.h == 4:
                    if value == pos.value:
                        pyautogui.moveTo(a, b, duration=0.5)
                        pyautogui.dragRel(self.cell_size, 0, duration=0.5)
                        if self.testMatrix():
                            print(" test y cmp h = 4 ");
                            #input();
                            return
                        else:
                            print(" test y cmp h = 4 same ");
                            self.count = self.count + 1
                            print("count: ",self.count)
                            #input();
                    else:
                        self.again = self.again + 1
                        print("again: ",self.again)
                elif poten.h == 5:
                    if value == pos.value:
                        pyautogui.moveTo(a, b, duration=0.5)
                        pyautogui.dragRel(0,-self.cell_size, duration=0.5)
                        if self.testMatrix():
                            print(" test x cmp h = 4 ");
                            #input();
                            return
                        else:
                            print(" test x cmp h = 4 same ");
                            self.count = self.count + 1
                            print("count: ",self.count)
                    else:
                        self.again = self.again + 1
                        print("again: ",self.again)
                elif poten.h == 6:
                    if value == pos.value:
                        pyautogui.moveTo(a, b, duration=0.5)
                        pyautogui.dragRel(0,self.cell_size, duration=0.5)
                        if self.testMatrix():
                            print(" test x cmp h = 4 ");
                            #input();
                            return
                        else:
                            print(" test x cmp h = 4 same ");
                            self.count = self.count + 1
                            print("count: ",self.count)
                    else:
                        self.again = self.again + 1
                        print("again: ",self.again)
                else:
                    print("strange")
                    input()
        
                    
        if self.count > 3:
            startGame()
        if self.again > 25:
            startGame()
        
        print(" out of 2 for "); 