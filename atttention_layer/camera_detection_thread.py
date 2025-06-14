#!/usr/bin/env python3
"""
camera_detection_thread.py

Runs YOLOv8-based detection on the Orin’s camera in a background daemon thread.
When configured classes are seen, triggers AttentionLayer.trigger_attention().
"""

import threading
import time
import cv2

class CameraDetectionThread:
    def __init__(self, profile_manager, attention_layer, camera_index=0,
                 model_path="yolov8n.pt", conf_thresh=0.5, iou_thresh=0.45,
                 width=320, height=240, fps=5, cooldown=3):
        """
        :param profile_manager: ProfileManager instance for gating
        :param attention_layer:  AttentionLayer instance to trigger
        :param camera_index:     OpenCV camera index
        :param model_path:       Path to YOLOv8 model (official or custom)
        :param conf_thresh:      Confidence threshold
        :param iou_thresh:       NMS IoU threshold
        :param width, height:    Capture resolution
        :param fps:              Stream fps (also governs MJPEG sleep)
        :param cooldown:         Seconds between consecutive triggers
        """
        self.profile_manager = profile_manager
        self.attention_layer = attention_layer

        self.enabled  = True
        self.running  = False
        self._stop    = False

        self._last_trigger_time = 0
        self._cooldown = cooldown
        self._frame_delay = 1.0 / fps

        # Load YOLOv8 model
        print("[CameraDetectionThread] Loading YOLOv8 model (GPU)...")
        from ultralytics import YOLO
        self.model = YOLO(model_path)
        self.model.fuse()  # optimize for inference
        self.model.conf = conf_thresh
        self.model.iou  = iou_thresh

        # Open camera
        print("[CameraDetectionThread] Opening camera...")
        self.cap = cv2.VideoCapture(camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,  width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def start(self):
        """Start the detection loop in a daemon thread."""
        if not self.running:
            print("[CameraDetectionThread] Starting detection thread...")
            self.running = True
            threading.Thread(target=self._loop, daemon=True).start()

    def stop(self):
        """Stop the detection thread and release resources."""
        print("[CameraDetectionThread] Stopping detection thread...")
        self.running = False
        self._stop    = True
        self.cap.release()

    def enable(self):
        """Enable attention triggers (profile may override)."""
        print("[CameraDetectionThread] Enabled by API")
        self.enabled = True

    def disable(self):
        """Disable attention triggers (profile may override)."""
        print("[CameraDetectionThread] Disabled by API")
        self.enabled = False

    def _loop(self):
        while self.running and not self._stop:
            # Profile-based gating
            if not self.profile_manager.is_attention_enabled() and self.enabled:
                print("[CameraDetectionThread] Profile disallows attention → disabling")
                self.enabled = False
            elif self.profile_manager.is_attention_enabled() and not self.enabled:
                print("[CameraDetectionThread] Profile allows attention → enabling")
                self.enabled = True

            if not self.enabled:
                time.sleep(0.5)
                continue

            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.1)
                continue

            try:
                # Perform inference (returns a Results object)
                results = self.model(frame, device="cuda:0")[0]

                # Iterate detections
                for det in results.boxes:
                    conf = float(det.conf[0])
                    cls  = int(det.cls[0])
                    class_name = self.model.names[cls]

                    now = time.time()
                    if now - self._last_trigger_time < self._cooldown:
                        continue

                    # Trigger attention on any detected class
                    print(f"[CameraDetectionThread] Detected '{class_name}' ({conf:.2f})")
                    self.attention_layer.trigger_attention("camera", class_name)
                    self._last_trigger_time = now

            except Exception as e:
                print(f"[CameraDetectionThread] Inference error: {e}")

            time.sleep(self._frame_delay)


