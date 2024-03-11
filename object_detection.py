from ultralytics import YOLO
import cv2

model = YOLO('yolov8n.pt')
cap =  cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()

    if success:
        results = model(frame, show=True, conf=0.4)
        for r in results:
            objs = r.names
            boxes = r.boxes
            for box in boxes:
                x1,y1,x2,y2=box.xyxy[0]
                x1,y1,x2,y2 = int(x1), int(y1), int(x2), int(y2)
                ind = int(box.cls)
                print(objs[ind], " => ", x1, y1, x2, y2)

#To stop webcam and other processes
cv2.destroyAllWindows()