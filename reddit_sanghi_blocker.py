from datetime import datetime
from dateutil.relativedelta import relativedelta
import praw
from psaw import PushshiftAPI
from collections import defaultdict

# fill client id, client secret below after creating web app at https://www.reddit.com/prefs/apps/
# follow user-agent format from https://praw.readthedocs.io/en/stable/getting_started/quick_start.html
# to get refresh token, follow directions on this page https://praw.readthedocs.io/en/latest/tutorials/refresh_token.html
reddit = praw.Reddit(
	client_id="XXXXXXXXXXXXXXXX",
	client_secret="XXXXXXXXXXXXXXXXXXXXXXXX",
	user_agent="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
	redirect_uri="http://localhost:8080",
	refresh_token="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
	)

# use line below if you're using praw.ini For info, check https://praw.readthedocs.io/en/stable/getting_started/configuration/prawini.html
#reddit = praw.Reddit("bot1", config_interpolation="basic")

pshift = PushshiftAPI(reddit)

# get list of usernames already blocked by authenticated user 
blocked_username_list_raw = reddit.user.blocked()
blocked_username_list = [x.name for x in blocked_username_list_raw]

# getting epoch values/unix timestamps for right now, and one month ago
time_now = datetime.utcnow()
time_now_epoch = int(time_now.timestamp())

# time_one_week_ago = time_now - relativedelta(weeks=1)
# time_one_week_ago_epoch = int(time_one_week_ago.timestamp())

time_one_month_ago = time_now - relativedelta(months=1)
time_one_month_ago_epoch = int(time_one_month_ago.timestamp())

# subreddits in sanghiverse
target_subreddit_list = [
						'IndiaSpeaks',
						'indiadiscussion',
						'indianews',
						'Chodi',
						'KeralaSpeaks',
						'SanghiKeralam',
						'Samaj',
						'Desimeta',
						]

# subreddits you visit
normal_subreddit_list = [
						'India', # if you just want to block sanghi redditors active in r-Kerala, comment out this line
						'Kerala',
						]

# getting list of redditors active for past one month in sanghi subreddits  
sanghi_redditor_dict = defaultdict(int)
for subreddit in target_subreddit_list:
	comment_generator = pshift.search_comments(
												subreddit=subreddit,
												after = time_one_month_ago_epoch,
												before = time_now_epoch,
												)
	for comment in comment_generator:
		try:
			sanghi_redditor_dict[comment.author.name] += 1
		except:
			continue

# getting list of redditors active for past one month in subreddits I visit 
normal_redditor_dict = defaultdict(int)
for subreddit in normal_subreddit_list:
	comment_generator = pshift.search_comments(
												subreddit=subreddit,
												after = time_one_month_ago_epoch,
												before = time_now_epoch,
												)
	for comment in comment_generator:
		try:
			normal_redditor_dict[comment.author.name] += 1
		except:
			continue

# sorting dictionaries in descending order so users with most comments in the month come first
sanghi_redditor_dict_sorted = dict(sorted(sanghi_redditor_dict.items(), key=lambda item: item[1], reverse=True))
normal_redditor_dict_sorted = dict(sorted(normal_redditor_dict.items(), key=lambda item: item[1], reverse=True))

sanghi_redditor_dict_sorted_members = list(sanghi_redditor_dict_sorted.keys())
normal_redditor_dict_sorted_members = list(normal_redditor_dict_sorted.keys())

# finding redditors active in both normal subreddits and sanghi-verse
common_redditor_set = set(sanghi_redditor_dict_sorted_members) & set(normal_redditor_dict_sorted_members)

# excluding some useful bots from the set
usernames_for_exclusion = ['AutoModerator','autotldr']
for username in usernames_for_exclusion:
	common_redditor_set.remove(username)

# the index sum gives us an idea of how active a redditor is in both normal reddits and sanghi-verse
	# the lower the index sum, the more active they are in both 'universes'
common_redditor_dict = {}
for redditor in common_redditor_set:
	common_redditor_dict[redditor]={}
	common_redditor_dict[redditor]['sanghi_dict_index'] = sanghi_redditor_dict_sorted_members.index(redditor)
	common_redditor_dict[redditor]['normal_dict_index'] = normal_redditor_dict_sorted_members.index(redditor)
	common_redditor_dict[redditor]['index_sum'] = (sanghi_redditor_dict_sorted_members.index(redditor) + 
													normal_redditor_dict_sorted_members.index(redditor))

# sorting this dictionary so that redditors with lowest index_sum come first
	# if two redditors have same index_sum, one with lower index in normal reddits, ie. the one more active in normal reddits comes first
common_redditor_dict_sorted = dict(sorted(common_redditor_dict.items(), 
										key=lambda item: (item[1]['index_sum'], item[1]['normal_dict_index'])
										))

# Have read somewhere there is limit on no. of users that can be blocked in total
	# so only blocking 5 users in a week, you can set it higher
max_users_to_block_in_week = 5

# getting first five redditors from common_redditor_dict
users_for_blocking_list = list(common_redditor_dict_sorted.keys())[0:max_users_to_block_in_week]

# block everyone in blockee list
for username in users_for_blocking_list:
 	reddit.redditor(username).block()
