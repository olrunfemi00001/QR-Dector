import cv2
import hashlib
import requests

API_URL = "https://qr-dector1.onrender.com/api/QR/"

def send_qr_to_api(qr_text):
    qr_hash = hashlib.sha256(qr_text.encode()).hexdigest()
    data = {'qr_hash': qr_hash}
    try:
        response = requests.post(API_URL, json=data)
        print("Sent to API:", response.json())
    except Exception as e:
        print("Error sending to API:", e)

def main():
    cap = cv2.VideoCapture(0)  # 0 = webcam; or replace with IP camera URL
    detector = cv2.QRCodeDetector()
    last_qr = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        data, points, _ = detector.detectAndDecode(frame)
        if data:
            if data != last_qr:  # Avoid duplicates
                print("Detected QR:", data)
                send_qr_to_api(data)
                last_qr = data

            # Draw box around QR
            if points is not None:
                points = points[0]
                for i in range(len(points)):
                    pt1 = tuple(map(int, points[i]))
                    pt2 = tuple(map(int, points[(i + 1) % len(points)]))
                    cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

        cv2.imshow("QR Scanner (press 'q' to quit)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
