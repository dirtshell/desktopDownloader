# /r/EarthPorn Desktop Downloading Script v1.0
# By dirtshell
#
# DESCRIPTION
# I made this script because I lacked getting new desktop
# backgrounds from reddit. I originally wrote this for getting
# desktops from /r/earthporn, but it can be used for a bunch
# of others.The idea is that in Windows or some other OS you have a
# folder of images that act as a slide show for your
# wallpaper. This bot finds images on an a subreddit and
# downloads them to (DESKTOP_DIR). Now, you can be
# getting new and interesting wallpapers daily. HUZZAH! 
# Unfortunately, you will need to look into how your OS 
# handles the desktop slide show feature.
#
# BUGS
# *  Currently doesn't play too friendly with posts that don't
#    include the actual path to the image in the URL. I have a
#    really lazy workaround in place that is still error prone,
#    just less so than an implementation with no checking. It
#    will simply ignore posts without direct links.
# *  Very lazy and unpythonic check if the image is a duplicate
#    using a flag and a loop break. Need to implement this correctly
#    to save face.
# *  No error handling in case there is an issue connecting to
#    reddit or the target image.
# *  Does not detect the image type and simply saves it as a 
#    PNG, so that there is compatibility with Windows =/. No
#    noticeable difference though afaik.

from PIL import ImageFile
import praw
import os
import urllib.request

# Create the PRAW interface
user_agent = "/r/EarthPorn Personal Wallpaper Scraper v0.314 by /u/dirtshell"
r = praw.Reddit(user_agent=user_agent)

MIN_RES_X = 2000
MIN_RES_Y = 2000
SUBREDDIT = 'skyporn'    # Change this depending on your personal fetish
DESKTOP_DIR = 'C:\\Users\\jake\\Pictures\\Sky Porn\\'    # Change this,keep the trailing slash
POST_LIMIT = 50     # The number of posts to analyse at a time

subreddit = r.get_subreddit(SUBREDDIT)    # Refresh the subreddit
downloaded_pics = os.listdir(DESKTOP_DIR)  # Load the files in the directory only once per main loop
downloaded_count = 0  # A count of the number of pics downloaded

# Function to check the image size without downloading the whole file
# This function checks the headers of the image to get the size
# Code from http://effbot.org/zone/pil-image-size.htm
def get_sizes(uri):
    file = urllib.request.urlopen(uri)
    p = ImageFile.Parser()
    while 1:
        data = file.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            return p.image.size
            break
    file.close()
    return None, None  # There was an issue

# Cycle through each recent post and create a list of possible desktop candidates
for submission in subreddit.get_hot(limit=POST_LIMIT):
    print(submission.title)
    res_x, res_y = get_sizes(submission.url)    # The x and y of the pic
    if res_x is None or res_y is None:
        continue  # If there was an issue go on to the next submission

    # Check if the image size is acceptable
    if res_x >= MIN_RES_X and res_y >= MIN_RES_Y:
        # Check if it is a direct link to an image
        if '.' in submission.url.split('/')[-1]:
            duplicate = False   # A flag indicating whether the image is new
            for name in downloaded_pics:
                if name == submission.id:  # Check the names of the downloaded files against the current one
                    duplicate = True
                    break
            if not duplicate:    # The file in the URL has NOT already been downloaded
                print('Downloading ' + submission.id + '...')
                urllib.request.urlretrieve(submission.url, DESKTOP_DIR + submission.id + '.jpeg')
                downloaded_count += 1
        else:
            print('This is not a direct link')
    else:
        print('Too small')
print('A total of {0} pics were downloaded'.format(downloaded_count))