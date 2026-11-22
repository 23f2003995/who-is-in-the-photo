import os, numpy as np, cv2
from sklearn.datasets import fetch_lfw_people

d = fetch_lfw_people(min_faces_per_person=5, color=True, resize=1.0)
imgs = d.images * 255 if d.images.max() <= 1.0 else d.images
imgs = imgs.astype(np.uint8)[..., ::-1]  # RGB -> BGR for OpenCV
names = d.target_names

os.makedirs("people", exist_ok=True)
group = []
for p in range(10):
    idx = np.where(d.target == p)[0]
    if p < 7:  # first 7 go in the folder, so the last 3 will be "unknown"
        cv2.imwrite(f"people/{names[p]}.jpg", imgs[idx[0]])
    group.append(imgs[idx[1]])  # a DIFFERENT photo of the same person

rows = [np.hstack(group[:5]), np.hstack(group[5:])]
cv2.imwrite("group.jpg", np.vstack(rows))
print("Folder: people/ (7 people). Group photo: group.jpg (10 people, 3 not in folder)")