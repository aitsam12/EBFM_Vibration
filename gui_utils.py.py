from vibration_utils import CustomFrequencyFrameGenerator
from metavision_sdk_ui import BaseWindow, MTWindow, UIAction, UIKeyEvent

class VibrationGUI:
    def __init__(self, width, height, min_freq, max_freq, freq_precision, min_pixel_count, out_video):
        self._frame_generator = CustomFrequencyFrameGenerator(width, height, min_freq, max_freq,
                                                              freq_precision, min_pixel_count)
        self._window = MTWindow(title="Vibration Monitoring", width=width, height=height,
                                mode=BaseWindow.RenderMode.BGR, open_directly=True)
        self.out_video = out_video
        if self.out_video:
            fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
            self.video_writer = cv2.VideoWriter(out_video, fourcc, 20, (width, height))

    def show(self, freq_map, ts):
        self._frame_generator.generate_bgr_image(freq_map)
        self._frame_generator.print_dominant_frequency(freq_map)
        self._window.show_async(self._frame_generator.output_img)
        if self.out_video:
            self.video_writer.write(self._frame_generator.output_img)

    def should_close(self):
        return self._window.should_close()

    def destroy_window(self):
        self._window.destroy()
        if self.out_video:
            self.video_writer.release()
            print(f"Video has been saved in {self.out_video}")

class CustomVibrationGUI(VibrationGUI):
    def show(self, freq_map, ts):
        super().show(freq_map, ts)
