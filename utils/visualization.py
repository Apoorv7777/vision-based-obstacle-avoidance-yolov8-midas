import cv2


def draw_detections(
        frame,
        detections):

    for det in detections:

        x1, y1, x2, y2 = det["bbox"]

        label = det["label"]

        conf = det["confidence"]

        text = f"{label} {conf:.2f}"

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            text,
            (x1, y1-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0,255,0),
            2
        )

    return frame

def show_depth_map(depth_map):

    colored_depth = cv2.applyColorMap(
        depth_map,
        cv2.COLORMAP_MAGMA
    )

    cv2.imshow(
        "Depth Map",
        colored_depth
    )

def show_direction(frame, direction):

    import cv2

    cv2.putText(
        frame,
        f"Direction: {direction}",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,0,255),
        2
    )

    return frame

def draw_zones(frame):

    import cv2

    height, width = frame.shape[:2]

    left_x = int(width * 0.33)
    right_x = int(width * 0.66)

    cv2.line(
        frame,
        (left_x, 0),
        (left_x, height),
        (255,255,0),
        2
    )

    cv2.line(
        frame,
        (right_x, 0),
        (right_x, height),
        (255,255,0),
        2
    )

    return frame