import pyautogui
import gym
from gym import spaces
import numpy as np

class Match3Env(gym.Env):
    def __init__(self, initial_state, start_x, start_y, cell_size):
        super(Match3Env, self).__init__()
        
        self.state = np.array(initial_state)
        self.start_x = start_x  # Toạ độ góc trên bên trái cell (0, 0)
        self.start_y = start_y
        self.cell_size = cell_size  # Kích thước mỗi ô (hình vuông)
        
        # Action space và observation space như cũ
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=1, high=6, shape=self.state.shape, dtype=int)

    def reset(self):
        return self.state

    def step(self, action):
        reward = 0
        done = False

        if action == 0:  # Trái
            reward = self.move_left()
        elif action == 1:  # Phải
            reward = self.move_right()
        elif action == 2:  # Lên
            reward = self.move_up()
        elif action == 3:  # Xuống
            reward = self.move_down()

        done = self.check_game_over()

        return self.state, reward, done, {}

    def move_right(self):
        # Di chuyển chuột và hoán đổi phần tử
        self.control_mouse_drag(0, 1)
        return self.swap(0, 1)

    def move_left(self):
        self.control_mouse_drag(0, -1)
        return self.swap(0, -1)

    def move_up(self):
        self.control_mouse_drag(-1, 0)
        return self.swap(-1, 0)

    def move_down(self):
        self.control_mouse_drag(1, 0)
        return self.swap(1, 0)

    def control_mouse_drag(self, delta_row, delta_col):
        """
        Điều khiển chuột dựa trên delta_row, delta_col.
        delta_row: hướng di chuyển theo hàng (-1: lên, 1: xuống, 0: không đổi).
        delta_col: hướng di chuyển theo cột (-1: trái, 1: phải, 0: không đổi).
        """
        x_start = self.start_x + (self.cell_size // 2)
        y_start = self.start_y + (self.cell_size // 2)

        # Move tới ô trung tâm của ma trận 3x3
        pyautogui.moveTo(x_start, y_start, duration=0.5)
        pyautogui.click()

        # Tính hướng kéo chuột
        x_drag = delta_col * self.cell_size
        y_drag = delta_row * self.cell_size

        # Thực hiện drag chuột
        pyautogui.dragRel(x_drag, y_drag, duration=0.5)

    def swap(self, delta_row, delta_col):
        return 0

    def check_game_over(self):
        # Kiểm tra xem không còn nhóm ghép 3 hay không
        return 0
