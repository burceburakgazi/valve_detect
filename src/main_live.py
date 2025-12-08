import cv2

from config_loader import load_env, load_camera_config
from camera.camera_stream import CameraStream
from utils.drawing import show_resizable
from detection.model_loader import load_valve_crate_model
from detection.valve_crate_detector import detect_crates_and_valves


def draw_detections(frame, crates, valves):
    """
    Tespit edilen kasaları ve vanaları frame üzerine çizer.
    Kasalar: yeşil kutu
    Vanalar: kırmızı kutu
    """
    # Kasalar
    for c in crates:
        x1, y1, x2, y2 = c["box"]
        conf = c["score"]
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"crate {conf:.2f}",
            (x1, max(0, y1 - 5)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            1,
        )

    # Vanalar
    for v in valves:
        x1, y1, x2, y2 = v["box"]
        conf = v["score"]
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(
            frame,
            f"valve {conf:.2f}",
            (x1, max(0, y1 - 5)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            1,
        )


def main():
    print("[DEBUG] main_live.py çalışmaya başladı")

    # 1) .env varsa yükle
    load_env()

    # 2) cameras.yaml dosyasını oku
    cameras = load_camera_config()

    cam1_cfg = cameras.get("cam1")
    if cam1_cfg is None:
        raise ValueError("cameras.yaml içinde 'cam1' tanımı bulunamadı.")

    cam_name = cam1_cfg.get("name", "Camera 1")
    cam_rtsp = cam1_cfg["rtsp"]

    # 3) YOLO modelini yükle
    model = load_valve_crate_model()

    # 4) Kamerayı aç
    cam = CameraStream(rtsp_url=cam_rtsp, name=cam_name)
    if not cam.open():
        return

    window_name = f"Live - {cam_name}"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    print("[INFO] Canlı görüntü + YOLO tespiti başlıyor. Çıkmak için 'q' veya ESC.")

    while True:
        ret, frame = cam.read()
        if not ret or frame is None:
            print("[WARN] Frame alınamadı. Bağlantı kopmuş olabilir.")
            break

        # 5) YOLO ile kasa + vana tespiti
        crates, valves = detect_crates_and_valves(model, frame)

        # 6) Sonucu çiz
        draw_detections(frame, crates, valves)

        # 7) Ekranda göster (ekrana sığdırarak)
        show_resizable(window_name, frame)

        key = cv2.waitKey(1) & 0xFF
        if key in (27, ord("q"), ord("Q")):
            print("[INFO] Kullanıcı çıkışı, program sonlandırılıyor...")
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
