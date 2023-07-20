import json
import logging
import os
import re
import time

import magic
import wget
import youtube_dl

from mastodon import Mastodon
import tweetdata

logging.basicConfig(
    filename="mastodon_log.log",
    filemode="a",
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    level=logging.DEBUG,
)

cur_dir = os.getcwd()
workdir = f"{cur_dir}/workdir"
os.system(f"rm -rf wortkdir")
if not os.path.isdir(f"{workdir}"):
    os.mkdir(f"{workdir}")


def log_debug(debug):
    """Simple logging functionality.
    Log level set to debug

    returns: logging

    rtype: str
    """

    return logging.debug(debug)


def get_api(user):
    secrets = open(f".{user}.json")
    login = json.load(secrets)

    client_key = login["client_key"]
    client_secret = login["client_secret"]
    access_token = login["access_token"]

    api = Mastodon(
        client_key, client_secret, access_token, api_base_url="https://retrotweets.com"
    )

    return api


def empty_workdir():
    for file in os.listdir(workdir):
        os.system(f"rm {workdir}/{file}")


def video_download(url):
    options = {"forceurl": True, "outtmpl": "workdir/temp.%(ext)s"}
    youtube_dl.YoutubeDL(options).download([url])


def photo_download(url):
    wget.download(url, out=workdir)


class Mastodon_Post:
    def __init__(self, user, tweet):
        self.user = user
        self.tweet = tweet

    def post_mastodon(self):
        media_id = []
        empty_workdir()
        api = get_api(self.user)
        data = tweetdata.TweetData(self.tweet)
        screen_name = data.screen_name()
        full_text = data.full_text()
        expanded_urls = data.expanded_urls()
        for i in expanded_urls:
            expanded_url = i
        retweet_url = f"https://twitter.com/{screen_name}/status/{self.tweet}"
        # Check if this is a tweet or a retweet
        if screen_name != self.user:
            # If this is a retweet, post a link to the twitterpost
            text = f"{self.user} retweeted on twitter:\n\n{retweet_url}"
        else:
            text = full_text
            # Remove short urls
            try:
                text = re.sub(
                    r"https:(\/\/t\.co\/([A-Za-z0-9]|[A-Za-z]){10})",
                    f"{expanded_url}",
                    text,
                    flags=re.MULTILINE,
                )
                log_debug("[LOGGING]Short url removed")
            except:
                pass
            # Test if this is a quoted tweet. If yes, add the link to the quouted tweet
            try:
                quoted = data.quoted_tweet_link()
                text += f"\n\n{quoted}"
                log_debug("[LOGGING]Quoted tweet, link added")
            except:
                log_debug("[LOGGING]Not a quoted tweet")
        # Get mediafiles
        try:
            mime = magic.Magic(mime=True)
            videos = data.video_urls()
            if videos != []:
                try:
                    for item in videos:
                        empty_workdir()
                        video_download(item)
                        for video in os.listdir(workdir):
                                media = api.media_post(f"{workdir}/{video}")
                                media_id.append(media)
                                time.sleep(20)
                                empty_workdir()
                        log_debug("[LOGGING]Video detected and uploaded")
                except:
                    log_degug("No videos detected")
            photos = data.photo_urls()
            if photos != []:
                try:
                    for item in photos:
                        empty_workdir()
                        photo_download(item)
                        for photo in os.listdir(workdir):
                                plaatje = mime.from_file(f"{workdir}/{photo}")
                                media = api.media_post(
                                    f"{workdir}/{photo}", mime_type=plaatje
                                )
                                media_id.append(media)
                                empty_workdir()
                        log_debug("[LOGGING]Image(s) detected and uploaded")
                except Exception as e:
                    log_debug(f"[LOGGING]No images detected {e}")
        except:
            log_debug("[LOGGING]No media detected")

        # Let's post, but do a final check on removable short urls
        text = re.sub(
                r"https:(\/\/t\.co\/([A-Za-z0-9]|[A-Za-z]){10})",
                "",text,
                flags=re.MULTILINE,
                )
        try:
            api.status_post(text, media_ids=media_id)
            log_debug("[LOGGING]Text + media posted")
        except Exception as e:
            api.toot(text)
            log_debug("[LOGGING]Only text, posted")
