import cv2
from pathlib import Path


def extract_frames(video_path, output_dir, interval_seconds=0.5):
    video_path = Path(video_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        cap.release()
        raise RuntimeError("Invalid video FPS")
    interval_frames = max(1, round(fps * interval_seconds))

    frame_index = 0
    saved_count = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_index % interval_frames == 0:
                output_path = (output_dir / f"frame_{saved_count:04d}.jpg")
                if not cv2.imwrite(str(output_path), frame):
                    raise RuntimeError(f"Failed to save frame: {output_path}")
                saved_count += 1

            frame_index += 1

    finally:
        cap.release()

    print(f"Saved {saved_count} frames to {output_dir}")
    return saved_count




if __name__ == "__main__":
    extract_frames("../data/before.mp4","../output/before_frames")
    extract_frames("../data/after.mp4","../output/after_frames")
