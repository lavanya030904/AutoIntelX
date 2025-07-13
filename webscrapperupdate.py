import requests
import json
import praw
import tweepy
import instaloader
import configparser
from bs4 import BeautifulSoup

class SocialMediaOSINT:
    def __init__(self, config_file="config.ini"):
        self.twitter_api = None
        self.reddit_api = None
        self.instaloader = instaloader.Instaloader()
        self.proxy = None
        
        config = configparser.ConfigParser()
        config.read(config_file)
        
        # Load proxy settings
        if "Proxy" in config:
            self.proxy = {
                "http": config.get("Proxy", "http", fallback=None),
                "https": config.get("Proxy", "https", fallback=None)
            }
        
        # Load Twitter API keys
        if "Twitter" in config:
            auth = tweepy.OAuthHandler(config["Twitter"]["api_key"], config["Twitter"]["api_secret"])
            auth.set_access_token(config["Twitter"]["access_token"], config["Twitter"]["access_secret"])
            self.twitter_api = tweepy.API(auth)
        
        # Load Reddit API keys
        if "Reddit" in config:
            self.reddit_api = praw.Reddit(
                client_id=config["Reddit"]["client_id"],
                client_secret=config["Reddit"]["client_secret"],
                user_agent=config["Reddit"]["user_agent"]
            )

    def search_twitter_user(self, username):
        """Fetch Twitter user data by username."""
        if not self.twitter_api:
            return "Twitter API not configured."
        try:
            user = self.twitter_api.get_user(screen_name=username)
            return {
                "name": user.name,
                "username": user.screen_name,
                "bio": user.description,
                "followers": user.followers_count,
                "following": user.friends_count,
                "tweets": user.statuses_count
            }
        except tweepy.TweepError as e:
            return f"Error: {e}"

    def search_reddit_user(self, username):
        """Fetch Reddit user data by username."""
        if not self.reddit_api:
            return "Reddit API not configured."
        try:
            user = self.reddit_api.redditor(username)
            return {
                "name": user.name,
                "karma": user.link_karma + user.comment_karma,
                "created_utc": user.created_utc
            }
        except Exception as e:
            return f"Error: {e}"

    def search_instagram_user(self, username):
        """Fetch Instagram user data by username."""
        try:
            profile = instaloader.Profile.from_username(self.instaloader.context, username)
            return {
                "name": profile.full_name,
                "bio": profile.biography,
                "followers": profile.followers,
                "following": profile.followees,
                "posts": profile.mediacount
            }
        except Exception as e:
            return f"Error: {e}"

    def search_linkedin_user(self, username):
        """Fetch LinkedIn user data by username (public profiles only)."""
        try:
            url = f"https://www.linkedin.com/in/{username}/"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, proxies=self.proxy)
            if response.status_code == 200:
                return {"profile_url": url, "status": "Profile found (public)"}
            else:
                return {"profile_url": url, "status": "Profile not accessible"}
        except Exception as e:
            return f"Error: {e}"

    def username_lookup(self, username):
        """Search for a username across multiple platforms."""
        platforms = {
            "Twitter": f"https://twitter.com/{username}",
            "Reddit": f"https://www.reddit.com/user/{username}",
            "Instagram": f"https://www.instagram.com/{username}/",
            "LinkedIn": f"https://www.linkedin.com/in/{username}/",
            "GitHub": f"https://github.com/{username}",
            "Pinterest": f"https://www.pinterest.com/{username}/",
            "TikTok": f"https://www.tiktok.com/@{username}",
            "YouTube": f"https://www.youtube.com/{username}"
        }
        results = {}
        headers = {'User-Agent': 'Mozilla/5.0'}
        for platform, url in platforms.items():
            try:
                response = requests.get(url, headers=headers, proxies=self.proxy)
                if response.status_code == 200:
                    results[platform] = "Profile found"
                else:
                    results[platform] = "Profile not found"
            except Exception as e:
                results[platform] = f"Error: {e}"
        return results

# Example Usage
if __name__ == "__main__":
    sm_osint = SocialMediaOSINT(config_file="config.ini")
    print(sm_osint.search_twitter_user("jack"))
    print(sm_osint.search_reddit_user("spez"))
    print(sm_osint.search_instagram_user("instagram"))
    print(sm_osint.search_linkedin_user("linkedin_username"))
    print(sm_osint.username_lookup("jack"))
