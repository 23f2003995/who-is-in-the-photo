"""Who Is in the Photo? Offline face identification. YuNet (detect) + SFace (embed)."""
import os, io
import cv2, numpy as np
from flask import Flask, jsonify, request, send_from_directory

HERE = os.path.dirname(os.path.abspath(__file__))
DET = os.path.join(HERE, "models", "yunet.onnx")
REC = os.path.join(HERE, "models", "sface.onnx")
MATCH_THRESHOLD = 0.30 # SFace cosine threshold recommended by OpenCV
MAX_SIDE = 1920           # downscale huge photos for speed

app = Flask(__name__, static_folder="static")
app.config["MAX_CONTENT_LENGTH"] = 512 * 1024 * 1024
GALLERY = {"names": [], "embs": None}

def _models():
    if not (os.path.exists(DET) and os.path.exists(REC)):
        raise RuntimeError("Models missing. Run: python download_models.py")
    detector = cv2.FaceDetectorYN.create(DET, "", (320, 320), 0.7, 0.3, 5000)
    recognizer = cv2.FaceRecognizerSF.create(REC, "")
    return detector, recognizer

def _decode(file_storage):
    data = np.frombuffer(file_storage.read(), np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)  # note: EXIF rotation is applied by imdecode
    if img is None:
        return None
    h, w = img.shape[:2]
    s = MAX_SIDE / max(h, w)
    return cv2.resize(img, None, fx=s, fy=s, interpolation=cv2.INTER_AREA) if s < 1 else img

def _faces(detector, img):
    h, w = img.shape[:2]
    detector.setInputSize((w, h))
    _, faces = detector.detect(img)
    return [] if faces is None else list(faces)

def _embed(recognizer, img, face):
    return recognizer.feature(recognizer.alignCrop(img, face)).flatten()

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/api/gallery", methods=["POST"])
def load_gallery():
    detector, recognizer = _models()
    names, embs, skipped = [], [], []
    for f in request.files.getlist("files"):
        stem = os.path.splitext(os.path.basename(f.filename))[0].strip()
        img = _decode(f)
        if img is None or not stem:
            continue  # not an image
        faces = _faces(detector, img)
        if not faces:
            skipped.append(stem); continue
        best = max(faces, key=lambda r: r[2] * r[3])  # largest face = the person
        names.append(stem); embs.append(_embed(recognizer, img, best))
    GALLERY["names"], GALLERY["embs"] = names, (np.array(embs) if embs else None)
    return jsonify(count=len(names), names=names, skipped=skipped)

@app.route("/api/identify", methods=["POST"])
def identify():
    if GALLERY["embs"] is None:
        return jsonify(error="Load the people folder first."), 400
    detector, recognizer = _models()
    img = _decode(request.files["photo"])
    if img is None:
        return jsonify(error="That file is not a readable image."), 400
    h, w = img.shape[:2]
    faces = _faces(detector, img)
    if not faces:
        return jsonify(width=w, height=h, results=[])
    q = np.array([_embed(recognizer, img, f) for f in faces])
    g = GALLERY["embs"]
    sims = (q / np.linalg.norm(q, axis=1, keepdims=True)) @ (g / np.linalg.norm(g, axis=1, keepdims=True)).T
    # one person can only appear once: assign best pairs first (greedy)
    assigned, used = {}, set()
    for fi, pi in sorted(np.ndindex(*sims.shape), key=lambda ij: -sims[ij]):
        if sims[fi, pi] < MATCH_THRESHOLD:
            break
        if fi in assigned or pi in used:
            continue
        assigned[fi] = pi; used.add(pi)
    results = []
    for i, f in enumerate(faces):
        x, y, bw, bh = [float(v) for v in f[:4]]
        known = i in assigned
        results.append(dict(
            name=GALLERY["names"][assigned[i]] if known else "Unknown",
            known=known,
            score=round(float(sims[i, assigned[i]] if known else sims[i].max()), 3),
            box=[x / w, y / h, bw / w, bh / h]))
    results.sort(key=lambda r: r["box"][0])  # left-to-right
    return jsonify(width=w, height=h, results=results)

if __name__ == "__main__":
    print("Open http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000)
