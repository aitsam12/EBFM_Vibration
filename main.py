## Vibration Vision: Real-Time Machinery Fault Diagnosis with Event Cameras
## ECCV-NeVi Workshop 2024


from arg_parser import parse_args
from gui_utils import CustomVibrationGUI
import cv2
import numpy as np

def main():
    args = parse_args()
    gui = CustomVibrationGUI(width=640, height=480, min_freq=10, max_freq=150,
                             freq_precision=1, min_pixel_count=5, out_video=args.output)
    # Simulation of frequency map for demonstration
    freq_map = np.random.randint(0, 256, (480, 640), dtype=np.uint8)
    gui.show(freq_map, 0)
    while not gui.should_close():
        # Update frequency map or handle other logic
        pass
    gui.destroy_window()

if __name__ == "__main__":
    main()
