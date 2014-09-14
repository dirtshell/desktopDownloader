# /r/EarthPorn Desktop Downloading Script v1.0
# By dirtshell
#
# DESCRIPTION
# The idea is that in Windows or some other OS you have a
# folder of images that act as a slide show for your
# wallpaper. This bot finds images on an /r/*porn subreddit and
# downloads them to this folder (DESKTOP_DIR). Now, you are
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
#    using a flag a loop break. Need to implement this correctly
#    to save face.
# *  No error handling in case there is an issue connecting to
#    reddit.
# *  Does not detect the image type and simply saves it as a 
#    PNG, so that there is compatibility with Windows =/. No
#    noticeable difference though afaik.


import praw, re, os, time, urllib.request

# Create the PRAW interface
user_agent = ("/r/EarthPorn Personal Wallpaper Scraper v0.314 by /u/dirtshell")
r = praw.Reddit(user_agent=user_agent)

MIN_RES_X = 2000
MIN_RES_Y = 2000
SLEEP_TIME = 1800   # Time between refreshes in seconds
SUBREDDIT = 'earthporn'    # Change this depending on your personal fetish
DESKTOP_DIR = 'C:\\Users\\jacob\\Pictures\\Earthporn\\'    # Change this depending on your setup, but keep the trailing slash
POST_LIMIT = 50     # The number of posts to analyse at a time

subreddit = r.get_subreddit(SUBREDDIT)    # Refresh the subreddit
downloaded_pics = os.listdir(DESKTOP_DIR) # Load the files in the directory only once per main loop
downloaded_count = 0 # A count of the number of pics downloaded
   
# Cycle through each recent post and create a list of possible desktop candidates
for submission in subreddit.get_hot(limit=POST_LIMIT):
    print(submission.title)
    match = re.search('\[([,\d]+)\s*x\s*([,\d]+)\]', submission.title)    # Check for the resolution
    if (match == None): # A quick check to make sure the post is a picture
        print('No matches')
        continue
    res_x = int(match.groups()[0].replace(',',''))    # The x of the pic w/o commas
    res_y = int(match.groups()[1].replace(',',''))    # The y of the pic w/o commas
    if (res_x >= MIN_RES_X and res_y >= MIN_RES_Y):
        if '.' in submission.url.split('/')[-1]:    # SUPER lazy test to check if it is a direct link to an image
            duplicate = False   # Once again, because I am lazy
            for name in downloaded_pics:
                if (name == submission.id): # Check the names of the downloaded files against the current one
                    duplicate = True    # This is lazy af
                    break   # Stop checking if it has already been downloaded
            if not duplicate:    # The file in the URL has NOT already been downloaded
                print('Downloading ' + submission.id + '...')
                urllib.request.urlretrieve(submission.url, DESKTOP_DIR + submission.id + '.jpeg')
                downloaded_count = downloaded_count + 1;
        else:
            print('This is not a direct link')
    else:
        print('Too small')
print('A total of {0} pics were downloaded'.format(downloaded_count))
