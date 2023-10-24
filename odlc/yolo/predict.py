from ultralytics import YOLO

modelPath = '/Users/mightymanh/Desktop/myCode/team-air-suas-2024/odlc/yolo/runs/detect/yolov8s_custom7/weights/best.pt'
model = YOLO(modelPath)

model.predict(
    source = '/Users/mightymanh/Desktop/myCode/team-air-suas-2024/simulate-images/snapshots/triangle/test/images/',
    conf = 0.25,
    save=True
)