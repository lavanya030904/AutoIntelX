import requests
import socket
import time
import configparser

class GeolocationIPAnalysis:
    def __init__(self, config_path="config.ini", proxy=None):
        config = configparser.ConfigParser()
        config.read(config_path)
        
        self.maxmind_api_key = config.get("API_KEYS", "MAXMIND_API_KEY", fallback=None)
        self.ip_quality_api_key = config.get("API_KEYS", "IPQUALITYSCORE_API_KEY", fallback=None)
        self.historical_api_key = config.get("API_KEYS", "HISTORICAL_IP_API_KEY", fallback=None)
        self.proxy = {"http": proxy, "https": proxy} if proxy else None

    def get_ip_location(self, ip):
        """Retrieve geolocation data for an IP using MaxMind API."""
        if not self.maxmind_api_key:
            return "MaxMind API key not configured."
        
        url = f"https://geoip.maxmind.com/geoip/v2.1/city/{ip}?key={self.maxmind_api_key}"
        try:
            response = requests.get(url, proxies=self.proxy)
            return response.json() if response.status_code == 200 else f"Error: {response.status_code}"
        except Exception as e:
            return f"Request failed: {e}"

    def get_ip_asn(self, ip):
        """Retrieve ASN (Autonomous System Number) details for an IP."""
        url = f"https://api.iptoasn.com/v1/as/ip/{ip}"
        try:
            response = requests.get(url, proxies=self.proxy)
            return response.json() if response.status_code == 200 else f"Error: {response.status_code}"
        except Exception as e:
            return f"Request failed: {e}"

    def reverse_dns_lookup(self, ip):
        """Perform reverse DNS lookup on an IP address."""
        try:
            return socket.gethostbyaddr(ip)
        except socket.herror:
            return "No reverse DNS record found."

    def check_vpn_proxy(self, ip):
        """Check if an IP is associated with a VPN or proxy using IPQualityScore API."""
        if not self.ip_quality_api_key:
            return "IPQualityScore API key not configured."
        
        url = f"https://www.ipqualityscore.com/api/json/ip/{self.ip_quality_api_key}/{ip}"
        try:
            response = requests.get(url, proxies=self.proxy)
            return response.json() if response.status_code == 200 else f"Error: {response.status_code}"
        except Exception as e:
            return f"Request failed: {e}"

    def get_ip_reputation(self, ip):
        """Retrieve IP reputation score from IPQualityScore API."""
        return self.check_vpn_proxy(ip)
    
    def get_historical_ip_data(self, ip):
        """Retrieve historical geolocation data for an IP."""
        if not self.historical_api_key:
            return "Historical IP API key not configured."
        
        url = f"https://historical-ip-api.example.com/v1/{ip}?key={self.historical_api_key}"
        try:
            response = requests.get(url, proxies=self.proxy)
            return response.json() if response.status_code == 200 else f"Error: {response.status_code}"
        except Exception as e:
            return f"Request failed: {e}"

    def track_ip_real_time(self, ip, interval=10, duration=60):
        """Track an IP's geolocation in real-time for a specified duration."""
        if not self.maxmind_api_key:
            return "MaxMind API key not configured."
        
        tracked_data = []
        for _ in range(duration // interval):
            data = self.get_ip_location(ip)
            tracked_data.append(data)
            time.sleep(interval)
        return tracked_data

# Example Usage
if __name__ == "__main__":
    ip_tool = GeolocationIPAnalysis()
    ip_address = "8.8.8.8"
    print("IP Geolocation:", ip_tool.get_ip_location(ip_address))
    print("ASN Info:", ip_tool.get_ip_asn(ip_address))
    print("Reverse DNS Lookup:", ip_tool.reverse_dns_lookup(ip_address))
    print("VPN/Proxy Check:", ip_tool.check_vpn_proxy(ip_address))
    print("IP Reputation Score:", ip_tool.get_ip_reputation(ip_address))
    print("Historical IP Data:", ip_tool.get_historical_ip_data(ip_address))
    print("Real-Time IP Tracking:", ip_tool.track_ip_real_time(ip_address))
