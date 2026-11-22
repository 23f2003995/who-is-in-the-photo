# Who Is in the Photo? (Take-home Task A)

Offline web app: open a folder of 50 named photos, upload a group photo, see who is who. Unmatched faces are marked **Unknown**.

## Install (internet needed only for this step)
```bash
python -m venv .venv
.venv\Scripts\activate          # Windows   (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
python download_models.py       # skip if models/ is already in the repo
```
## Run (no internet needed)
```bash
python app.py
```
Open http://127.0.0.1:5000 then: **1.** click *Open folder of people* (files named `Priya Sharma.jpg`) → **2.** click *Upload group photo*.

## Tips
- Folder photos: one clear, front-facing face each (the largest face in the file is used).
- If a known person shows as Unknown, lower `MATCH_THRESHOLD` in `app.py` (default 0.363). If strangers get named, raise it.
- Models: YuNet (face detection) + SFace (face embeddings), both from OpenCV Zoo, run on CPU.
