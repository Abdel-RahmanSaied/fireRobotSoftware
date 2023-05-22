import numpy as np
import cv2
import os
# import kerasmodel.h5
from keras.models import load_model

class Model:
    def __init__(self, modelPath):
        self.modelPath = modelPath

    def load_model(self,):
        try:
            model = load_model(self.modelPath)
        except Exception as e:
            return f"Model Not Found with error {e}"
        else:
            return model

    def predict_input_image(self, img, model):
        model = model
        class_names = ['fire_images', 'non_fire_images']
        resized_frame = cv2.resize(img, (224, 224))
        # Reshape the input image into a 4D array
        img_4d = resized_frame.reshape(-1, 224, 224, 3)

        # Use the loaded model to predict the class of the input image
        prediction = model.predict(img_4d)[0]

        # If the prediction value is greater than 0.5, it is considered as fire
        if prediction > 0.5:
            # probability of fire and non-fire
            pred = [1 - prediction, prediction]
        else:
            # probability of non-fire and fire
            pred = [1 - prediction, prediction]

        # Create a dictionary containing the confidence scores for each class
        confidences = {class_names[i]: float(pred[i]) for i in range(2)}
        print(confidences)
        return confidences