import pyautogui
from PIL import Image
import cv2
import os
import numpy as np

CELL_SIZE = 70  # Kích thước mỗi ô trong ma trận (tính bằng pixel)
START_X = 1392  # Vị trí x của ô đầu tiên
START_Y = 450   # Vị trí y của ô đầu tiên


# Hàm để tải tất cả hình ảnh trong thư mục
def load_patterns(pattern_folder):
    patterns = []
    for filename in os.listdir(pattern_folder):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            img_path = os.path.join(pattern_folder, filename)
            pattern = cv2.imread(img_path)
            if pattern is not None:
                patterns.append((filename, pattern))  # Đảm bảo thêm tuple (filename, pattern)
    return patterns
    
def printColor(row,col):
    start_x = START_X + col * CELL_SIZE + 35
    start_y = START_Y + row * CELL_SIZE + 35

    pixel_value = screenshot.getpixel((start_x, start_y))
    print(f"Pixel value at ", pixel_value)

# Hàm để lấy tất cả hình ảnh từ thư mục
def load_images(image_folder):
    images = []
    for filename in os.listdir(image_folder):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            img_path = os.path.join(image_folder, filename)
            image = cv2.imread(img_path)
            if image is not None:
                images.append((filename, image))  # Thêm tuple (filename, image)
    return images
    
#screenshot = pyautogui.screenshot()
# Lưu ảnh (nếu cần)
#screenshot.save("screenshot.png")

#screenshot = Image.open("screenshot.png")

def Matrix77():
    pattern_folder = r'C:\MyStore\workspace\pt'
    image_folder = r'C:\MyStore\workspace\image'

    image = cv2.imread(r'C:\MyStore\workspace\image\cell_1_1.png', cv2.IMREAD_GRAYSCALE)
    images = load_images(image_folder)
    patterns = load_patterns(pattern_folder)
    if not patterns:
        raise ValueError("Không tìm thấy bất kỳ pattern nào.")
    if not images:
        raise ValueError("Không tìm thấy bất kỳ ảnh nào trong thư mục hình ảnh.")

    #print(patterns)
    #matrix_7x7 = [[0 for _ in range(7)] for _ in range(7)]
    matrix_7x7 = np.zeros((7, 7), dtype=int)
    i=0
    j=0

    for img_filename, image in images:
        # Khởi tạo biến để theo dõi độ khớp cao nhất
        max_matching_percentage = 0
        best_match_name = ""
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        for item in patterns:
            if isinstance(item, tuple) and len(item) == 2:
                filename, pattern = item
                
                gray_pattern = cv2.cvtColor(pattern, cv2.COLOR_BGR2GRAY)

                # Tạo đối tượng SIFT
                sift = cv2.SIFT_create()

                # Tìm các điểm đặc trưng và mô tả (descriptors) trong ảnh gốc và pattern
                keypoints_img, descriptors_img = sift.detectAndCompute(gray_image, None)
                keypoints_pattern, descriptors_pattern = sift.detectAndCompute(gray_pattern, None)

                # Sử dụng FLANN matcher để so khớp các đặc trưng
                flann = cv2.FlannBasedMatcher()
                matches = flann.knnMatch(descriptors_pattern, descriptors_img, k=2)

                # Chọn các matches tốt nhất (Dựa trên khoảng cách)
                good_matches = [m for m, n in matches if m.distance < 0.7 * n.distance]

                # Tính toán tỷ lệ % khớp dựa trên số lượng matches tốt
                matching_percentage = (len(good_matches) / len(keypoints_pattern)) * 100

                
                # Cập nhật độ khớp cao nhất và tên mẫu
                if matching_percentage > max_matching_percentage:
                    max_matching_percentage = matching_percentage
                    best_match_name1 = filename
                    best_match_name = filename.split('_')[1].split('.')[0]
                    #best_match_name = filename

        matrix_7x7[i][j] = int(best_match_name)
        # Cập nhật i và j
        if j == 6:  # Khi j đạt 6, tức là cột cuối cùng, thì chuyển sang dòng tiếp theo
            i += 1
            j = 0
        else:
            j += 1  # Nếu không phải cột cuối, tăng j lên

    return matrix_7x7