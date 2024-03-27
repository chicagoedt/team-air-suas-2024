from ultralytics import YOLO


modelPath = 'yolov5s'
# Load the model.
model = YOLO(modelPath)
 
# Training.
results = model.train(
   data='/Users/ethanky/Documents/GitHub/team-air-suas-2024/simulate-images/snapshots/allShapes/data.yaml',
   epochs=5,
   batch=8,
)