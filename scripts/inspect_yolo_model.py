from pathlib import Path
from ultralytics import YOLO

# Script konumundan proje kökünü bul
project_root = Path(__file__).resolve().parents[1]

# MODEL ADINI BURAYA DOĞRU YAZ !
model_path = project_root / "models" / "valve_crate.pt"

print(f"Model yolu: {model_path}")

# Modeli yüklemeyi dene
try:
    model = YOLO(str(model_path))
except Exception as e:
    print("MODEL YÜKLENEMEDİ! Hata:", e)
    exit()

# Model sınıf isimlerini yazdır
print("\nModel class isimleri (id: name):")
print(model.names)
