from ultralytics import YOLO


class YOLODetector:

    def __init__(self,
                 model_path="yolov8n.pt"):

        self.model = YOLO(model_path)

        self.class_names = (
            self.model.names
        )

    def detect(self, frame):

        results = self.model(
            frame,
            verbose=False
        )

        detections = []

        for r in results:

            for box in r.boxes:

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                conf = float(
                    box.conf[0]
                )

                cls = int(
                    box.cls[0]
                )

                label = self.class_names[
                    cls
                ]

                detections.append({

                    "bbox": (
                        x1,
                        y1,
                        x2,
                        y2
                    ),

                    "confidence": conf,

                    "label": label

                })

        return detections