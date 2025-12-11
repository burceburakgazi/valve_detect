import cv2
import os
from pathlib import Path
from datetime import datetime

# ================== BURAYI DÜZENLE ==================
RTSP_URL = "rtsp://admin:dkk2025..@172.16.42.57:554/Streaming/Channels/101"
CAMERA_NAME = "cam1"   # hangi kamera olduğu (dosya adında gözükecek)
OUTPUT_DIR = Path(r"C:\proje\valve_detect\dataset\valve_crate\images\train")
# ====================================================


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] Çıktı klasörü: {OUTPUT_DIR}")
    print(f"[INFO] Kameraya bağlanılıyor: {RTSP_URL}")

    cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)
    if not cap.isOpened():
        print("[ERROR] Kamera açılamadı.")
        return

    cv2.namedWindow("Capture", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Capture", 1280, 720)

    counter = 0

    print("[INFO] Space: frame kaydet | q: çıkış")

    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            print("[WARN] Frame alınamadı, çıkılıyor.")
            break

        cv2.imshow("Capture", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            print("[INFO] Çıkış yapıldı.")
            break
        elif key == 32:  # SPACE
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = f"{CAMERA_NAME}_{timestamp}.jpg"
            filepath = OUTPUT_DIR / filename
            cv2.imwrite(str(filepath), frame)
            counter += 1
            print(f"[INFO] Kaydedildi: {filepath} (toplam {counter})")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
