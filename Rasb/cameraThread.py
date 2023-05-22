import cv2
import threading

# Define a class for the camera thread
class CameraThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.video_capture = cv2.VideoCapture(0)  # Use the appropriate camera index if multiple cameras are available
        self.frame = None
        self.lock = threading.Lock()
        self.is_running = False

    def run(self):
        self.is_running = True
        while self.is_running:
            ret, frame = self.video_capture.read()
            if not ret:
                break

            # Acquire the lock and set the current frame
            with self.lock:
                self.frame = frame

    def stop(self):
        self.is_running = False

    def get_frame(self):
        with self.lock:
            return self.frame

# Create an instance of the camera thread
camera_thread = CameraThread()

# Start the camera thread
camera_thread.start()

# Access the frame from the main thread
while True:
    frame = camera_thread.get_frame()

    # Perform operations with the frame or display it in the main thread
    if frame is not None:
        cv2.imshow("Main Thread", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

# Stop the camera thread
camera_thread.stop()

# Wait for the camera thread to finish
camera_thread.join()

# Release the camera and close any open windows
camera_thread.video_capture.release()
cv2.destroyAllWindows()
