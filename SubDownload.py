import praw
import requests
import cv2
import numpy as np
import os
import pickle
import csv
from utils.create_token import create_token
from utils.square_fit import square_fit
from utils.get_audio import get_audio
from utils.init_files import create_database, create_folder
from utils.trie import trieNode, insert,find,serialize,deserialize
postlist = []

# Path to save images
dir_path = os.path.dirname(os.path.realpath(__file__))
image_path = os.path.join(dir_path, "images/")
video_path = os.path.join(dir_path, "videos/")
ignore_path = os.path.join(dir_path, "ignore_images/")
create_folder(image_path)
create_folder(video_path)
create_database(dir_path)

data = open("serialized_database.txt", "r").read()
root = deserialize(data)
# Get token file to log into reddit.
# You must enter your....
# client_id - client secret - user_agent - username password
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
else:
    creds = create_token()
    pickle_out = open("token.pickle","wb")
    pickle.dump(creds, pickle_out)

reddit = praw.Reddit(client_id=creds['client_id'],
                    client_secret=creds['client_secret'],
                    user_agent=creds['user_agent'],
                    username=creds['username'],
                    password=creds['password'])


f_final = open("sub_list.csv", "r")
img_notfound = cv2.imread('imageNF.png')

for line in f_final:
    sub = line.split(",")[0]
    limits = int(line.split(",")[1])
    subreddit = reddit.subreddit(sub)
    print(f"Starting {sub}!")
    count = 0
    for submission in subreddit.hot(limit=limits):
        if "png" in submission.url.lower() or "jpg" in submission.url.lower():
            try:
                unique_id = submission.id
                present = find(root,unique_id)
                if (present):
                    print(unique_id + " is already present!")
                else:

                    title = submission.title
                    title = title.encode("ascii", "ignore")
                    title = title.decode()

                    author = submission.author

                    resp = requests.get(submission.url.lower(), stream=True).raw
                    image = np.asarray(bytearray(resp.read()), dtype="uint8")
                    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

                    # Could do transforms on images like resize!
                    compare_image = cv2.resize(image, (224, 224))

                    # Get all images to ignore
                    for (dirpath, dirnames, filenames) in os.walk(ignore_path):
                        ignore_paths = [os.path.join(dirpath, file) for file in filenames]
                    ignore_flag = False

                    for ignore in ignore_paths:
                        ignore = cv2.imread(ignore)
                        difference = cv2.subtract(ignore, compare_image)
                        b, g, r = cv2.split(difference)
                        total_difference = cv2.countNonZero(b) + cv2.countNonZero(g) + cv2.countNonZero(r)
                        if total_difference == 0:
                            ignore_flag = True
                    if not ignore_flag:

                        cv2.imwrite(f"{image_path}{unique_id}.png", image)

                        image = cv2.imread(f"{image_path}{unique_id}.png")
                        resized_image = square_fit(image)
                        cv2.imwrite(f"{image_path}{unique_id}.png", resized_image)
                        postlist.append([unique_id,sub,author,title])
                        count += 1
                        insert(root, unique_id)
            except Exception as e:
                print(f"Image failed. {submission.url.lower()}")
                print(e)
"""
        if "v.redd.it" in submission.url.lower():
            try:
                unique_id = submission.id
                present = find(root,unique_id)
                if (present):
                    print(unique_id + " is already present!")
                else:
                    title = submission.title
                    title = title.encode("ascii", "ignore")
                    title = title.decode()
                    author = submission.author
                    video_url = submission.media["reddit_video"]["fallback_url"]
                    audio_url = get_audio(video_url)
                    file_name = "video.mp4"
                    r = requests.get(video_url, stream=True)
                    with open(file_name, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024 * 1024):
                            if chunk:
                                f.write(chunk)
                    file_name = "audio.mp4"
                    r = requests.get(audio_url, stream=True)
                    # download started
                    with open(file_name, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024 * 1024):
                            if chunk:
                                f.write(chunk)
                    cmd = "ffmpeg -i video.mp4 -i audio.mp4 -c:v copy -c:a aac "+video_path+"/"+unique_id+".mp4"
                    os.system(cmd)
                    os.remove("video.mp4")
                    os.remove("audio.mp4")
                    insert(root,unique_id)
                    postlist.append([unique_id, sub, author, title])
                    count += 1
            except Exception as e:
                print(f"Video failed. {submission.url.lower()}")
                print(e)
"""

with open('posted.csv', 'a+', newline='') as file:
    writer = csv.writer(file)
    for a,b,c,d in postlist:
        writer.writerow([a,b,c,d])

os.remove("serialized_database.txt")
f = open("serialized_database.txt",'a')
f.write(serialize(root))
f.close()