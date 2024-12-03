import pyautogui
import gym
import keyboard
import numpy as np
import random
import torch
import torch.optim as optim
import torch.nn as nn
import os

from env2 import Match3MouseEnv
from gym import spaces
from time import sleep
from nn import QNetwork

# Hàm tìm kiếm các nhóm giá trị liên tiếp trong ma trận
def find_potential_matches(matrix, threshold=2):
    matches = []
    
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
    
    return matches
    
# Q-learning parameters
ALPHA = 0.1    # Learning rate
GAMMA = 0.9    # Discount factor
EPSILON = 0.2  # Exploration rate
EPISODES = 2000  # Number of training episodes
LEARNING_RATE = 0.005  # Tốc độ học
ACTIONS = ['right', 'down', 'left', 'up'] # Danh sách các hành động (tương ứng với môi trường)

if __name__ == "__main__":
    #prePos =0;
    position = 0;
    # Khởi tạo môi trường
    env = Match3MouseEnv()
    # Create the Q-network
    input_dim = 49  # 7x7 matrix flattened
    action_dim = 49  # Number of actions
    q_network = QNetwork(input_dim, action_dim)
    optimizer = optim.Adam(q_network.parameters(), lr=LEARNING_RATE)
    loss_fn = nn.MSELoss()
    
    # Nạp trọng số đã lưu (nếu có)
    if os.path.exists("q_network_weights.pth"):
        q_network.load_state_dict(torch.load("q_network_weights.pth"))
        print("Loaded saved model weights from q_network_weights.pth")
    else:
        print("No saved model weights found. Training from scratch.")

    current_state = env.reset()
     # Bắt đầu học
    for episode in range(EPISODES):
        print(f"Episode {episode + 1}/{EPISODES}")
        # Reset môi trường
        state_tensor = torch.tensor(current_state, dtype=torch.float32).flatten().unsqueeze(0)

        # state_tensor giờ có kích thước [1, 49]
        print("State tensor shape:", state_tensor.shape)
        
        # Dự đoán Q-values bằng mạng nơ-ron
        q_values = q_network(state_tensor)
        print("Q-values shape:", q_values.shape)
        print("Q-values :", q_values)
        #position = torch.argmax(q_values).item()
        print("pos :", position)
        #input()
        #if position == 47:
        ##    position = 0
        #else:
        #    position = position+1
        prePos = position
        print("Position: ",position)
        
       
        #tam thoi nen xoa sau nay
        current_state = env.reset()
        
        # find match 3 pattern
        print(current_state)
        
        
        matches = find_potential_matches(current_state, threshold=2)

           
        #input()
        #new_observation, reward, done = env.step(position)
        new_observation, reward, done = env.step(matches)
        # Chuyển trạng thái thành tensor
        state_tensor = torch.tensor(current_state, dtype=torch.float32).flatten().unsqueeze(0)
        predicted_q = q_network(state_tensor)[0, position] # Giá trị Q dự đoán
        print("predich: ",predicted_q)
        #input()
        target_q = predicted_q
        # Tìm trạng thái tiếp theo
        next_state = new_observation.flatten()
        
        next_state_tensor = torch.tensor(next_state, dtype=torch.float32).unsqueeze(0)
        if torch.allclose(state_tensor, next_state_tensor, atol=1e-5):  # atol là tham số sai số tuyệt đối
            print("same")
            with torch.no_grad():
                target_q = target_q -0.5
            #input()
            #env.resetArray()
        else:
            env.resetArray()
            # Tính giá trị Q mục tiêu (target Q-value)
            with torch.no_grad():  # Không tính gradient cho target
                target_q = reward + GAMMA * torch.max(q_network(next_state_tensor))
            #input()
        
        print(" GAMMA * torch.max(q_network(next_state_tensor)) ", GAMMA * torch.max(q_network(next_state_tensor)))
        print(" Reward : ",reward)
        print(" Reward : ",target_q)
        print(" Reward : ",predicted_q)
        # Tính loss
        loss = loss_fn(predicted_q, target_q)

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        print(f"Loss at step: {loss.item()}")

        # Chuyển sang trạng thái tiếp theo
        current_state = next_state
        sleep(2)
        
    # Lưu trọng số sau huấn luyện
    torch.save(q_network.state_dict(), "q_network_weights.pth")
    print("Model weights saved to q_network_weights.pth")   