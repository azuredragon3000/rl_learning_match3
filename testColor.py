import pyautogui
import cv2
import os
import numpy as np


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
    
def getNumberImage(image,patterns):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    max_matching_percentage = 0 # Khởi tạo biến để theo dõi độ khớp cao nhất
    best_match_name = "0"
    for item in patterns:
        if isinstance(item, tuple) and len(item) == 2:
            filename, pattern = item
            
            gray_pattern = cv2.cvtColor(pattern, cv2.COLOR_BGR2GRAY)

            sift = cv2.SIFT_create() # Tạo đối tượng SIFT

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
                best_match_name = filename.split('_')[1].split('.')[0]
    return best_match_name

def Matrix77(pattern_folder,image_folder):

    matrix_7x7 = np.zeros((7, 7), dtype=int)
    row=0
    col=0
    isZero = False
    images = load_images(image_folder)
    patterns = load_images(pattern_folder)
    if not patterns:
        return matrix_7x7 #raise ValueError("Không tìm thấy bất kỳ pattern nào.")
    if not images:
        return matrix_7x7 #raise ValueError("Không tìm thấy bất kỳ ảnh nào trong thư mục hình ảnh.")     

    for image in images:
        best_match_name = getNumberImage(image,patterns)
        try: 
            matrix_7x7[row][col] = int(best_match_name) # --> error happen
        except Exception as e:
            return np.zeros((7, 7), dtype=int)
        if col == 6:  # Cập nhật row và col # Khi col đạt 6, tức là cột cuối cùng, thì chuyển sang row tiếp theo
            row += 1
            col = 0
        else:
            col += 1  # Nếu không phải cột cuối, tăng col lên
    
    all_zeros = np.all(matrix_7x7 == 0)
    if all_zeros: # check if matrix return all element is 0 --> process error
        print("All elements in the 7x7 matrix are 0.")
        isZero = True
    
    return matrix_7x7,isZero
