import cv2

def initialize_camera(stream_url):

    cap = cv2.VideoCapture(stream_url)

    if not cap.isOpened():
        raise RuntimeError(
            "Cannot open camera stream"
        )

    return cap


def get_frame(cap):

    # Drop buffered frames
    for _ in range(3):
        cap.grab()

    ret, frame = cap.read()

    if not ret:
        return None

    return frame


def release_camera(cap):

    cap.release()