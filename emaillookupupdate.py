import requests
import re
import configparser

class EmailLeakSearch:
    def __init__(self, proxy=None):
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.hunter_api_key = config.get("API_KEYS", "hunter_api_key", fallback=None)
        self.hibp_api_key = config.get("API_KEYS", "hibp_api_key", fallback=None)
        self.proxy = {"http": proxy, "https": proxy} if proxy else None

    def validate_email(self, email):
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None

    def search_email_breaches(self, email):
        """Check if an email has been exposed in data breaches using HaveIBeenPwned API."""
        if not self.hibp_api_key:
            return "HIBP API key not configured."
        
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
        headers = {
            "hibp-api-key": self.hibp_api_key,
            "User-Agent": "EmailLeakSearchTool"
        }
        try:
            response = requests.get(url, headers=headers, proxies=self.proxy)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return "No breaches found."
            else:
                return f"Error: {response.status_code}"
        except Exception as e:
            return f"Request failed: {e}"

    def search_email_sources(self, email):
        """Search for email sources using Hunter.io API."""
        if not self.hunter_api_key:
            return "Hunter API key not configured."
        
        url = f"https://api.hunter.io/v2/email-finder?email={email}&api_key={self.hunter_api_key}"
        try:
            response = requests.get(url, proxies=self.proxy)
            if response.status_code == 200:
                return response.json()
            else:
                return f"Error: {response.status_code}"
        except Exception as e:
            return f"Request failed: {e}"

    def search_domain_emails(self, domain):
        """Find all emails associated with a domain using Hunter.io API."""
        if not self.hunter_api_key:
            return "Hunter API key not configured."
        
        url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={self.hunter_api_key}"
        try:
            response = requests.get(url, proxies=self.proxy)
            if response.status_code == 200:
                return response.json()
            else:
                return f"Error: {response.status_code}"
        except Exception as e:
            return f"Request failed: {e}"

    def search_pastebin_leaks(self, email):
        """Check for leaked emails on Pastebin (unofficial method)."""
        url = f"https://psbdmp.ws/api/search/{email}"
        try:
            response = requests.get(url, proxies=self.proxy)
            if response.status_code == 200:
                return response.json()
            else:
                return "No leaks found or access restricted."
        except Exception as e:
            return f"Request failed: {e}"

# Example Usage
if __name__ == "__main__":
    email_tool = EmailLeakSearch()
    email = "example@example.com"
    domain = "example.com"
    if email_tool.validate_email(email):
        print("Breaches:", email_tool.search_email_breaches(email))
        print("Email Sources:", email_tool.search_email_sources(email))
        print("Pastebin Leaks:", email_tool.search_pastebin_leaks(email))
    print("Domain Emails:", email_tool.search_domain_emails(domain))
