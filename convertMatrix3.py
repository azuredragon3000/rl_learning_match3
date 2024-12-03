import cv2
import numpy as np
import os

def load_patterns(pattern_folder):
    """
    Load các pattern mẫu từ thư mục.
    """
    patterns = {}
    for i in range(1, 7):  # Giả sử pattern có tên pattern_1.png, ..., pattern_6.png
        pattern_path = os.path.join(pattern_folder, f"pattern_{i}.png")
        pattern = cv2.imread(pattern_path, cv2.IMREAD_UNCHANGED)
        if pattern is not None:
            patterns[i] = pattern
        else:
            print(f"Không thể load pattern: {pattern_path}")
    return patterns

def match_with_patterns(cell, patterns):
    """
    So sánh ô với các pattern và trả về nhãn của pattern khớp nhất.
    """
    max_score = -1
    matched_label = 0

    for label, pattern in patterns.items():
        # Resize pattern nếu cần để khớp kích thước với cell
        resized_pattern = cv2.resize(pattern, (cell.shape[1], cell.shape[0]))
        
        # So sánh cell với pattern bằng cv2.matchTemplate
        result = cv2.matchTemplate(cell, resized_pattern, cv2.TM_CCOEFF_NORMED)
        score = result.max()
        
        if score > max_score:
            max_score = score
            matched_label = label

    return matched_label

def match_with_orb(cell, patterns):
    orb = cv2.ORB_create()
    kp_cell, des_cell = orb.detectAndCompute(cell, None)
    
    best_match_label = 0
    max_matches = 0

    # Duyệt qua các pattern mẫu và so sánh với cell
    for label, pattern in patterns.items():
        kp_pattern, des_pattern = orb.detectAndCompute(pattern, None)
        
        # Khởi tạo matcher
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des_cell, des_pattern)

        # Tính số lượng matches
        num_matches = len(matches)

        # Cập nhật match tốt nhất
        if num_matches > max_matches:
            max_matches = num_matches
            best_match_label = label

    return best_match_label

def match_with_histogram(cell, patterns):
    """
    So sánh histogram của ô với các pattern.
    """
    # Chuyển cell và pattern sang không gian màu HSV
    cell_hsv = cv2.cvtColor(cell, cv2.COLOR_BGR2HSV)
    max_score = -1
    matched_label = 0

    for label, pattern in patterns.items():
        pattern_hsv = cv2.cvtColor(pattern, cv2.COLOR_BGR2HSV)

        # Tính histogram cho cả ô và pattern
        cell_hist = cv2.calcHist([cell_hsv], [0, 1, 2], None, [16, 16, 16], [0, 256, 0, 256, 0, 256])
        pattern_hist = cv2.calcHist([pattern_hsv], [0, 1, 2], None, [16, 16, 16], [0, 256, 0, 256, 0, 256])

        # So sánh histogram sử dụng phương pháp correlation
        score = cv2.compareHist(cell_hist, pattern_hist, cv2.HISTCMP_CORREL)

        if score > max_score:
            max_score = score
            matched_label = label

    return matched_label


def image_to_matrix_with_patterns(image_path, pattern_folder):
    """
    Phân tích hình ảnh thành ma trận 8x8 dựa trên pattern matching.
    """
    

    # Load patterns
    patterns = load_patterns(pattern_folder)
    if not patterns:
        raise ValueError("Không tìm thấy bất kỳ pattern nào.")

    # Load ảnh
    image = cv2.imread(image_path)
    # Kích thước mỗi ô (75x75 pixel)
    cell_width = 75
    cell_height = 75

    # Khởi tạo ma trận 7x7
    matrix = np.zeros((7, 7), dtype=int)

    # Duyệt qua từng ô (7x7)
    for row in range(7):
        for col in range(7):
            # Tính tọa độ của ô hiện tại
            left = col * cell_width
            top = row * cell_height
            right = left + cell_width
            bottom = top + cell_height

            # Cắt ô từ ảnh gốc
            cell = image[top:bottom, left:right]

            # So khớp với các pattern
            label = match_with_histogram(cell, patterns)
            matrix[row, col] = label

    return matrix
