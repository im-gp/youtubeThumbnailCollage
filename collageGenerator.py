# documentation can be found here
# https://github.com/googleapis/google-api-python-client/blob/main/docs/start.md <--- YouTube Python Git
# https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.html <--- YouTube v3 Docs
# https://developers.google.com/youtube/v3/docs <--- YouTube Developper API Page
# https://www.youtube.com/watch?v=coZbOM6E47I <--- YouTube video used

import csv
import pandas as pd
import urllib.request
import os, os.path
import math
import shutil
import glob
from googleapiclient.discovery import build
from pathlib import Path
from PIL import Image

# ----- USER PARAMETERS -------
csvData = 'collage.csv'
FILE_PATH = 'images/'
keepImages = True
keepCSV = True
api_key = '' 
playlistID = 'PLHykAyQQdTart3T8wrDjEnAFEmbVstInA'

# ----- GLOBAL VARIABLES ------

youtube = build('youtube', 'v3', developerKey=api_key) 
vid_thumbnailURL = []
global_vid_ids = []
nextPageToken = None

# ----- FUNCTIONS -----

def csv_length(csv_file):
    '''
        Args:
            -- csv_file : file path of a .csv
    '''
    file = open(csv_file)
    reader = csv.reader(file)
    lines= len(list(reader))
    return lines - 1

def url_to_jpg(i, url, file_path):

    '''
        Args:
            -- i : number of image
            -- url : a URL address of a given image
            -- file_path : where to save the file
    '''

    filename = 'image{}'.format(i)
    full_path = '{}{}'.format(file_path, filename)
    download = urllib.request.urlretrieve(url, full_path)

    im = Image.open(full_path)
    imCrop = im.crop((0, 45, 480, 315))
    imCrop.save(full_path +'.jpg')
    os.remove(full_path)
    return None

# ----- CODE ------

# check if 'images/' exists and remove any images already inside
if os.path.exists(FILE_PATH):
    files = glob.glob(FILE_PATH+'*.jpg')
    for f in files:
        os.remove(f)
    print(f'cleared {FILE_PATH}')
    pass
else:
    Path(FILE_PATH).mkdir(parents=True, exist_ok=True)

# request a list of video IDs from YouTube API
while True:
    vid_ids = []

    pl_request = youtube.playlistItems().list(      
            part='contentDetails, snippet',
            playlistId=playlistID,
            maxResults=50,
            pageToken=nextPageToken
            )

    pl_response = pl_request.execute()

    for item in pl_response['items']:
        global_vid_ids.append(item['contentDetails']['videoId'])

        # https://developers.google.com/youtube/v3/docs/thumbnails <---- different sized thumbnails available
        vid_thumbnailURL.append(item['snippet']['thumbnails']['high']['url'])

    nextPageToken = pl_response.get('nextPageToken')
    if not nextPageToken:
        break

# zip video ids and thumbnail urls into a list
csvPrint = list(zip(vid_thumbnailURL, global_vid_ids))
headerList = ['Thumbnail','VideoID']

# create/open csv file and write to it 
with open(csvData, 'w', newline='') as csvFile:
    dw = csv.DictWriter(csvFile, delimiter=',', fieldnames=headerList)
    dw.writeheader()
    writer = csv.writer(csvFile)

    for i in csvPrint:
        writer.writerows([i])
print(f"{len(csvPrint)} videos added to {csvData}")

# download images from urls in the csv file
urls = pd.read_csv(csvData, usecols=['Thumbnail'])
for i, url in enumerate(urls.values):
    url_to_jpg(i, url[0], FILE_PATH)

# begin defining variables for collage
imageSqrt = math.ceil(math.sqrt(csv_length(csvData)))
mod = math.sqrt(csv_length(csvData)) % 1
if mod > 0 and mod < 0.5:
    mod = 270
else:
    mod = 0
i=0
col=0
row=0
x=0
y=0
breakout = False

# hard coded thumbnail dimenions
# https://developers.google.com/youtube/v3/docs/thumbnails  <--- for thumbnail dimensions
img_x = 480 
img_y = 270

# define the collage dimensions
collage = Image.new("RGBA", (img_x*imageSqrt,(img_y*imageSqrt)-mod))

# writing images to the collage
while row < imageSqrt and breakout == False:
    while col < imageSqrt:
        file = FILE_PATH + "image" + str(i) +".jpg"

        if os.path.exists(file):
            photo = Image.open(file).convert("RGBA")

            #print(f"i:{i},x:{x},y:{y},col:{col},row:{row},image:{file}")
            collage.paste(photo, (x,y))
            #print(f"{file} pasted.\n")

            i += 1
            col += 1
            x += img_x
        else:
            row = imageSqrt
            breakout = True
            break
    x = 0
    y += img_y
    col = 0
    row += 1

# save the collage
print("collaging...")
collage.save("collage.png")

# keep/remove files and folders
if keepImages == True:
    print(f'kept {FILE_PATH}')
    pass
else:
    shutil.rmtree(FILE_PATH)
    print(f'removed {FILE_PATH}')

if keepCSV == True:
    print(f'kept {csvData}')
    pass
else:
    os.remove(csvData)
    print(f'removed {csvData}')

print('finished')