# AI Collaboration

> Fill every TODO in your own words. Use your real chat; do not invent excerpts. Put the full exported history in `chat_history/` starting from your first prompt.

## Decisions
### Decision 1: which face-recognition stack
AI suggested: OpenCV YuNet + SFace (ONNX), after noting dlib/InsightFace need heavier setup.
I decided: TODO (keep or change)
Why: TODO (e.g. must install on an unknown laptop, offline)
Evidence: chat excerpt #1

### Decision 2: how models are shipped
AI suggested: a one-time `download_models.py` (the AI sandbox could not fetch the files), then commit `models/` to the repo.
I decided: TODO
Why: TODO (demo has no internet)
Evidence: chat excerpt #2

### Decision 3: unknown people
AI suggested: cosine threshold 0.363 plus one-to-one assignment so one person cannot name two faces.
I decided: TODO (your tuned value, from your own tests)
Why: TODO
Evidence: TODO (your test results)

### Decisions 4-5 (TODO)
Examples: UI layout (two-step cards), using the largest face in each folder photo, image downscaling to 1920 px. Add anything where you pushed back on the AI.

## Chat excerpts
### Excerpt #1 (TODO: paste real text)
> me: ...
> AI: ...

### Excerpt #2 (TODO)
### Excerpt #3 (TODO)
