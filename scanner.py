import cv2
import hashlib
import requests
import threading
import time

API_URL = "https://qr-dector4.onrender.com/api/QR/"

def send_qr_to_api(qr_text):
    qr_hash = hashlib.sha256(qr_text.encode()).hexdigest()
    data = {'qr_hash': qr_hash}
    try:
        response = requests.post(API_URL, json=data, timeout=5)
        print(f"Sent to API: {response.status_code} → {response.json()}")
    except Exception as e:
        print("Error sending to API:", e)


def scan_camera(source, name="Camera"):
    cap = cv2.VideoCapture(source)
    detector = cv2.QRCodeDetector()
    last_qr = None

    if not cap.isOpened():
        print(f"❌ Could not open {name} ({source})")
        return

    print(f"✅ {name} feed started...")

    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"⚠️ {name} frame not captured")
            break

        data, points, _ = detector.detectAndDecode(frame)
        if data:
            if data != last_qr:
                print(f"[{name}] Detected QR:", data)
                send_qr_to_api(data)
                last_qr = data

            if points is not None:
                points = points[0]
                for i in range(len(points)):
                    pt1 = tuple(map(int, points[i]))
                    pt2 = tuple(map(int, points[(i + 1) % len(points)]))
                    cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

        cv2.imshow(f"{name} (press 'q' to quit)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"🔴 {name} feed stopped.")


def main():
    # You can add multiple cameras here:
    cameras = [
        0,  # Default webcam
        # "http://192.168.0.101:8080/video",  # Example phone IP camera
        # "rtsp://user:pass@192.168.0.55:554/stream",  # Example RTSP feed
    ]

    threads = []
    for i, cam in enumerate(cameras):
        t = threading.Thread(target=scan_camera, args=(cam, f"Camera {i+1}"))
        t.start()
        threads.append(t)
        time.sleep(1)  # slight delay between camera starts

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
