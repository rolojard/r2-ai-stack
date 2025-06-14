import threading
import time
import cv2
import torch

class CameraDetectionThread:
    """
    Runs YOLO-based detection on the Orin’s camera in a background daemon thread.
    On matching classes triggers attention_layer.trigger_attention().
    """

    def __init__(self, profile_manager, attention_layer, camera_index=0):
        self.profile_manager = profile_manager
        self.attention_layer = attention_layer
        self.enabled  = True
        self.running  = False
        self._thread  = None
        self._stop    = False
        self._last_trigger_time = 0
        self._cooldown = 3  # seconds

        print("[CameraDetectionThread] Loading YOLO model (GPU)...")
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        self.model.to('cuda:0')
        self.model.conf = 0.5
        self.model.iou  = 0.45

        print("[CameraDetectionThread] Opening camera...")
        self.cap = cv2.VideoCapture(camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def start(self):
        if not self.running:
            print("[CameraDetectionThread] Starting thread...")
            self.running = True
            self._thread = threading.Thread(target=self._loop, daemon=True)
            self._thread.start()

    def stop(self):
        print("[CameraDetectionThread] Stopping thread...")
        self.running = False
        self._stop = True
        if self._thread:
            self._thread.join()
        self.cap.release()

    def enable(self):
        print("[CameraDetectionThread] Enabled")
        self.enabled = True

    def disable(self):
        print("[CameraDetectionThread] Disabled")
        self.enabled = False

    def _loop(self):
        while self.running:
            if self._stop:
                break

            # Check profile-based gating
            if not self.profile_manager.is_attention_enabled() and self.enabled:
                print("[CameraDetectionThread] Profile disallows attention → disabling thread.")
                self.enabled = False
            elif self.profile_manager.is_attention_enabled() and not self.enabled:
                print("[CameraDetectionThread] Profile allows attention → enabling thread.")
                self.enabled = True

            if not self.enabled:
                time.sleep(0.5)
                continue

            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.1)
                continue

            try:
                results = self.model(frame)
                for *box, conf, cls in results.xyxy[0]:
                    class_name = self.model.names[int(cls)]
                    now = time.time()
                    if class_name and (now - self._last_trigger_time) > self._cooldown:
                        print(f"[CameraDetectionThread] Detected {class_name} at {conf:.2f}")
                        self.attention_layer.trigger_attention("camera", class_name)
                        self._last_trigger_time = now
            except Exception as e:
                print(f"[CameraDetectionThread] Inference error: {e}")

            time.sleep(0.05)
