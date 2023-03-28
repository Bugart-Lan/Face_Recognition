# This file runs the face recognition program

import cv2 as cv


def detect_faces(img):
    faces = face_cascade.detectMultiScale(img)
    img_faces = []
    coords = []
    for (x, y, w, h) in faces:
        coords.append(((x, y), (x+w, y+h)))
        img_faces.append(img[y:y+h, x:x+w])
    return img_faces, coords


face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
size = (92, 112)


if __name__ == "__main__":
    model = cv.face.EigenFaceRecognizer.create()
    model.read("eigen_face_recognizer_model_0328.xml")

    # Open webcam and start detection
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Unable to open camera.")
        exit()
    print("Successfully open camera!")
    print("Press q to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Cannot receive frame. Exiting...")

        # Convert frame image to grayscale
        gray = img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # Capture all faces
        faces, coords = detect_faces(gray)
        for i in range(len(faces)):
            face, coord = faces[i], coords[i]
            face = cv.resize(face, size)
            predicted_label, confidence = model.predict(face)
            img = cv.rectangle(img, coord[0], coord[1], 255, 4)
            name = model.getLabelInfo(predicted_label)
            name = name if bool(name) else "Unknown"
            img = cv.putText(img, name, coord[0], cv.FONT_HERSHEY_SIMPLEX, 1, 255, 4)
            print("Prediction =", predicted_label, "Confidence =", confidence)
        cv.imshow('frame', img)

        if cv.waitKey(1) == ord('q'):
            print('Quit')
            break

    cap.release()
    cv.destroyAllWindows()
