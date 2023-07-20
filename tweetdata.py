import twit_api

class TweetData:

    def __init__(self, tweet_id):
        self.tweet_id = tweet_id
        t = twit_api.FetchTweet(self.tweet_id)
        self.data = t.get_items()
        self.userdata = self.data["core"]["user_results"]["result"]
        self.tweetdata = self.data["legacy"]

    def screen_name(self):
        screen_name = self.userdata["legacy"]["screen_name"]
        return screen_name

    def full_text(self):
        content = self.tweetdata["full_text"]
        return content

    def video_urls(self):
        videos = []
        for items in self.tweetdata["extended_entities"]["media"]:
            if items["type"] == "video":
                video = items["video_info"]["variants"][0]["url"]
                videos.append(video)
        return videos

    def photo_urls(self):
        photos = []
        for items in self.tweetdata["extended_entities"]["media"]:
            if items["type"] == "photo":
                photo = items["media_url_https"]
                photos.append(photo)
        return photos

    def expanded_urls(self):
        expanded_urls = []
        for items in self.tweetdata['entities']['urls']:
            url = items['expanded_url']
            expanded_urls.append(url)
        return expanded_urls

    def reply_to_user(self):
        if self.tweetdata["in_reply_to_user_id_str"]:
            data = self.tweetdata["in_reply_to_user_id_str"]
        return data

    def quoted_tweet_link(self):
        if self.tweetdata["quoted_status_permalink"]:
            data = self.tweetdata["quoted_status_permalink"]["expanded"]
        return data

class UserData:
    def __init__(self, user):
        self.user = user
        self.data = twit_api.Users(self.user)

    def get_user_id(self):
        data = self.data
        temp = data.get_username_info()
        userid = temp["data"]["user"]["result"]["rest_id"]
        return userid

    def get_user_name(self):
        data = self.data
        temp = data.get_userid_info()
        screen_name = temp["data"]["user"]["result"]["legacy"]["screen_name"]
        return screen_name
