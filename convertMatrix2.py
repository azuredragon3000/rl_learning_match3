import cv2
import numpy as np
import os
from PIL import Image

def remove_black_background(image):
    """
    Loại bỏ nền màu đen khỏi ảnh.
    """
    # Chuyển ảnh sang không gian màu HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Tạo mask giữ lại các vùng không phải màu đen (độ sáng V > 50)
    mask = cv2.inRange(hsv, (0, 0, 50), (180, 255, 255))

    # Áp dụng mask để xóa nền đen
    result = cv2.bitwise_and(image, image, mask=mask)
    return result

def image_to_matrix_with_opencv(image_path):
    """
    Phân tích hình ảnh thành ma trận 8x8 dựa trên màu sắc, sử dụng OpenCV để xử lý.
    """
    # Load hình ảnh
    image = cv2.imread(image_path)

    # Loại bỏ nền đen
    image_no_bg = remove_black_background(image)
    img = Image.open(image_path)
    # Kích thước mỗi ô (75x75 pixel)
    img_width, img_height = img.size
    cell_width = 70
    cell_height = 70

    # Thư mục lưu hình ảnh cắt nhỏ
    output_folder = "C:\MyStore\workspace\image"
    os.makedirs(output_folder, exist_ok=True)

    # Khởi tạo ma trận 7x7
    matrix = np.zeros((7, 7), dtype=int)

    # Định nghĩa màu sắc và gán giá trị số
    color_map = {
        (255, 0, 0): 1,    # Đỏ
        (0, 255, 0): 2,    # Xanh lá
        (0, 0, 255): 3,    # Xanh dương
        (255, 255, 0): 4,  # Vàng
        (255, 165, 0): 5,  # Cam
        (128, 0, 128): 6,  # Tím
        (0, 255, 255): 7,  # Xanh ngọc
        (255, 255, 255): 8, # Trắng (nếu cần)
    }

    # Duyệt qua từng ô (7x7)
    for row in range(7):
        for col in range(7):
            # Tính tọa độ của ô hiện tại
            left = col * cell_width
            top = row * cell_height
            right = left + cell_width
            bottom = top + cell_height
            
            # Cắt ô từ hình ảnh đã loại bỏ nền đen
            cell = image_no_bg[top:bottom, left:right]

            # Lưu hình ảnh ô
            cell_filename = os.path.join(output_folder, f"cell_{row+1}_{col+1}.png")
            cv2.imwrite(cell_filename, cell)

            # Tính màu trung bình (bỏ qua các điểm nền đen)
            mask = np.any(cell != [0, 0, 0], axis=-1)
            avg_color = cell[mask].mean(axis=0).astype(int) if mask.any() else [0, 0, 0]

            # Tìm màu gần nhất trong color_map
            closest_color = min(color_map.keys(), key=lambda c: np.linalg.norm(np.array(c) - avg_color))
            matrix[row, col] = color_map[closest_color]

    return matrix
