import json
import os

import snscrape.modules.twitter

import utils


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

        s = snscrape.modules.twitter.TwitterSearchScraper(
            f"from:{self.user} include:nativeretweets"
        )

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
        for i, t in enumerate(s.get_items()):
            if maxSeen is None:
                maxSeen = t.id
                break
            if t.id <= maxSeen:
                break
            newTweets.append(t)
        if newTweets:
            maxSeen = max(maxSeen, newTweets[0].id)
        with open(f"{maxseendir}/{self.user}.txt", "w") as f:
            f.write(str(maxSeen))
        utils.log_debug("[LOGGING] tweet id written.")

        for tweet in reversed(newTweets):
            tweet_json = json.loads(tweet.json())
            test = tweet_json["inReplyToUser"]
            if test is not None:
                if test["username"] != tweet_json["user"]["username"]:
                    utils.log_debug("[LOGGING]This is a reply")
            else:
                utils.log_debug("[LOGGING]Fresh or threaded tweet")
                make_tweet = utils.Mastodon_Post(
                    tweet_json["user"]["username"], tweet_json
                )
                make_tweet.post_mastodon()
