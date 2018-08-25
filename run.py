import praw
import time
from urllib.request import urlopen
from PIL import ImageFile
import re
import sys
from halo import Halo


client_id = 'XXXX'
client_secret = 'XXXX'
reddit_user = 'XXXX'
reddit_pass = 'XXXX'
target_subreddits = 'recycledrobot+whelks'
user_agent = 'Resbot (by /u/impshum)'


spinner = Halo(text='Running', spinner='dots')
spinner.start()


def getsizes(url):
    file = urlopen(url)
    size = file.headers.get('content-length')
    if size:
        size = int(size)
    p = ImageFile.Parser()
    while True:
        data = file.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            return size, p.image.size
            break
    file.close()
    return size, None


def get_size(size, precision=2):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    suffixIndex = 0
    while size > 1024 and suffixIndex < 4:
        suffixIndex += 1
        size = size / 1024.0
    return '%.*f%s' % (precision, size, suffixes[suffixIndex])


def main():
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent,
                         username=reddit_user,
                         password=reddit_pass)

    subreddit = reddit.subreddit(target_subreddits)
    start_time = int(time.time())
    for post in subreddit.stream.submissions():
        posted_time = int(post.created_utc)
        url = post.url
        if start_time < posted_time and len(re.findall('([-\w]+\.(?:jpg|gif|png|jpeg))', url, re.IGNORECASE)) != 0:
            size, dms = getsizes(url)
            size = get_size(size)
            msg = 'Image info: {}x{} | {}'.format(dms[0], dms[1], size)
            post.reply(msg)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        spinner.succeed('Exiting')
        sys.exit()
