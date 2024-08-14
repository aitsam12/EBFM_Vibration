import cv2
import numpy as np
import os
import csv

class CustomFrequencyFrameGenerator:
    def __init__(self, width, height, min_freq, max_freq, freq_precision, min_pixel_count):
        self._font_face = cv2.FONT_HERSHEY_PLAIN
        self._font_scale = 1.0
        self._thickness = 1
        self._margin = 5
        self._width = width
        self._height = height
        self.output_img = np.zeros((height, width, 3), dtype=np.uint8)
        self.full_height = height
        self.full_width = width

    def _freq_to_string(self, freq):
        return "{:.2f}".format(freq)

    def print_dominant_frequency(self, freq_map):
        dominant_frequency = self._compute_dominant_value(freq_map)
        msg = "Frequency: "
        if dominant_frequency is not None:
            msg += self._freq_to_string(dominant_frequency) + " Hz"
        else:
            msg += "N/A"
        cv2.putText(self.output_img, msg, (self._margin, self._height - 10),
                    self._font_face, self._font_scale, (255, 255, 255), self._thickness)


    def print_rois_frequencies(self, freq_map, rois, ts, save_to_csv):
        for idx, roi in enumerate(rois):
            top_left, bot_right = roi
            cv2.rectangle(self.output_img, top_left, bot_right, (0, 255, 255))
            roi_freq_map = freq_map[top_left[1]:bot_right[1], top_left[0]:bot_right[0]]
            dominant_frequency = self._compute_dominant_value(roi_freq_map)
            msg = self._freq_to_string(dominant_frequency) + " Hz" if dominant_frequency is not None else "N/A"
            cv2.putText(self.output_img, msg, (bot_right[0] + self._margin, bot_right[1]),
                        self._font_face, self._font_scale, (255, 255, 255), self._thickness)
            if dominant_frequency is not None:
                save_to_csv(ts, idx + 1, dominant_frequency)

    def generate_bgr_image(self, freq_map):
        norm_freq_map = cv2.normalize(freq_map, None, 0, 255, cv2.NORM_MINMAX)
        heat_map = cv2.applyColorMap(norm_freq_map.astype(np.uint8), cv2.COLORMAP_JET)
        self.output_img = heat_map

    def _compute_dominant_value(self, freq_map):
        flattened = freq_map.flatten()
        nonzero = flattened[flattened > 0]
        if len(nonzero) == 0:
            return None
        hist, bin_edges = np.histogram(nonzero, bins=np.arange(nonzero.min(), nonzero.max() + 1))
        if len(hist) == 0:
            return None
        return bin_edges[np.argmax(hist)]
