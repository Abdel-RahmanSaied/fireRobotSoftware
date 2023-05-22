import cv2
import threading
from blynklib import Blynk


class BlynkStreaming(threading.Thread):
    def __init__(self, authToken: str, virtualPin: int):
        threading.Thread.__init__(self)
        self.authToken = authToken
        self.virtualPin = virtualPin
        self.blynk = Blynk(authToken)
        self.is_streaming = False
        self.frame_queue = []
        self.lock = threading.Lock()

    def run(self):
        self.is_streaming = True
        self.blynk.run()

    def stop_streaming(self):
        self.is_streaming = False
        self.blynk.disconnect()
        self.join()
        print("Streaming stopped")

    def enqueue_frame(self, frame):
        with self.lock:
            self.frame_queue.append(frame)

    def process_frame(self, frame):
        # Resize the frame to a desired size for model function
        resized_frame = cv2.resize(frame, (224, 224))

        # Convert the frame to JPEG format
        _, encoded_frame = cv2.imencode('.jpg', resized_frame)

        if _:
            # Convert the encoded frame to bytes
            frame_bytes = encoded_frame.tobytes()

            # Send the frame bytes to the Blynk app for streaming
            self.blynk.virtual_write(self.virtualPin, frame_bytes)

    def process_frame_queue(self):
        while self.is_streaming:
            with self.lock:
                if len(self.frame_queue) > 0:
                    frame = self.frame_queue.pop(0)
                    self.process_frame(frame)

    def start_streaming(self):
        if not self.is_streaming:
            self.start()
            print("Streaming started")

    # def stop_streaming(self):
    #     if self.is_streaming:
    #         self.stop_streaming()
    #         self.join()
