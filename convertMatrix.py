from PIL import Image
import numpy as np
import os

def image_to_matrix(image_path):
    # Mở ảnh
    img = Image.open(image_path)
    output_folder = "C:\MyStore\workspace\image"
    os.makedirs(output_folder, exist_ok=True)

    # Resize ảnh về kích thước chuẩn (7x7 ô, mỗi ô có kích thước đồng đều)
    img_width, img_height = img.size
    cell_width = img_width//8 
    cell_height = 75 

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
        
            # Lấy màu trung bình trong ô
            avg_color = np.array(cell).mean(axis=(0, 1)).astype(int)[:3]
            avg_color = tuple(avg_color)  # Chuyển thành tuple để so sánh

            # Gán giá trị số tương ứng với màu sắc
            closest_color = min(color_map.keys(), key=lambda c: np.linalg.norm(np.array(c) - np.array(avg_color)))
            matrix[row, col] = color_map[closest_color]

    return matrix
