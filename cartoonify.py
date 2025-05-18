# cartoonify.py

import cv2
import numpy as np
import os

def cartoonify_video(input_path, output_path):
    cap = cv2.VideoCapture(input_path)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    def cartoonify_frame(frame):
        color = cv2.bilateralFilter(frame, 9, 100, 100)
        Z = color.reshape((-1, 3)).astype(np.float32)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        K = 8
        _, labels, centers = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        centers = np.uint8(centers)
        flat_colors = centers[labels.flatten()].reshape(frame.shape)

        gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
        edges = cv2.adaptiveThreshold(cv2.medianBlur(gray, 7), 255,
                                      cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, 9, 2)
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        anime = cv2.addWeighted(flat_colors, 0.95, edges_colored, 0.05, 0)
        return anime

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cartoon = cartoonify_frame(frame)
        out.write(cartoon)

    cap.release()
    out.release()
