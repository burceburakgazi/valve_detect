from pathlib import Path

from ultralytics import YOLO


def load_valve_crate_model():
    """
    models/valve_crate.pt dosyasını yükler ve YOLO model nesnesini döndürür.
    """
    project_root = Path(__file__).resolve().parents[1]
    model_path = project_root / "models" / "valve_crate.pt"

    if not model_path.exists():
        raise FileNotFoundError(f"YOLO model dosyası bulunamadı: {model_path}")

    print(f"[INFO] YOLO modeli yükleniyor: {model_path}")
    model = YOLO(str(model_path))
    print("[INFO] YOLO modeli yüklendi.")
    return model
