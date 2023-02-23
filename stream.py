#!/usr/bin/env python
import random
import time

import tweeps
from track_mastodon import TweepStream
from utils import log_debug

users = tweeps.Tweeps.listconvert()

log_debug(f"[LOGGING]Start streaming")
while True:
    for user in users:
        check = TweepStream(user)
        check.stream()
        log_debug(f"[LOGGING][WACHT]We wachten 10 seconden tot de volgende")
        time.sleep(10)
