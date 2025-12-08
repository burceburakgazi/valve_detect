import cv2


def show_resizable(window_name: str, frame, max_width: int = 1280, max_height: int = 720):
    """
    Frame'i ekrana sığacak şekilde ölçekleyip gösterir.
    """
    h, w = frame.shape[:2]

    scale = min(max_width / w, max_height / h, 1.0)
    new_w = int(w * scale)
    new_h = int(h * scale)

    resized = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)
    cv2.imshow(window_name, resized)
