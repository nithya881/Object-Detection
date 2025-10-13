import cv2
import numpy as np
import time

picked_hsv = None
color_picked = False

def pick_color(event, x, y, flags, param):
    global picked_hsv, color_picked
    if event == cv2.EVENT_LBUTTONDOWN:
        frame = param
        h, w = frame.shape[:2]
        size = 7
        x1, y1 = max(x - size, 0), max(y - size, 0)
        x2, y2 = min(x + size, w - 1), min(y + size, h - 1)
        region = frame[y1:y2, x1:x2]
        hsv = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
        avg_hsv = np.median(hsv.reshape(-1, 3), axis=0).astype(int)
        picked_hsv = avg_hsv
        color_picked = True
        print(f"Picked HSV (avg): {picked_hsv}")

cap = cv2.VideoCapture(0)
cv2.namedWindow("Color Tracker")

last_contour = None
last_time = 0
MEMORY = 0.5
frame_count = 0
total_time = 0  # total time for average calc

while True:
    frame_start = time.time()  # start timing here

    ret, frame = cap.read()
    if not ret:
        break
    display = frame.copy()
    cv2.setMouseCallback("Color Tracker", pick_color, param=frame)
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)

    if not color_picked:
        cv2.imshow("Color Tracker", display)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = picked_hsv

    delta_h, delta_s, delta_v = 10, 80, 80

    # Clip S and V ranges
    min_s, max_s = np.clip([s - delta_s, s + delta_s], 0, 255)
    min_v, max_v = np.clip([v - delta_v, v + delta_v], 0, 255)

    # Handle modular hue wrap-around
    h_low = (h - delta_h) % 180
    h_high = (h + delta_h) % 180

    # Define HSV ranges
    if h_low <= h_high:
        lower1 = np.array([h_low, min_s, min_v])
        upper1 = np.array([h_high, max_s, max_v])
        lower2 = upper2 = None
    else:
        lower1 = np.array([0, min_s, min_v])
        upper1 = np.array([h_high, max_s, max_v])
        lower2 = np.array([h_low, min_s, min_v])
        upper2 = np.array([179, max_s, max_v])

    # Create masks
    mask1 = cv2.inRange(hsv_frame, lower1, upper1)
    mask = mask1
    if lower2 is not None:
        mask2 = cv2.inRange(hsv_frame, lower2, upper2)
        mask = cv2.bitwise_or(mask1, mask2)

    # Clean up the mask
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Detect contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    big_contours = [c for c in contours if cv2.contourArea(c) > 1000]

    if big_contours:
        last_contour = max(big_contours, key=cv2.contourArea)
        last_time = time.time()

    if last_contour is not None and time.time() - last_time < MEMORY:
        cv2.drawContours(display, [last_contour], -1, (0, 255, 0), 3)
        M = cv2.moments(last_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            cv2.putText(display, "Tracked Object", (cx - 50, cy - 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    else:
        last_contour = None
        cv2.putText(display, "Object not visible", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # End timing for this frame
    dt_ms = (time.time() - frame_start) * 1000
    fps = 1000 / dt_ms if dt_ms > 0 else 0
    frame_count += 1
    total_time += (time.time() - frame_start)

    # Show detection time & FPS on video
    cv2.rectangle(display, (5, 5), (340, 35), (0, 0, 0), -1)
    cv2.putText(display, f"Detection: {dt_ms:.2f} ms | FPS: {fps:.1f}",
                (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow("Color Tracker", display)
    cv2.imshow("mask preview", mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Show average detection time & FPS
if frame_count > 0:
    avg_time_per_frame_ms = (total_time / frame_count) * 1000
    avg_fps = frame_count / total_time
    print(f"\nAverage detection time per frame: {avg_time_per_frame_ms:.2f} ms")
    print(f"Average FPS: {avg_fps:.2f}")
else:
    print("\nNo frames processed.")

