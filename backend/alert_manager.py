from datetime import datetime

ALERTS = []

def send_alert(name, camera_id, score):
    alert = {
        "name": name,
        "camera": camera_id,
        "confidence": round(float(score), 3),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    ALERTS.append(alert)

    print("\n[ALERT]")
