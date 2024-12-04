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
MATRIX_SIZE = 7

def moveAndClick(x,y,dura):
    pyautogui.moveTo(x, y, duration=dura)
    pyautogui.click()
    
def startGame():
    moveAndClick(1400,120,0.5)
    moveAndClick(1545,614,0.5)
    moveAndClick(1069,961,0.5)
    sleep(50)
    print("done")
    moveAndClick(1878,382,0.5)
    
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
        moveAndClick(1660,666,0.5)
    return matches


def cropImage(screenshot,l,t,r,b,text):
    crop_box = (l, t, r, b) # all game image
    cropped_image = screenshot.crop(crop_box) # Cắt vùng ảnh  
    cropped_image.save(text)   # Lưu ảnh đã cắt
   

def captureImage(output_folder,image_path,screenshot,cropped_image): # Chụp toàn màn hình
    screenshot = pyautogui.screenshot()
    screenshot = Image.open(screenshot)
    cropImage(screenshot,1400, 450, 1902, 955,cropped_image)
    os.makedirs(output_folder, exist_ok=True)
    img = Image.open(image_path)# Mở ảnh
    img_width, img_height = img.size # Resize ảnh về kích thước chuẩn (MATRIX_SIZExMATRIX_SIZE ô, mỗi ô có kích thước đồng đều)
    cell_width = img_width//MATRIX_SIZE
    cell_height = img_height//MATRIX_SIZE 
    
    for row in range(MATRIX_SIZE): # Duyệt qua từng ô (MATRIX_SIZExMATRIX_SIZE)
        for col in range(MATRIX_SIZE):
            left = col * cell_width # Lấy tọa độ của ô hiện tại
            upper = row * cell_height
            right = left + cell_width
            lower = upper + cell_height
            cell = img.crop((left, upper, right, lower)) # Cắt ô từ hình ảnh
            cell_filename = os.path.join(output_folder, f"cell_{row+1}_{col+1}.png") # Save the cell
            cell.save(cell_filename) #print("wait here")
            
    #return matrix

def calculateXY(row,col):
    start_x = START_X + col * CELL_SIZE+35
    start_y = START_Y + row * CELL_SIZE+35
    return start_x,start_y
    
def position_to_coords(position): # Giả sử ma trận MATRIX_SIZExMATRIX_SIZE (MATRIX_SIZE hàng và MATRIX_SIZE cột)
    row = position // MATRIX_SIZE
    col = position % MATRIX_SIZE
    start_x,start_y = calculateXY(row,col)
    return start_x, start_y,row,col
    
def coords(row,col):
    start_x,start_y = calculateXY(row,col)
    return start_x, start_y

def stop(text):
    print(text)
    input()
    
class Match3MouseEnv:        
    def __init__(self):
        self.start_x = 1392  # Tọa độ X của ô đầu tiên (tùy chỉnh theo game của bạn)
        self.start_y = 450   # Tọa độ Y của ô đầu tiên
        self.cell_size = CELL_SIZE  # Độ dài mỗi ô
        #self.check = False
        pyautogui.moveTo(1392, 200, duration=0.5) # move to the begining position
    def compare_matrices(self, matrix2):
        return not np.array_equal(matrix1, matrix2)
        
    def testMatrix(self):
        cmMatrix, isZero = self._calculate_matrix()
        #TODO - check isZero
        return not np.array_equal(self.matrix, cmMatrix)
    
    def reset(self,image_path,pattern_folder,output_folder,screenshot,cropped_image): """Khởi tạo lại môi trường."""
        self.matrix, isZero = self._calculate_matrix(image_path,pattern_folder,output_folder,screenshot,cropped_image)
        
        while isZero:
            moveAndClick(1660, 666,0.5)
            self.matrix, isZero = self._calculate_matrix(image_path,pattern_folder,output_folder,screenshot,cropped_image)
        
        return self.matrix
    
    def _calculate_matrix(self,image_path,pattern_folder,output_folder,screenshot,cropped_image):       
        captureImage(output_folder,image_path,screenshot,cropped_image) # capture image         
        matrix, isZero = Matrix77()
            
        all_zeros = np.all(matrix_7x7 == 0)
        if all_zeros: # check if matrix return all element is 0 --> process error
            print("All elements in the 7x7 matrix are 0.")
            moveAndClick(1660, 666,0.5)

        return matrix, isZero
    
    def drag(act):
        if act == "up":
            pyautogui.dragRel(0, -self.cell_size, duration=0.5)  #1 - up
        elif act == "down":
            pyautogui.dragRel(0, self.cell_size, duration=0.5)  #2 - down
        elif act == "right":
            pyautogui.dragRel(self.cell_size, 0,  duration=0.5)  #3 - right
        elif act == "left":
            pyautogui.dragRel(-self.cell_size,0,  duration=0.5)  #4 - left
            
    
    def action(value,pos.value,a,b,act):
        if value == pos.value:
            pyautogui.moveTo(a, b, duration=0.5)
            drag(act)
            while not self.testMatrix():
                print(" tim thay diem valid nhung drag that bai ? ");
                # tai sao drag that bai 
                # isZero happen ?
                # lagging - just perfrom again
                if isZero:
                    moveAndClick(1660, 666,0.5)
                pyautogui.moveTo(a, b, duration=0.5)
                drag(act)
            print(" drag thanh cong ");
    
    def calculatePotential(number, position,match,r,l):
        parts = match[0].split() 
        number_str = parts[1] 
        number = int(number_str) # Chuyển đổi phần tử thứ 1 từ chuỗi sang số nguyên 
        potential_x = PotentialX(number, position,match,r,l)
    def getPotential(pos):
        a, b = coords(poten.x,poten.y)
        value = self.matrix[poten.x][poten.y]
        return a,b,value
    
    def processAction(poten,pos,act1,act2,act3,act4,act5,act6):
        a, b, value = getPotential(poten)
        if poten.h == 1:
            action(value,pos.value,a,b,act1)
        elif poten.h == 2:
            action(value,pos.value,a,b,act2)                     
        elif poten.h == 3:
            action(value,pos.value,a,b,act3)
        elif poten.h == 4:
            action(value,pos.value,a,b,act4)
        elif poten.h == 5:
            action(value,pos.value,a,b,act5) 
        elif poten.h == 6:
            action(value,pos.value,a,b,act6)
        else:
            stop("strange - need check this place ")
            
    
    def process(potential,act1,act2,act3,act4,act5,act6):
        for pos in potential: 
            print(pos) 
            for poten in pos.pairs:
                processAction(poten,pos,act1,act2,act3,act4,act5,act6)
    def calculateDir():
        positions = []
        potential_x = calculatePotential(number, position,match[1],r,l)
        positions.append(potential_x)
        return positions
    
    def step(self, matches):   
        self.matrix_bk = self.matrix
        positionXs = []
        positionYs = []
        for match in matches:  # In kết quả
            direction = match[4]
            position = match[3]
            #group = match[2]
            self.start_x, self.start_y,r,l = position_to_coords(position) #print(f"Match found in {match[0]} at position {position}: value {match[1]} appears in group {group} ({direction})")
            
            if direction == 'horizontal':
                positionXs = calculateDir(number, position,match[1],r,l)
            elif direction == 'vertical':
                positionYs = calculateDir(number, position,match[1],r,l)
            else:
                print("strange")
                input()
        
        process(positionXs,"up","down","up","down","left","right")  
        process(positionYs,"up","down","up","down","left","right")     # sai       

        print(" done actions "); 
