import argparse

parser = argparse.ArgumentParser(description='Process tweets.')
parser.add_argument('input_file_path', metavar='input_file_path',
                    type=str, nargs=1,
                    help='the file path of the tweets')

parser.add_argument('--debug', '-d',dest='debug',
                    action='store_true', default=False,
                    help='show debug logs (default: hide debug logs)')

parser.add_argument('--num_entries', '-n', dest='num_entries',
                    type=int, default=-1,
                    help='number of entries to process (default: all)')

parser.add_argument('--output', '-o', dest='output_data',
                    action='store_true', default=False,
                    help='output the results (default: no output)')

args = parser.parse_args()

import json
import re
import urllib

class Twitter:
    def __init__(self, user, tweet, retweet_count, reply_count, like_count):
        self.user = user
        self.tweet = tweet
        self.retweet_count = retweet_count
        self.reply_count = reply_count
        self.like_count = like_count

with open(args.input_file_path[0]) as json_data:
    data = json.load(json_data)

entries = [Twitter(tweet['user'], tweet['text'], tweet['retweets'], tweet['replies'], tweet['likes']) for tweet in data]

if args.num_entries > -1:
    entries = entries[:args.num_entries]

# Bios
bios = []
for entry in entries:
    try:
        url = "https://twitter.com/" + entry.user
        f = urllib.urlopen(url)
        page = f.read()
        bios.append([entry.user, re.search('<p class=\"ProfileHeaderCard-bio u-dir\" dir=\"ltr\">(.*)</p>', page).group(1), 'bio'])
    except:
        bios.append([entry.user, '', 'bio'])

# Tweets
tweets = []
retweet_counts = []
reply_counts = []
like_counts = []
for entry in entries:
    tweets.append([entry.user, entry.tweet, 'tweet'])
    retweet_counts.append([entry.user, entry.retweet_count, 'retweet count'])
    reply_counts.append([entry.user, entry.reply_count, 'reply count'])
    like_counts.append([entry.user, entry.like_count, 'like count'])

if args.debug:
    print 'Bios'
    for bio in bios:
        print bio
    print '\n'

    print 'Tweets'
    for tweet in tweets:
        print tweet
    print '\n'

    print 'Retweet count'
    for retweet_count in retweet_counts:
        print retweet_count
    print '\n'

    print 'Reply count'
    for reply_count in reply_counts:
        print reply_count
    print '\n'

    print 'Like count'
    for like_count in like_counts:
        print like_count
    print '\n'

import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

arrs = [bios, tweets, retweet_counts, reply_counts, like_counts]
if not args.output_data:
    if args.debug:
        print 'Not outputting to file'
else:
    if args.debug:
        print 'Outputting to file'
    for arr in arrs:
        for el in arr:
            print el[0] + ',' + el[1] + ',' + el[2]