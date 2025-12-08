from pathlib import Path

import yaml
from dotenv import load_dotenv


def load_env():
    """
    Proje kökündeki .env dosyası varsa yükler.
    Şimdilik şart değil ama ileride kullanıcı/şifre vb. için kullanabiliriz.
    """
    project_root = Path(__file__).resolve().parents[1]
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path)


def load_camera_config():
    """
    config/cameras.yaml dosyasını okur ve kamera bilgilerini döndürür.

    Dönüş örneği:
    {
        "cam1": {"name": "Ana Paketleme", "rtsp": "rtsp://..."},
        ...
    }
    """
    project_root = Path(__file__).resolve().parents[1]
    config_path = project_root / "config" / "cameras.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"cameras.yaml bulunamadı: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    cameras = data.get("cameras", {})
    if not cameras:
        raise ValueError("cameras.yaml içinde 'cameras' alanı boş veya yok.")

    return cameras
