"""One-time setup (needs internet ONCE). The app itself runs fully offline."""
import os, urllib.request
BASE = "https://github.com/opencv/opencv_zoo/raw/main/models/"
FILES = {
    "models/yunet.onnx": BASE + "face_detection_yunet/face_detection_yunet_2023mar.onnx",
    "models/sface.onnx": BASE + "face_recognition_sface/face_recognition_sface_2021dec.onnx",
}
os.makedirs("models", exist_ok=True)
for path, url in FILES.items():
    if os.path.exists(path) and os.path.getsize(path) > 100_000:
        print("ok", path); continue
    print("downloading", path); urllib.request.urlretrieve(url, path)
    print("  size", os.path.getsize(path))
print("Done. Commit models/ to git so the demo works with no internet.")
