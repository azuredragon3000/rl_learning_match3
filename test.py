from pynput.mouse import Controller
import time

mouse = Controller()

print("Nhấn Ctrl+C để thoát chương trình.")
try:
    while True:
        # Lấy vị trí chuột
        x, y = mouse.position
        print(f"Vị trí chuột: X = {int(x)}, Y = {int(y)}", end="\r", flush=True)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nChương trình kết thúc.")
