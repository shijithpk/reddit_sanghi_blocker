### About the repo 

Wrote a basic python script for blocking Hindu nationalist trolls ('sanghis' in Indian lingo) who're active in r/India and my state subreddit r/Kerala.

(Here's the script [reddit_sanghi_blocker.py](reddit_sanghi_blocker.py), best to run it with a scheduler like cron, instructions on how to use it are within.)

Basically it sees who're the redditors active in Hindu nationalist subreddits (r/Indiaspeaks, r/Chodi etc.) and in normal subreddits (r/India, r/Kerala) over the past month. The redditors most active in the sanghi-verse AND in normal-verse get blocked. The plan is to run the script every Thursday, and block 5 sanghis every week.

(You can block more than 5 if you want, just adjust the parameters in the script. Have put comments everywhere so you know exactly what's going on at each step.)

This script will solve the problem of long-term sanghis polluting the comment sections, and help you get some peace of mind. It won't solve the problem of IT cell alts that are a few months old--and who aren't members of sanghi subreddits--swarming the comments, solving that is a little more complicated.

(Also, if any of you are working in ML, I guess this can be seen as a problem of how to classify someone as a 'sanghi troll' using their subreddit memberships, posts upvoted, textual analysis of their comments etc. If you can create something more sophisticated than this script, please do so and share it with me!)