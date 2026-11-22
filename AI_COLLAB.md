# AI Collaboration

I built this project with Claude (Anthropic) as a pair programmer. My full chat history is in `chat_history/`, starting from my very first prompt (the assignment email). Below are the key decisions, what the AI suggested, what I decided, why, and the evidence.

## Key decisions

### Decision 1: Read the real brief before building
AI suggested: My first upload was my resume, not the brief. The AI said it could not tell what to build and asked for the Task A PDF instead of guessing.
I decided: To upload the Task A brief and build only from it.
Why: The brief says no clarifying questions are allowed, so the requirements (offline, folder of 50 named photos, group photo, "unknown" label, good UI, four required docs) had to come from my own careful reading.
Evidence: Chat excerpt #1.

### Decision 2: Face recognition stack
AI suggested: OpenCV YuNet (face detection) with SFace (face recognition), both small ONNX models. It compared them with dlib/face_recognition, InsightFace and DeepFace, and rejected those for heavier setup or downloading weights at runtime.
I decided: To use YuNet + SFace.
Why: The demo runs on a new laptop with no internet, so a one-command `pip install`, ~40 MB of models and CPU-only speed matter more than the last bit of accuracy. I did not benchmark the other libraries myself; I relied on the AI's comparison (recorded in RESEARCH.md) and checked that my chosen stack installs and runs.
Evidence: `RESEARCH.md`, `README.md`, chat excerpt #1 and the earlier model discussion in `chat_history/`.

### Decision 3: Ship the models inside the repo
AI suggested: A one-time `download_models.py`, because its sandbox could not download the models, and committing `models/` so nothing is fetched at demo time.
I decided: To run the download once on my laptop and commit `models/yunet.onnx` and `models/sface.onnx`.
Why: The brief says no internet at runtime, so the reviewers' machine must not need to download anything.
Evidence: `download_models.py`, `models/` in the repo, my `git status` and push output in `chat_history/`.

### Decision 4: Where to set the "Unknown" threshold
AI suggested: Start from the library's recommended cosine threshold of 0.363. After my first test, the AI noticed that two people from the folder scored 32% and 31% (just under the cutoff) while the three real strangers scored 25% or lower, and suggested 0.30.
I decided: To set `MATCH_THRESHOLD = 0.30` in `app.py` and re-run the test.
Why: The change fixed the two misses on my test set without naming any stranger. I know a lower threshold raises the risk of naming strangers, so I also tested on a real group photo.
Evidence: First run named 5 of 7 people (screenshot `docs/lfw_before.png`), after the change 7 of 7 with 3 Unknown (`docs/lfw_after.png`), chat excerpt #2.

### Decision 5: One person can match only one face
AI suggested: Assign the best-scoring face and person pairs first, so one person cannot be named on two faces in the same photo.
I decided: To keep this rule.
Why: The demo group photo contains people who are not in the folder, and this reduces wrong names for lookalikes.
Evidence: The identify route in `app.py`.

### Decision 6: Practice data
AI suggested: Because the brief provides no data, build a test set from the public LFW dataset with `make_test_data.py`: 7 people in the folder and 10 faces in a group collage, so 3 should come out Unknown.
I decided: To use it for the first test, keep the script and sample data in the repo, and then test again with real photos.
Why: LFW gives a repeatable check, but it is only a grid of headshots. Real group photos have different face sizes, angles and lighting. When the AI told me this, I ran the real-photo test, and all faces were found and named correctly.
Evidence: `make_test_data.py`, `people/`, `group.jpg`, `docs/real_test.png`, chat excerpt #3.

### Decision 7: Keep personal photos out of the public repo
AI suggested: Add my personal test folder (`my_people/`) to `.gitignore`, and blur faces or avoid publishing screenshots of people who have not agreed.
I decided: To follow this.
Why: The repo is public and I should not publish other people's photos without their permission.
Evidence: `.gitignore`.

### Decision 8: Simple two-step UI
AI suggested: One screen with two big buttons (1. choose the people folder, 2. upload the group photo), coloured boxes with names on the photo, a list beside it, and no external libraries or CDNs so it works offline.
I decided: To keep this design.
Why: The brief says the users are office staff and the UI is part of the score. Green means a recognised person and red means Unknown, which is readable at a glance.
Evidence: `static/index.html`.

## Chat excerpts (from my real chat)

### Excerpt #1: the wrong file
> me: (uploaded my resume and the email screenshot)
> AI: The PDF you uploaded is a resume, not the assignment brief... Since they won't answer clarifying questions, I'd rather work from the actual brief than guess at the requirements.
> me: (uploaded Task-A-Face-Recognition.pdf) this has to be completed

### Excerpt #2: tuning the threshold from my own result
> me: (screenshot of the app: 5 people named, 5 Unknown)
> AI: It works... Two of the "Unknown" scores are 32% and 31%, just under the cutoff of 36.3%... The three real strangers score 25%, 25% and 20%... lower the threshold slightly... 0.30.
> me: now fine it is working...should i delete the people folder and the make test file..?

### Excerpt #3: questioning whether to test properly
> me: shd i compulsorily do step 7 and8..
> AI: Steps 7 and 8 aren't required to submit, but I'd strongly advise doing at least a small version of them... The app has never run on real photos... You need results for your docs.
> me: yes crctly found

### Excerpt #4: making sure I understood it
> me: what is YuNet and SFace
> AI: They are the two small AI models your app uses. YuNet is the face detector... SFace is the face recognizer... it turns one cropped, aligned face into 128 numbers called an embedding.

## What I did myself
I ran every step on my own laptop: set up the virtual environment, fixed a nested-folder path problem, installed the missing Pillow package, downloaded the models, created the test data, ran the app, created the GitHub repo and pushed the code. I tested it on LFW and on a real group photo, and I asked the AI to explain the models so I can explain them in the interview.

## Limits I found
- The first test with the library's default threshold missed 2 of 7 people, so I tuned it. The right value depends on the data, so the live demo may need a small adjustment.
- Small, blurry or side-on faces are harder for both models, and low-quality photos give lower match scores.
- A lower threshold finds more real people but risks naming a stranger; a higher one does the opposite.
- My real-photo test used one group photo, so it shows the app works but does not prove accuracy in general.
