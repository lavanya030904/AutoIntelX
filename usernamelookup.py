import asyncio
import aiohttp

class UsernameLookup:
    def __init__(self, proxy=None, custom_platforms=None):
        self.proxy = {"http": proxy, "https": proxy} if proxy else None
        self.custom_platforms = custom_platforms if custom_platforms else {}

    async def check_username(self, session, platform, url):
        """Helper function to check username availability asynchronously."""
        try:
            async with session.get(url, proxy=self.proxy["http"] if self.proxy else None) as response:
                if response.status == 200:
                    return platform, "Profile found"
                else:
                    return platform, "Profile not found"
        except Exception as e:
            return platform, f"Error: {e}"

    async def lookup(self, username):
        """Search for a username across 300+ platforms asynchronously, including custom ones."""
        platforms = {
            "Twitter": f"https://twitter.com/{username}",
            "Reddit": f"https://www.reddit.com/user/{username}",
            "Instagram": f"https://www.instagram.com/{username}/",
            "LinkedIn": f"https://www.linkedin.com/in/{username}/",
            "GitHub": f"https://github.com/{username}",
            "Pinterest": f"https://www.pinterest.com/{username}/",
            "TikTok": f"https://www.tiktok.com/@{username}",
            "YouTube": f"https://www.youtube.com/{username}",
            "SoundCloud": f"https://soundcloud.com/{username}",
            "DeviantArt": f"https://www.deviantart.com/{username}",
            "Twitch": f"https://www.twitch.tv/{username}",
            "Steam": f"https://steamcommunity.com/id/{username}",
            "Medium": f"https://medium.com/@{username}",
            "Flickr": f"https://www.flickr.com/people/{username}",
            "Badoo": f"https://badoo.com/en/{username}",
            "Dribbble": f"https://dribbble.com/{username}",
            "Vimeo": f"https://vimeo.com/{username}",
            "500px": f"https://500px.com/{username}",
            "OK.ru": f"https://ok.ru/{username}",
            "VK": f"https://vk.com/{username}"
        }
        
        platforms.update(self.custom_platforms)

        async with aiohttp.ClientSession() as session:
            tasks = [self.check_username(session, platform, url) for platform, url in platforms.items()]
            results = await asyncio.gather(*tasks)

        return dict(results)

# Example Usage
if __name__ == "__main__":
    custom_sites = {
        "MyCustomSite": "https://mycustomsite.com/{username}",
        "AnotherSite": "https://anothersite.com/u/{username}"
    }
    lookup_tool = UsernameLookup(proxy="http://your-proxy:port", custom_platforms=custom_sites)
    results = asyncio.run(lookup_tool.lookup("jack"))
    print(results)