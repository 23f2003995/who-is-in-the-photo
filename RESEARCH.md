# Research

## The problem in one line

Match every face in a group photo (about 10 people) against a folder of 50 named photos, fully offline, and label anyone not in the folder as "unknown".
This is **1:N face identification with an open set**: the system must be able to say "none of these".

## Pipeline I settled on

1. **Detect** every face (box + 5 landmarks).
2. **Align and embed** each face into a vector (a numerical fingerprint).
3. **Compare** with cosine similarity against the 50 stored vectors.
4. **Decide**: best match above a threshold gets the name, otherwise "Unknown".

## Existing tools and projects compared

| Option                                                              | Link                                         | Offline?                         | Setup                                                                                              | Decision                                                                         |
| ------------------------------------------------------------------- | -------------------------------------------- | -------------------------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **OpenCV YuNet + SFace**                                            | https://github.com/opencv/opencv_zoo         | Yes (two ONNX files)             | Only `opencv-python`                                                                               | **Chosen**                                                                       |
| face_recognition (dlib)                                             | https://github.com/ageitgey/face_recognition | Yes                              | Needs dlib, which compiles from source and can be hard on Windows (from reports, not tested by me) | Rejected: setup risk on an unknown demo laptop                                   |
| InsightFace (ArcFace)                                               | https://github.com/deepinsight/insightface   | Yes, once weights are downloaded | onnxruntime plus larger models                                                                     | Not chosen: heavier. Likely more accurate, a possible upgrade (not tested by me) |
| DeepFace                                                            | https://github.com/serengil/deepface         | Only after weights are cached    | Wraps TensorFlow and several models                                                                | Rejected: heavy, and downloads weights on first use                              |
| AlchemyFace (existing wrapper around the same YuNet + SFace models) | https://pypi.org/project/alchemyface/        | Yes, if weights are pre-fetched  | Extra dependency                                                                                   | Not used: I wanted to write and understand the pipeline myself                   |
| Cloud APIs (Gemini, OpenAI, Rekognition)                            | n/a                                          | No                               | n/a                                                                                                | Not allowed by the brief                                                         |

## Why YuNet + SFace

- The OpenCV documentation says the two ONNX models are used through `cv::FaceDetectorYN` and `cv::FaceRecognizerSF`. The detector is about 338 KB, the recognizer about 36.9 MB. Source: https://docs.opencv.org/5.0/tutorials/dnn/dnn_face/dnn_face.html
- Both run on CPU, so no graphics card is needed.
- The same documentation gives a recommended **cosine threshold of 0.363**, which I used as my starting point.
- **YuNet** (detector): https://github.com/ShiqiYu/libfacedetection
- **SFace** (recognizer): paper https://arxiv.org/abs/2205.12010

## Data sources

- **LFW (Labeled Faces in the Wild)**: https://vis-www.cs.umass.edu/lfw/ . Public dataset, loaded through scikit-learn in `make_test_data.py`.
- **My own real photos** of people who agreed, kept out of the repo (`.gitignore`).
- The brief allows public data or self-made data. No AI image or cloud service is used inside the solution.

## What I tested

| Test                                                       | Threshold       | Result                                                 |
| ---------------------------------------------------------- | --------------- | ------------------------------------------------------ |
| LFW collage: 7 people in the folder, 10 faces, 3 strangers | 0.363 (default) | All 10 faces found, but only 5 of 7 known people named |
| Same test                                                  | 0.30            | 7 of 7 named, 3 Unknown                                |
| Real group photo                                           | 0.30            | Faces found and named correctly                        |

Screenshots: `docs/lfw_before.png`, `docs/lfw_after.png`, `docs/real_test.png`.

## What I learned

- LFW photos are small and low quality, so match scores come out lower than the documented defaults. In my test the correct matches scored about 31% to 76%, and strangers scored 25% or lower, which is why 0.30 separated them.
- The threshold is a trade-off. Lower finds more real people but risks naming strangers; higher does the opposite. The demo includes strangers, so wrong names are the bigger risk.
- To avoid one person being named on two faces, the app assigns the best-scoring pairs first and lets each person match only once.

## Limits and what I'd try next

- Small, blurry, side-on or partly hidden faces are harder for both models.
- My real-photo test used a single photo, so it shows the pipeline works but is not a measure of overall accuracy.
- Next steps: compare against InsightFace (ArcFace) on the same photos, and average several photos per person if the folder ever has more than one.
