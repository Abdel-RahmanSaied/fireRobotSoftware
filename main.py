import cv2
from Rasb.rasb import BlynkStreaming
from Rasb.streamingCam import CameraThread
from model.ModelPredict import Model


def run_camera_stream(auth_token, virtual_pin):
    blynk_streaming = BlynkStreaming(auth_token, virtual_pin)
    camera_thread = CameraThread(blynk_streaming)
    model_instance = Model("model/model.h5")
    model = model_instance.load_model()

    # Start the camera thread
    camera_thread.start()

    # Start streaming to Blynk
    # blynk_streaming.start()

    # Access the frame from the main thread
    while True:
        frame = camera_thread.get_frame()

        # Perform operations with the frame or display it in the main thread
        if frame is not None:
            pred = model_instance.predict_input_image(frame, model)

            # Determine the class label with the highest confidence score and create a result string
            if pred['fire_images'] > pred['non_fire_images'] and round(pred['fire_images'] * 100, 2) > 52:
                res = f"Fire {round(pred['fire_images'] * 100, 2)} %"
            else:
                # res = f"No Fire {round(pred['non_fire_images']*100, 2)} %"
                res = "No Fire"

            frame = cv2.putText(frame, str(res), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,
                                        cv2.LINE_AA)
            cv2.imshow("Main Thread", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
            break

    # Stop streaming to Blynk
    blynk_streaming.stop_streaming()

    # Stop the camera thread
    camera_thread.stop()

    # Wait for the camera thread to finish
    camera_thread.join()


# Usage example
if __name__ == '__main__':
    authToken = "oE0qoNY_Qm5hiWksRXs96WlTGOcqDow4"
    virtualPin = 1
    run_camera_stream(authToken, virtualPin)
