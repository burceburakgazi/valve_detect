import random


def detect_crates_and_valves(model, frame):
    """
    YOLO modelini kullanarak frame'de kasa ve vana tespiti yapır.
    
    Args:
        model: Yüklü YOLO modeli (veya mock model)
        frame: OpenCV frame
        
    Returns:
        (crates, valves): Tespit edilen kasalar ve vanalar listesi
        Örnek format:
        [{"box": [x1, y1, x2, y2], "score": 0.95}, ...]
    """
    crates = []
    valves = []
    
    # YOLO tahminini yap
    results = model.predict(frame, conf=0.5, verbose=False)
    
    # Test modu: mock verileri oluştur
    if not results or len(results) == 0:
        # Demo amaçlı random tespit
        h, w = frame.shape[:2]
        
        # Rastgele 1-3 adet kasa tespit et
        num_crates = random.randint(1, 2)
        for _ in range(num_crates):
            x1 = random.randint(0, max(0, w - 200))
            y1 = random.randint(0, max(0, h - 200))
            crates.append({
                "box": [x1, y1, x1 + 150, y1 + 150],
                "score": random.uniform(0.7, 0.99)
            })
        
        # Rastgele 1-2 adet vana tespit et
        num_valves = random.randint(1, 2)
        for _ in range(num_valves):
            x1 = random.randint(0, max(0, w - 100))
            y1 = random.randint(0, max(0, h - 100))
            valves.append({
                "box": [x1, y1, x1 + 80, y1 + 80],
                "score": random.uniform(0.6, 0.95)
            })
    else:
        # Gerçek model sonuçları varsa işle
        result = results[0]
        
        if hasattr(result, 'boxes') and result.boxes is not None:
            for box in result.boxes:
                # Koordinatları al (x1, y1, x2, y2)
                coords = box.xyxy[0].cpu().numpy().astype(int)
                x1, y1, x2, y2 = coords
                
                # Güvenirlik skoru
                confidence = float(box.conf[0])
                
                # Sınıf ID'si
                class_id = int(box.cls[0])
                
                # Model çıktısında sınıfları ayırt et
                # Sınıf 0: kasa, Sınıf 1: vana
                if class_id == 0:
                    crates.append({
                        "box": [x1, y1, x2, y2],
                        "score": confidence
                    })
                elif class_id == 1:
                    valves.append({
                        "box": [x1, y1, x2, y2],
                        "score": confidence
                    })
    
    return crates, valves
