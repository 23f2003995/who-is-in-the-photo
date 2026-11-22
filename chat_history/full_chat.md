PDF

I'll build this as a small offline Flask app on OpenCV's YuNet detector and SFace recognizer. Both are tiny ONNX models, so setup is a plain pip install. First I'm checking that the models can be fetched here.

The model download is blocked in my sandbox (the files sit behind Git LFS). I'll ship a one-time download_models.py for your laptop instead. Writing the app now.

I've built the project as a working app plus the four required docs. I couldn't test it end to end: my sandbox can't download the face models, so the code only compiles and has never run on real photos. Run it on your laptop and check it before relying on it.

What it does: you open a folder of named photos, upload a group photo, and each face gets a box and a name. Faces with no match are marked "Unknown", and the results also appear as a list. It runs fully offline and uses OpenCV's YuNet (face detection) and SFace (face recognition) models.

Do these next:

Unzip who-is-in-the-photo.zip, then follow the README: install the requirements and run python download_models.py once while online. Commit the models/ folder so the demo needs no internet.
Test with 50 faces and a real group photo that includes some people not in the folder. Adjust MATCH_THRESHOLD in app.py if known people show as Unknown or strangers get named.
AI_COLLAB.md: fill in the TODO parts in your own words and paste real excerpts from this chat. Export this chat into chat_history/. I left your decisions and evidence blank on purpose, because the graders want your reasoning and I shouldn't invent it.
ARCHITECTURE.md: have your AI agent install Archify as the brief says and diagram the project, then save the image as docs/architecture.png. The Mermaid sketch in the file is only a placeholder.
RESEARCH.md: the comparison table is my own summary, not something I verified or benchmarked. Check the links and add your test numbers.
Push to a public GitHub repo, and commit regularly before Tuesday, since the graders look at your history over the week. Send them the repo link and say you chose Task A before 11:59 PM IST on 24 Nov.

If it misbehaves on your photos, tell me what you see and I'll fix it. I can also add an optional upgrade to the stronger InsightFace models.

Who is in the photo
ZIP

give me step by step..firstly i have unzipped

Good. Here are the steps from where you are, written for Windows. Do them in order and tell me if any step shows an error.

Step 1: Open a terminal in the project folder

Open the unzipped who-is-in-the-photo folder in File Explorer. You should see app.py inside it.
Click the address bar at the top, type cmd and press Enter. A black terminal window opens in that folder.

Step 2: Check Python is installed

python --version

You should see Python 3.9 or newer. If you get an error, install Python from python.org and tick "Add Python to PATH" during setup.

Step 3: Create a virtual environment

python -m venv .venv
.venv\Scripts\activate

You should now see (.venv) at the start of the line.

Step 4: Install the requirements

pip install -r requirements.txt

Step 5: Download the face models (internet needed, once only)

python download_models.py

It should print two "downloading" lines and then "Done". Afterwards models/ should contain yunet.onnx and sface.onnx. The second file is about 37 MB.

Step 6: Run the app

python app.py

Open http://127.0.0.1:5000 in your browser.

Step 7: Get test data

Make a folder called people with about 5 to 10 photos for a quick test. Name each file after the person, for example Priya Sharma.jpg. Each photo should show one clear, front-facing face.
Find a group photo that includes some of those people and some who aren't in the folder. Include at least one person who isn't in the folder, so you can check the "Unknown" label.

Step 8: Try it

Click Open folder of people and choose your people folder. Your browser may ask you to confirm the upload, which is fine because nothing leaves your computer.
Click Upload group photo and choose the group photo.

Tell me what you get after Step 5 or Step 8, whether it works or shows an error, and I'll take you through the next part: GitHub, the docs and the submission.

shd i compulsorily do step 7 and8..

Steps 7 and 8 aren't required to submit, but I'd strongly advise doing at least a small version of them.

Why they matter

The app has never run on real photos. I couldn't test it, so you'd be submitting code nobody has seen work. A single bug could ruin the live demo, which is a big part of the score.
You need results for your docs. RESEARCH.md and AI_COLLAB.md ask for evidence, such as test results and your tuned threshold. You can't write those honestly without running it.
The demo is on unseen data. If you've tried it once on your own photos, you'll know how to handle problems when they ask about them.

Quickest version (about 10 minutes)

Put 5 photos of clear, front-facing faces in a folder, each named after the person (for example Ravi Kumar.jpg). Photos of friends or family, or public photos of well-known people, are fine.
Upload one group photo that has 2 or 3 of those people plus at least one stranger.
Check that the right people are named and the stranger shows "Unknown".

If that works, you can skip a full 50-person test for now and do it later when you have time. Steps 1 to 6 are the ones you can't skip, because they make the app run at all.

Where are you now: have you finished Step 5 and the models downloaded?

can u give the photos?

I can't give you photo files myself, because I can't generate or download images here. You can build a test set from the public LFW face dataset, which is one of the sources I listed in RESEARCH.md. This script downloads it and builds both the people folder and a group photo.

Step 1: Install one extra package (venv active, in the project folder)

pip install scikit-learn

Step 2: Create a file called make_test_data.py in the project folder and paste this in:

python
import os, numpy as np, cv2
from sklearn.datasets import fetch_lfw_people

d = fetch_lfw_people(min_faces_per_person=5, color=True, resize=1.0)
imgs = d.images \* 255 if d.images.max() <= 1.0 else d.images
imgs = imgs.astype(np.uint8)[..., ::-1] # RGB -> BGR for OpenCV
names = d.target_names

os.makedirs("people", exist_ok=True)
group = []
for p in range(10):
idx = np.where(d.target == p)[0]
if p < 7: # first 7 go in the folder, so the last 3 will be "unknown"
cv2.imwrite(f"people/{names[p]}.jpg", imgs[idx[0]])
group.append(imgs[idx[1]]) # a DIFFERENT photo of the same person

rows = [np.hstack(group[:5]), np.hstack(group[5:])]
cv2.imwrite("group.jpg", np.vstack(rows))
print("Folder: people/ (7 people). Group photo: group.jpg (10 people, 3 not in folder)")

Step 3: Run it

python make_test_data.py

The first run downloads the dataset, so it can take a few minutes. It creates a people folder with 7 named photos and a group.jpg with 10 faces.

Step 4: Test in the app

Run python app.py and open http://127.0.0.1:5000.
Click Open folder of people and choose the people folder.
Click Upload group photo and choose group.jpg.
Expected result: 7 faces named correctly and 3 marked Unknown.

group.jpg is a collage, not a real group photo. It's good for checking that the pipeline works, but the real demo uses a normal photo with people at different sizes and angles. After this works, test once with a real photo, such as a phone photo of friends, or ask me if you want to try other options.

Don't commit people/ and group.jpg unless you want them as sample data. If you do keep them, mention them in the README.

how to create that py file

There are two easy ways. Pick whichever you prefer.

Option A: Notepad (no extra software)

Open the who-is-in-the-photo folder in File Explorer.
Right-click an empty space, choose New, then Text Document.
Open it and paste the whole code from my previous message.
Click File, then Save As.
At the bottom, set Save as type to All Files. This is the important part, otherwise it saves as .txt.
Name it make_test_data.py, make sure you're saving inside the project folder, and click Save.
Delete the original "New Text Document.txt" if it's still there.

Option B: VS Code (if you have it installed)

In the terminal (with the project folder open), type code . and press Enter. Or open VS Code, choose File, then Open Folder, and pick the project folder.
In the left panel, click the New File icon and type make_test_data.py.
Paste the code and press Ctrl+S.

Check it worked

In your terminal, type:

dir make_test_data.py

If the file is listed, you're ready to run python make_test_data.py. If you see "File Not Found", the file may have been saved as make_test_data.py.txt. In that case, in File Explorer click View, then Show, then tick File name extensions, and rename it by removing the .txt.

Tell me what happens when you run it.

(.venv) PS C:\Users\Vasundhara Rajesh\Downloads\who-is-in-the-photo> python make_test_data.py
Traceback (most recent call last):
File "C:\Users\Vasundhara Rajesh\Downloads\who-is-in-the-photo\who-is-in-the-photo\.venv\Lib\site-packages\sklearn\datasets_lfw.py", line 136, in \_load_imgs
from PIL import Image
ModuleNotFoundError: No module named 'PIL'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
File "C:\Users\Vasundhara Rajesh\Downloads\who-is-in-the-photo\make*test_data.py", line 4, in <module>
d = fetch_lfw_people(min_faces_per_person=5, color=True, resize=1.0)
File "C:\Users\Vasundhara Rajesh\Downloads\who-is-in-the-photo\who-is-in-the-photo\.venv\Lib\site-packages\sklearn\utils_param_validation.py", line 218, in wrapper
return func(\*args, \*\*kwargs)
File "C:\Users\Vasundhara Rajesh\Downloads\who-is-in-the-photo\who-is-in-the-photo\.venv\Lib\site-packages\sklearn\datasets_lfw.py", line 406, in fetch_lfw_people
faces, target, target_names = load_func(
~~~~~~~~~^
data_folder_path,
^^^^^^^^^^^^^^^^^
...<3 lines>...
slice*=slice*,
^^^^^^^^^^^^^^
)
^
File "C:\Users\Vasundhara Rajesh\Downloads\who-is-in-the-photo\who-is-in-the-photo\.venv\Lib\site-packages\joblib\memory.py", line 616, in **call**
return self.\_cached_call(args, kwargs, shelving=False)[0]
~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\Vasundhara Rajesh\Downloads\who-is-in-the-photo\who-is-in-the-photo\.venv\Lib\site-packages\joblib\memory.py", line 571, in \_cached_call
return self.\_call(call_id, args, kwargs, shelving)
~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\Vasundhara Rajesh\Downloads\who-is-in-the-photo\who-is-in-the-photo\.venv\Lib\site-packages\joblib\memory.py", line 841, in \_call
output = self.func(\*args, \*\*kwargs)
File "C:\Users\Vasundhara Rajesh\Downloads\who-is-in-the-photo\who-is-in-the-photo\.venv\Lib\site-packages\sklearn\datasets_lfw.py", line 238, in \_fetch_lfw_people
faces = \_load_imgs(file_paths, slice*, color, resize)
File "C:\Users\Vasundhara Rajesh\Downloads\who-is-in-the-photo\who-is-in-the-photo\.venv\Lib\site-packages\sklearn\datasets_lfw.py", line 138, in \_load_imgs
raise ImportError(
...<4 lines>...
)
ImportError: The Python Imaging Library (PIL) is required to load data from jpeg files. Please refer to https://pillow.readthedocs.io/en/stable/installation.html for installing PIL.

This is a missing package, not a problem with your code. scikit-learn needs Pillow to read the JPEG files, so install it:

pip install pillow

Then run the script again:

python make_test_data.py

The dataset was probably already downloaded before the error, so the second run should be quicker.

One thing to check: your path shows who-is-in-the-photo\who-is-in-the-photo\.venv, so the folder is nested twice from unzipping. Your terminal is in the outer folder, and app.py is probably in the inner one. Check with:

dir
If you see app.py in the list, you're in the right place and nothing needs to change.
If you only see another who-is-in-the-photo folder, run cd who-is-in-the-photo and use that inner folder for everything. That includes python app.py, the people folder and group.jpg. When you create the GitHub repo later, it should be this inner folder, the one containing app.py and README.md.

Tell me what the script prints.

(.venv) PS C:\Users\Vasundhara Rajesh\Downloads\who-is-in-the-photo> python make_test_data.py
Folder: people/ (7 people). Group photo: group.jpg (10 people, 3 not in folder)
(.venv) PS C:\Users\Vasundhara Rajesh\Downloads\who-is-in-the-photo>

The test data is ready: a people folder with 7 named photos and a group.jpg with 10 faces. Next, check the face models.

Step 1: Check the models exist

dir models

You should see yunet.onnx and sface.onnx, with sface.onnx around 37 MB.

If the folder is empty or missing them, run python download_models.py (needs internet) and check again.
If that download fails, copy the error here.

Step 2: Start the app

python app.py

It should print Open http://127.0.0.1:5000. Leave this terminal open while you use the app.

Step 3: Test in your browser

Go to http://127.0.0.1:5000.
Click Open folder of people, choose the people folder, and confirm if the browser asks. You should see "✅ 7 people ready".
Click Upload group photo and choose group.jpg.

Expected result: 10 boxes, with 7 named people and 3 marked Unknown in red. The list on the right should show the same.

This collage test is a rough check, so a few misses are possible. Tell me what you see. Say how many faces were found, how many were named correctly, and whether any errors appeared in the terminal or the browser. If something is wrong, I'll fix it before we move on to GitHub and the docs.

.venv) PS C:\Users\Vasundhara Rajesh\Downloads\who-is-in-the-photo> dir models
dir : Cannot find path 'C:\Users\Vasundhara Rajesh\Downloads\who-is-in-the-photo\models' because it does not exist.
At line:1 char:1

- dir models
- ```
    + CategoryInfo          : ObjectNotFound: (C:\Users\Vasund...he-photo\models:String) [Get-ChildItem], ItemNotFou
   ndException
    + FullyQualifiedErrorId : PathNotFound,Microsoft.PowerShell.Commands.GetChildItemCommand
  ```

The models folder isn't in this folder, which fits the nested-folder issue I mentioned. Your earlier error shows the virtual environment inside a second who-is-in-the-photo folder, so the real project is probably one level down.

Step 1: See what's here

dir

Step 2: Go into the inner folder

If the list shows a folder named who-is-in-the-photo and no app.py, run:

cd who-is-in-the-photo
dir

You should now see app.py, README.md, requirements.txt, download_models.py and a models folder.

Step 3: Move your test data into this inner folder

people and group.jpg were created in the outer folder, so move them in:

move ..\people .
move ..\group.jpg .
move ..\make_test_data.py .

Skip any of these that say the file isn't found.

Step 4: Download the models (internet needed once)

The models folder starts empty, so fill it:

python download_models.py

Then check:

dir models

You should see yunet.onnx and sface.onnx, with sface.onnx around 37 MB.

The virtual environment may not stay active after changing folders. If python complains about missing modules, run ..\.venv\Scripts\activate or .venv\Scripts\activate, whichever path exists.

Paste what dir shows after Step 2 and what Step 4 prints, and I'll take it from there.

Mode LastWriteTime Length Name

---

d----- 22-11-2026 17:17 people  
d----- 22-11-2026 16:18 who-is-in-the-photo  
-a---- 22-11-2026 17:17 43410 group.jpg  
-a---- 22-11-2026 16:20 806 make_test_data.py  
for dir

This confirms it: the real project is the inner who-is-in-the-photo folder. Your test files (people, group.jpg, make_test_data.py) are in the outer one.

Step 1: Move the test files into the inner folder

move people who-is-in-the-photo\
move group.jpg who-is-in-the-photo\
move make_test_data.py who-is-in-the-photo\

Step 2: Go into the inner folder

cd who-is-in-the-photo
dir

You should see app.py, README.md, requirements.txt, download_models.py, static, people and group.jpg. If you also see models, it's currently empty.

Step 3: Download the models (internet needed once)

python download_models.py

It should print two "downloading" lines with sizes, then "Done".

Step 4: Check the models

dir models

You should see yunet.onnx (small) and sface.onnx (about 37 MB).

If Step 3 gives a "module not found" error, the virtual environment isn't active in this folder. Run ..\.venv\Scripts\activate and try again. The .venv lives in the outer folder, so it's best to keep using it from there.

Paste what Steps 3 and 4 show and we'll go on to start the app.

yes done till here

Next, start the app and run the test.

Step 1: Start the app (in the inner folder, with (.venv) showing)

python app.py

It should print Open http://127.0.0.1:5000. Leave this terminal open.

Step 2: Open the app
Go to http://127.0.0.1:5000 in your browser.

Step 3: Load the people

Click Open folder of people and choose the people folder inside the project.
If the browser asks you to confirm the upload, allow it. Nothing leaves your computer.
Wait for "✅ 7 people ready".

Step 4: Identify the group photo

Click Upload group photo and choose group.jpg.
Expected result: 10 boxes, with 7 named people and 3 marked Unknown in red, plus the same list on the right.

Step 5: Tell me the result
Send me:

how many faces were found,
how many were named correctly,
any error shown in the browser or in the terminal.

If it errors or the numbers are off, I'll fix it before we go on to GitHub and the docs.

It works. The app found all 10 faces, and the 5 names it gave look right. It named 5 people, though, and the test expected 7, so it's missing 2.

Why
Two of the "Unknown" scores are 32% and 31%, just under the cutoff of 36.3% (the MATCH_THRESHOLD setting). The three real strangers score 25%, 25% and 20%. I'm inferring that the 32% and 31% faces are your two missed people, since I can't see which is which. These LFW photos are small and low quality, and the folder photo and group photo of the same person differ, so the scores run lower than usual.

Fix: lower the threshold slightly

Open app.py in Notepad or VS Code.
Find MATCH_THRESHOLD = 0.363 and change it to MATCH_THRESHOLD = 0.30.
Save the file.
In the terminal, press Ctrl+C, then run python app.py again.
Refresh the browser, load the people folder again, and upload group.jpg.

You should now see 7 named people and 3 Unknown. The gap between your lowest correct match (about 31%) and highest stranger (25%) makes 0.30 a reasonable value here.

Two cautions

Don't treat 0.30 as final. A lower threshold raises the risk of naming a stranger as someone in the folder, which the live demo specifically tests. Test with a real group photo, such as a phone photo of friends, and keep whichever value works.
Your screenshot is real evidence for AI_COLLAB.md and RESEARCH.md. Save it in the docs/ folder and write down the scores above and what you changed.

Tell me the result after the change, and whether you have a real group photo to try next. After that we move on to GitHub and the docs.

now fine it is working...should i delete the people folder and the make test file..?

Weighing whether the repo needs cleanup.

You don't have to delete either one, and keeping them is better for the submission.

make_test_data.py: keep it

It shows how you created your test data, which supports the research and effort parts of the score.
It needs two extra packages, so add a line to README.md such as: "To regenerate sample data: pip install scikit-learn pillow, then python make_test_data.py".

people folder and group.jpg: keep them as sample data (recommended)

A reviewer can try the app right away.
The images are small, about 43 KB for group.jpg, so they won't bloat the repo.
They are public LFW photos, so mention LFW as the source in the README. This is allowed, since the brief says to use public data.
To keep things tidy, rename the folder with ren people sample_people, or create a sample_data folder and put both inside it.
If you'd rather keep the repo minimal, don't delete them. Add people/ and group.jpg to .gitignore so they stay on your laptop but aren't uploaded.

Do not delete or ignore these

models/: it must be committed so the demo works offline.
.venv: this is already in .gitignore, so it won't be uploaded.

Update before you commit

Change MATCH_THRESHOLD in the README tips to your new value (0.30).

Next is GitHub. Do you have a GitHub account and Git installed? If not, say so and I'll walk you through it. If you do, say which and I'll give you the commands to create the repo and push it.

ok next

Here's the GitHub step. First, two quick edits so the first commit is right.

Step 1: Update the README
Open README.md and make two changes:

In the Tips section, change the default threshold to 0.30.
Add a line: "Sample data: people/ and group.jpg are made from the public LFW dataset by make_test_data.py (needs pip install scikit-learn pillow)."

Also set MATCH_THRESHOLD = 0.30 in app.py if you haven't already, and save your screenshot into the docs/ folder.

Step 2: Check Git is installed

git --version

If you get an error, install Git from git-scm.com, accept the defaults, then close and reopen the terminal.

Step 3: Create the repo on GitHub

Sign in at github.com. Create an account if you don't have one.
Click + at the top right, then New repository.
Name it who-is-in-the-photo and choose Public.
Leave "Add a README", ".gitignore" and "license" unticked, since the project already has these files.
Click Create repository and copy the URL it shows, like https://github.com/YOURNAME/who-is-in-the-photo.git.

Step 4: Commit your project (terminal in the inner folder, the one with app.py)

git init
git config user.name "Your Name"
git config user.email "your-github-email@example.com"
git add .
git status

Look through the git status list. It should include models/onnx files, app.py and the docs, and it should not include .venv. If .venv appears, stop and tell me.

Then:

git commit -m "Initial version: offline face identification app"
git branch -M main

Step 5: Push to GitHub

git remote add origin https://github.com/YOURNAME/who-is-in-the-photo.git
git push -u origin main

Replace the URL with yours. A browser window may open asking you to sign in to GitHub, so do that. Then refresh the repo page, and your files should be there.

Step 6: Keep committing
The graders look at your history over the week, so make small commits as you finish each doc:

git add .
git commit -m "Describe what you changed"
git push

What's left before the deadline (Tue 24 Nov, 11:59 PM IST)

Fill in AI_COLLAB.md and export this chat into chat_history/.
Create the Archify diagram for ARCHITECTURE.md.
Fill in RESEARCH.md with your test results.
Test once with a real group photo.
Send your repo link and "Task A" to the placement team.

Tell me what git status shows, or any error from the push, and we'll sort it out.

is this enough..will i get selected..or do we have to improve anything

I can't tell you whether you'll be selected. I don't know the other candidates or how the graders score. What I can say is that what you have is a working baseline, not yet a strong submission. The brief lists what they judge, so here is where you stand on each point.

Judged on Where you are What to do
Live demo on unseen data Works on the LFW collage, but not yet tested on real group photos Highest priority: test with real photos (see below)
UI/UX Clean and functional Small polish, optional
System design Simple and sensible Needs the Archify diagram
Research Table is drafted but unverified Check links, add your test numbers
AI collaboration doc Template only Fill it in honestly with real excerpts
Effort (GitHub history) One commit so far Commit regularly through Monday and Tuesday

Improvements that matter most (in order)

Test with real photos. Take a phone photo of 8 to 10 friends or family, or use a real group photo. Put 40 to 50 single photos in a folder, with some of the group left out. The demo uses real photos, which are harder than LFW: faces are smaller, angles vary and lighting differs. Watch for two failures: people who are in the folder showing as Unknown, and strangers wrongly given a name. Wrong names are the worse one for a demo, so lean toward a slightly stricter threshold. Record what you try in RESEARCH.md.
Finish the four docs. They are required, and a missing or empty one will likely cost you.
Make the AI collaboration real. Use real moments from this chat, such as the nested-folder problem, the Pillow error, and tuning the threshold from 0.363 to 0.30 using your own screenshot. They want to see how you steered, not just that you used AI.
Optional upgrades if you have time:
Show a similarity score or confidence on each box (already in the list).
Let the user click a face to see its closest match.
Handle failure messages clearly, such as when a folder photo has no face.

Know your limits for the interview

Be ready to explain how it works, why you chose YuNet and SFace, what the threshold does, and what happens with small or side-on faces. They ask about your decisions, so don't submit anything you can't explain.
Face recognition on small faces can be weak, so say so openly rather than hiding it. Describing a failure case you found yourself is a strength.

Do you have a real group photo to test with? If you can share the results, I'll help you tune the threshold and decide whether an upgrade such as InsightFace is worth it.

Option 1: Share link (the easiest)

Open this chat in claude.ai or the Claude app.
Click the Share button (top right on desktop, or in the chat menu on mobile).
Create the share link and copy it.
Open chat_history/README.md in VS Code and replace its text with:

# Full AI chat history

Full conversation with Claude, from my first prompt:
https://claude.ai/share/PASTE-YOUR-LINK-HERE
Open the link in an incognito window to check that it loads without signing in.

Option 2: Copy and paste a backup file

Select the whole conversation, from the top to the bottom, and copy it.
In VS Code, create chat_history/full_chat.md and paste it in.
Save it.
