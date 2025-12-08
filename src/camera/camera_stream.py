import cv2


class CameraStream:
    """
    Tek bir IP kameradan RTSP üzerinden frame okuyan basit sınıf.
    """

    def __init__(self, rtsp_url: str, name: str = "Camera"):
        self.rtsp_url = rtsp_url
        self.name = name
        self.cap = None

    def open(self) -> bool:
        """Kameraya bağlanmayı dener."""
        print(f"[INFO] {self.name}: Kameraya bağlanılıyor...")
        self.cap = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)

        if not self.cap.isOpened():
            print(f"[ERROR] {self.name}: Kamera açılamadı.")
            return False

        # Gecikmeyi azaltmak için buffer'ı küçült
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        print(f"[INFO] {self.name}: Bağlantı başarılı.")
        return True

    def read(self):
        """
        Tek frame okur.
        Dönüş: (ret, frame)
        """
        if self.cap is None:
            return False, None

        ret, frame = self.cap.read()
        return ret, frame

    def release(self):
        """Kaynağı serbest bırak."""
        if self.cap is not None:
            self.cap.release()
            self.cap = None
            print(f"[INFO] {self.name}: Kamera bağlantısı kapatıldı.")
