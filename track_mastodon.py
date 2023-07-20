import json
import os

import utils
import twit_api
import tweetdata
class TweepStream:
    def __init__(self, user):
        self.user = user

    def stream(self):
        """Stream tweets from the actual users and reply to them.

        :param list users: List of users to track.

        returns: none

        rtype: str
        """
        utils.log_debug(f"[LOGGING]Check fresh tweets for {self.user}")

        workdir = os.getcwd()
        maxseendir = f"{workdir}/txt"
        if not os.path.isdir(maxseendir):
            os.mkdir(maxseendir)
        try:
            current = open(f"{maxseendir}/{self.user}.txt")
            for i in current:
                maxSeen = i.rstrip("\n")
                maxSeen = int(maxSeen)
        except:
            maxSeen = None

        newTweets = []
        temp = twit_api.UserTimeline(self.user)
        s = temp.list_user_tweets()
        for t in s:
            t = int(t)
            if maxSeen is None:
                maxSeen = t
                break
            if t <= maxSeen:
                break
            newTweets.append(t)
        if newTweets:
            maxSeen = max(maxSeen, newTweets[0])

        for tweet in reversed(newTweets):
            tweets = tweetdata.TweetData(tweet)
            try:
                test = tweets.reply_to_user()
            except:
                test = None
            if test is not None:
                if test != self.user:
                    utils.log_debug("[LOGGING]This is a reply")
            else:
                utils.log_debug("[LOGGING]Fresh or threaded tweet")
                make_tweet = utils.Mastodon_Post(self.user, tweet)
                make_tweet.post_mastodon()
        with open(f"{maxseendir}/{self.user}.txt", "w") as f:
            f.write(str(maxSeen))
        utils.log_debug("[LOGGING] tweet id written.")
