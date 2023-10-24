from ultralytics import YOLO


modelPath = '/Users/mightymanh/Desktop/myCode/team-air-suas-2024/odlc/yolo/runs/detect/yolov8s_custom7/weights/best.pt'
# Load the model.
model = YOLO(modelPath)
 
# Training.
results = model.train(
   data='/Users/mightymanh/Desktop/myCode/team-air-suas-2024/simulate-images/snapshots/rectangle/data.yaml',
   epochs=5,
   batch=8,
)