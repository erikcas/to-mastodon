import requests
import json
import enum

#auth
#auth = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
auth = "Bearer AAAAAAAAAAAAAAAAAAAAAFQODgEAAAAAVHTp76lzh3rFzcHbmHVvQxYYpTw%3DckAlMINMjmCwxUcaXbAN4XqJVdgMJaHqNOFgPMK0zN1qLqLQCF"
content = "application/x-www-form-urlencoded;charset=UTF-8"
grant_type = "client_credentials"
agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0"

#urls
base_url = "https://api.twitter.com"
auth_url = f"{base_url}/1.1/guest/activate.json"
graph_url = f"{base_url}/graphql"
user_url = f"{base_url}/1.1/users/search.json"

def get_auth():
    headers = {"Authorization": auth, "user-agent": agent, "Content-Type": content}
    data = {"grant_type": grant_type}
    r = requests.post(auth_url, data  = data, headers = headers)
    return r.json()['guest_token']

class Users:

    def __init__(self, user):
        self.user = user

        self.user_vars = {"withSafetyModeUserFields": True}

        self.user_features = {"hidden_profile_likes_enabled": False,
                              "hidden_profile_subscriptions_enabled": False,
                              "responsive_web_graphql_exclude_directive_enabled": True,
                              "verified_phone_label_enabled": False,
                              "subscriptions_verification_info_verified_since_enabled": True,
                              "highlights_tweets_tab_ui_enabled": True,
                              "creator_subscriptions_tweet_preview_api_enabled": True,
                              "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                              "responsive_web_graphql_timeline_navigation_enabled": True,
                              "super_follow_badge_privacy_enabled": False,
                              "subscriptions_verification_info_enabled": True,
                              "blue_business_profile_image_shape_enabled": False,
                              "creator_subscriptions_subscription_count_enabled": False,
                              "super_follow_user_api_enabled": False,
                              "super_follow_exclusive_tweet_notifications_enabled": False
                              }
        
    def get_username_info(self):

        graphql = "pVrmNaXcxPjisIvKtLDMEA/UserByScreenName"
        self.user_vars["screen_name"] = self.user
        variables = json.dumps(self.user_vars)
        features = json.dumps(self.user_features)
        params = {"variables": variables, "features": features}

        guest_token = get_auth()
        headers = {"Authorization": auth, "x-guest-token": guest_token}
        resp = requests.get(f"{graph_url}/{graphql}", headers=headers, params=params)
        return resp.json()

    def get_userid_info(self):

        graphql = "1YAM811Q8Ry4XyPpJclURQ/UserByRestId"
        self.user_vars["userId"] = self.user
        variables = json.dumps(self.user_vars)
        features = json.dumps(self.user_features)
        params = {"variables": variables, "features": features}

        guest_token = get_auth()
        headers = {"Authorization": auth, "x-guest-token": guest_token}
        resp = requests.get(f"{graph_url}/{graphql}", headers=headers, params=params)
        return resp.json()

class Tweets:

    def __init__(self, user):
        self.user = user
        self.variables = {"userId": self.user,
                          "count":100,
                          "cursor": None,
                          "includePromotedContent":True,
                          "withVoice":True,
                          "withV2Timeline":True
                          }

        self.features = {"rweb_lists_timeline_redesign_enabled":True,
                         "responsive_web_graphql_exclude_directive_enabled":True,
                         "verified_phone_label_enabled":False,
                         "creator_subscriptions_tweet_preview_api_enabled":True,
                         "responsive_web_graphql_timeline_navigation_enabled":True,
                         "responsive_web_graphql_skip_user_profile_image_extensions_enabled":False,
                         "tweetypie_unmention_optimization_enabled":True,
                         "responsive_web_edit_tweet_api_enabled":True,
                         "graphql_is_translatable_rweb_tweet_is_translatable_enabled":True,
                         "view_counts_everywhere_api_enabled":True,
                         "longform_notetweets_consumption_enabled":True,
                         "responsive_web_twitter_article_tweet_consumption_enabled":False,
                         "tweet_awards_web_tipping_enabled":False,
                         "freedom_of_speech_not_reach_fetch_enabled":True,
                         "standardized_nudges_misinfo":True,
                         "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":True,
                         "longform_notetweets_rich_text_read_enabled":True,
                         "longform_notetweets_inline_media_enabled":True,
                         "responsive_web_media_download_video_enabled":False,
                         "responsive_web_enhance_cards_enabled":False
                         }

    def get_timeline(self):

        graphql = "2GIWTr7XwadIixZDtyXd4A/UserTweets"
        
        self.variables["withQuickPromoteEligibilityTweetFields"] = True
        variables = json.dumps(self.variables)
        features = json.dumps(self.features)
        params = {'variables': variables, 'features': features}
        
        guest_token = get_auth()
        headers = {"Authorization": auth, "x-guest-token": guest_token}
        
        resp = requests.get(f"{graph_url}/{graphql}", headers=headers, params=params)
        return resp.json()

    def get_timeline_with_replies(self):

        graphql= "1-5o8Qhfc2kWlu_2rWNcug/UserTweetsAndReplies"

        self.variables["withCommunity"] = True
        variables = json.dumps(self.variables)
        features = json.dumps(self.features)
        params = {'variables': variables, 'features': features}
        
        guest_token = get_auth()
        headers = {"Authorization": auth, "x-guest-token": guest_token}
        
        resp = requests.get(f"{graph_url}/{graphql}", headers=headers, params=params)
        return resp.json()

class UserTimeline:

    def __init__(self, username):
        self.username = username

    def list_user_tweets(self, limit=120):
        list_tweets = []
        cursor = None

        tweeps = Users(self.username)
        tweep = tweeps.get_username_info()
        tweep = tweep['data']['user']['result']['rest_id']

        tweets = Tweets(tweep)
        json_response = tweets.get_timeline()

        result = json_response["data"]["user"]["result"]
        timeline = result["timeline_v2"]["timeline"]["instructions"]
        entries = [x["entries"] for x in timeline if x["type"] == "TimelineAddEntries"]
        entries = entries[0] if entries else []
        for entry in entries:
            content = entry["content"]
            entry_type = content["entryType"]
            if entry_type == "TimelineTimelineItem":
                item_result = content["itemContent"]["tweet_results"]["result"]
                tweet_id = item_result["rest_id"]
                legacy = item_result["legacy"]
                list_tweets.append(tweet_id)
            elif entry_type == "TimelineTimelineModule":
                item_result = content["items"][0]["item"]["itemContent"]["tweet_results"]["result"]
                tweet_id = item_result["rest_id"]
                legacy = item_result["legacy"]
                list_tweets.append(tweet_id)

        return list_tweets

    def list_user_tweets_and_replies(self, limit=120):
        list_tweets = []
        cursor = None

        tweeps = Users(self.username)
        tweep = tweeps.get_username_info()
        tweep = tweep['data']['user']['result']['rest_id']

        tweets = Tweets(tweep)
        json_response = tweets.get_timeline_with_replies()

        result = json_response["data"]["user"]["result"]
        timeline = result["timeline_v2"]["timeline"]["instructions"]
        entries = [x["entries"] for x in timeline if x["type"] == "TimelineAddEntries"]
        entries = entries[0] if entries else []
        for entry in entries:
            content = entry["content"]
            entry_type = content["entryType"]
            if entry_type == "TimelineTimelineModule":
                item_result = content["items"][0]["item"]["itemContent"]["tweet_results"]["result"]
                tweet_id = item_result["rest_id"]
                legacy = item_result["legacy"]
                list_tweets.append(tweet_id)

        return list_tweets

class FetchTweet:

    def __init__(self, tweet_id):
        self.tweet_id = tweet_id

        self.variables = {"focalTweetId": self.tweet_id,
                "with_rux_injections": False,
                "includePromotedContent": True,
                "withCommunity": True,
                "withQuickPromoteEligibilityTweetFields": True,
                "withBirdwatchNotes": True,
                "withVoice": True,
                "withV2Timeline": True
                }

        self.features = {"rweb_lists_timeline_redesign_enabled": True,
                "responsive_web_graphql_exclude_directive_enabled": True,
                "verified_phone_label_enabled": False,
                "creator_subscriptions_tweet_preview_api_enabled": True,
                "responsive_web_graphql_timeline_navigation_enabled": True,
                "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                "tweetypie_unmention_optimization_enabled": True,
                "responsive_web_edit_tweet_api_enabled": True,
                "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                "view_counts_everywhere_api_enabled": True,
                "longform_notetweets_consumption_enabled": True,
                "responsive_web_twitter_article_tweet_consumption_enabled": False,
                "tweet_awards_web_tipping_enabled": False,
                "freedom_of_speech_not_reach_fetch_enabled": True,
                "standardized_nudges_misinfo": True,
                "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                "longform_notetweets_rich_text_read_enabled": True,
                "longform_notetweets_inline_media_enabled": True,
                "responsive_web_media_download_video_enabled": False,
                "responsive_web_enhance_cards_enabled": False
                }

    def fetch_tweet(self):

        graphql = "-Ls3CrSQNo2fRKH6i6Na1A/TweetDetail"

        variables = json.dumps(self.variables)
        features = json.dumps(self.features)
        params = {'variables': variables, 'features': features}

        guest_token = get_auth()
        headers = {"Authorization": auth, "x-guest-token": guest_token}

        resp = requests.get(f"{graph_url}/{graphql}", headers=headers, params=params)
        return resp.json()

    def get_items(self):

        raw_tweet = FetchTweet(self.tweet_id)
        json_response = raw_tweet.fetch_tweet()

        result = json_response["data"]["threaded_conversation_with_injections_v2"]
        timeline = result["instructions"]
        entries = [x["entries"] for x in timeline if x["type"] == "TimelineAddEntries"]
        entries = entries[0] if entries else []
        for entry in entries:
            content = entry["content"]
            entry_type = content["entryType"]
            if entry_type == "TimelineTimelineItem":
                if content["itemContent"]["itemType"] == "TimelineTweet":
                 item_result = entry['content']['itemContent']['tweet_results']['result']
        return item_result

