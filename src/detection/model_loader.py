from pathlib import Path


def load_valve_crate_model():
    """
    models/valve_crate.pt dosyasını yükler ve YOLO model nesnesini döndürür.
    Şuan test modu: model dosyası boş olduğundan mock model döndürülüyor.
    """
    project_root = Path(__file__).resolve().parents[1]
    model_path = project_root / "models" / "valve_crate.pt"

    print(f"[INFO] Model yükleme başladı: {model_path}")
    
    # Mock model döndür (demo/test modu)
    class MockModel:
        def predict(self, frame, conf=0.5, verbose=False):
            # Test amaçlı dummy sonuçlar
            return []
    
    print("[INFO] Test modu: Mock model yüklendi.")
    return MockModel()
