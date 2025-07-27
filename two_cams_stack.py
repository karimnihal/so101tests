import argparse, time
import cv2
import numpy as np

def open_cam(idx, w, h, fps):
    cap = cv2.VideoCapture(idx, cv2.CAP_AVFOUNDATION)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  w)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
    cap.set(cv2.CAP_PROP_FPS,          fps)
    return cap

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=int, default=0, help="index of cam a (top) – mac webcam")
    ap.add_argument("--b", type=int, default=1, help="index of cam b (bottom) – wrist cam")
    ap.add_argument("--w", type=int, default=1280)
    ap.add_argument("--h", type=int, default=720)
    ap.add_argument("--fps", type=int, default=30)
    args = ap.parse_args()

    cap_a = open_cam(args.a, args.w, args.h, args.fps)
    cap_b = open_cam(args.b, args.w, args.h, args.fps)

    if not cap_a.isOpened() or not cap_b.isOpened():
        print("couldn't open one or both cameras. indices ok? permissions granted?")
        return

    last = time.time(); frames = 0; fps_est = 0.0
    while True:
        ok_a, fa = cap_a.read()
        ok_b, fb = cap_b.read()
        if not ok_a or not ok_b:
            print("read fail:", ok_a, ok_b)
            break

        frames += 1
        now = time.time()
        if now - last >= 1:
            fps_est = frames / (now - last)
            frames, last = 0, now

        cv2.putText(fa, f"cam {args.a} (top) ~{fps_est:.1f} fps",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        cv2.putText(fb, f"cam {args.b} (bottom) ~{fps_est:.1f} fps",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        combo = np.vstack([fa, fb])  # stacked in one window
        cv2.imshow("both cams (q to quit)", combo)

        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            break

    cap_a.release(); cap_b.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
