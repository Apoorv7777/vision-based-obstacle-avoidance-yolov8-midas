import cv2
import time

from utils.camera import (
    initialize_camera,
    get_frame,
    release_camera
)

from models.yolo_detector import (
    YOLODetector
)

from models.depth_estimator import (
    DepthEstimator
)

from navigation.obstacle_mapper import (
    ObstacleMapper
)

from navigation.decision_engine import (
    DecisionEngine
)

from navigation.navigation_memory import (
    NavigationMemory
)

from utils.visualization import (
    draw_detections,
    show_depth_map,
    show_direction,
    draw_zones
)


# Phone webcam stream
STREAM_URL = "http://192.168.29.221:4747/video"


def main():

    print("Initializing camera...")

    cap = initialize_camera(STREAM_URL)

    print("Loading models...")

    detector = YOLODetector()
    depth_estimator = DepthEstimator()
    mapper = ObstacleMapper()
    decision_engine = DecisionEngine()
    memory = NavigationMemory()

    print("System running...")

    # FPS tracking
    fps_list = []
    inference_times = []

    detections = []
    depth_map = None

    frame_count = 0

    while True:

        loop_start = time.time()

        # Get frame
        frame = get_frame(cap)

        if frame is None:
            break

        # Resize FIRST (important)
        frame = cv2.resize(
            frame,
            (640, 480)
        )

        # Draw zones AFTER resize
        frame = draw_zones(frame)

        frame_count += 1

        # Run heavy models every 2 frames
        if frame_count % 2 == 0 or not detections:

            inf_start = time.time()

            # Object Detection
            detections = detector.detect(frame)

            # Depth Estimation
            depth_map = depth_estimator.estimate_depth(frame)

            inf_end = time.time()

            # Store inference time
            inference_time = inf_end - inf_start

            inference_times.append(
                inference_time
            )

            if len(inference_times) > 10:
                inference_times.pop(0)

        # Draw detections
        frame = draw_detections(
            frame,
            detections
        )

        # Show depth
        if depth_map is not None:
            show_depth_map(depth_map)

        # Navigation logic
        frame_width = frame.shape[1]

        zone_distances, zone_has_object = mapper.analyze_obstacles(
            detections,
            depth_map,
            frame_width
        )

        raw_direction = decision_engine.decide(
            zone_distances,
            zone_has_object
        )

        direction = memory.smooth_direction(
            raw_direction
        )

        # Print direction
        print(direction)

        # Show zone distances
        left = zone_distances["LEFT"]
        center = zone_distances["CENTER"]
        right = zone_distances["RIGHT"]

        cv2.putText(
            frame,
            f"C:{center} L:{left} R:{right}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 0),
            2
        )

        # Show navigation direction
        frame = show_direction(
            frame,
            direction
        )

        # -------- Display FPS --------

        loop_end = time.time()

        loop_fps = 1 / (loop_end - loop_start)

        fps_list.append(loop_fps)

        if len(fps_list) > 10:
            fps_list.pop(0)

        avg_display_fps = sum(fps_list) / len(fps_list)

        # -------- Inference FPS --------

        if inference_times:

            avg_inf_time = sum(
                inference_times
            ) / len(inference_times)

            inference_fps = 1 / avg_inf_time

        else:

            inference_fps = 0

        # Show FPS
        cv2.putText(
            frame,
            f"Display FPS: {int(avg_display_fps)}",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Inference FPS: {int(inference_fps)}",
            (20, 150),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 200, 255),
            2
        )

        # Show frame
        cv2.imshow(
            "Vision Navigation System",
            frame
        )

        if cv2.waitKey(1) == 27:
            break

    # Cleanup
    release_camera(cap)

    cv2.destroyAllWindows()


if __name__ == "__main__":

    main()