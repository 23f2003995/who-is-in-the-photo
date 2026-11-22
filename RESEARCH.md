# Research

## Options compared
| Option | Link | Offline? | Install effort | Verdict |
|---|---|---|---|---|
| OpenCV YuNet + SFace | https://github.com/opencv/opencv_zoo | Yes, ~40 MB models | `pip install opencv-python` only | **Chosen** |
| face_recognition (dlib) | https://github.com/ageitgey/face_recognition | Yes | Needs dlib/CMake compile, painful on Windows | Rejected: setup risk on an unknown demo laptop |
| InsightFace (ArcFace) | https://github.com/deepinsight/insightface | Yes once models are downloaded | onnxruntime + larger models; auto-downloads weights | Strong accuracy; rejected for size and download-at-runtime risk (TODO: test as upgrade) |
| DeepFace wrapper | https://github.com/serengil/deepface | Only after weights cached | Pulls TensorFlow, heavy | Rejected: heavy and downloads weights at first run |
| Cloud APIs (Gemini, Rekognition) | n/a | No | n/a | Forbidden by the brief |

## Papers / models
- SFace: https://arxiv.org/abs/2205.12010 (OpenCV's recommended cosine threshold 0.363)
- YuNet detector: https://github.com/ShiqiYu/libfacedetection

## Data for practice
- LFW: http://vis-www.cs.umass.edu/lfw/ (public face dataset)
- Own images generated with an image tool, only as practice data (allowed by the brief)

## TODO before submitting (fill in with your own results)
- Test with 50 folder photos + a real group photo; record accuracy and failure cases.
- Tune the threshold on your own test photos and note the numbers here.
