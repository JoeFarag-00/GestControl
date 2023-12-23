import cv2
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os
import joblib

class HandRecognizer:
    def __init__(self, k_neighbors=3, image_size=(50, 50)):
        self.k_neighbors = k_neighbors
        self.image_size = image_size
        self.model = KNeighborsClassifier(n_neighbors=k_neighbors)

    def _load_images(self, folder_path, label):
        images = []
        labels = []
        for filename in os.listdir(folder_path):
            img_path = os.path.join(folder_path, filename)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                img = cv2.resize(img, self.image_size)  
                images.append(img.flatten())
                labels.append(label)
        return images, labels

    def train(self, fist_folder_path, palm_folder_path):
        fist_images, fist_labels = self._load_images(fist_folder_path, 0) 
        palm_images, palm_labels = self._load_images(palm_folder_path, 1)  

        X = np.concatenate([fist_images, palm_images])
        y = np.concatenate([fist_labels, palm_labels])

        X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_train)
        accuracy = accuracy_score(y_train, y_pred)
        print(f"Model Accuracy: {accuracy}")

    def recognize(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized_frame = cv2.resize(gray_frame, self.image_size)
        flattened_frame = resized_frame.flatten()

        prediction = self.model.predict([flattened_frame])

        if prediction == 0:
            return "Closed"
        else:
            return "Open"

    def save_weights(self, filename="Model/KNN_Weights.joblib"):
        joblib.dump(self.model, filename)
        print(f"Weights saved to {filename}")

    def load_weights(self, filename="Model/KNN_Weights.joblib"):
        if os.path.exists(filename):
            self.model = joblib.load(filename)
            print(f"Weights loaded from {filename}")
        else:
            print(f"Error: {filename} not found.")

if __name__ == "__main__":
    fist_folder = "Dataset/Fist"
    palm_folder = "Dataset/Palm"

    hand_recognizer = HandRecognizer(k_neighbors=9)
    hand_recognizer.train(fist_folder, palm_folder)
    hand_recognizer.save_weights()

    cap = cv2.VideoCapture(1)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        result = hand_recognizer.recognize(frame)
        cv2.putText(frame, f"Hand State: {result}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Hand Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
