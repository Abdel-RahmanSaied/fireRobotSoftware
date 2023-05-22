import cv2
import threading
from Rasb.rasb import BlynkStreaming

class CameraThread(threading.Thread):
    def __init__(self, blynkStreaming):
        threading.Thread.__init__(self)
        self.video_capture = cv2.VideoCapture(0)
        self.frame = None
        self.lock = threading.Lock()
        self.is_running = False
        self.blynk_streaming = blynkStreaming

    def run(self):
        self.is_running = True
        self.blynk_streaming.start_streaming()
        while self.is_running:
            ret, frame = self.video_capture.read()
            if not ret:
                break

            # Acquire the lock and set the current frame
            with self.lock:
                self.frame = frame

            # Enqueue the frame for processing and streaming
            self.blynk_streaming.enqueue_frame(frame)
        # Release the video capture and destroy any OpenCV windows
        self.video_capture.release()
        cv2.destroyAllWindows()

    def stop(self):
        self.is_running = False

    def get_frame(self):
        with self.lock:
            return self.frame


