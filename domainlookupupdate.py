import requests
import socket
import whois as whois_lookup
import dns.resolver
import shodan
import configparser

# Load configuration
def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['API_KEYS'].get('shodan_api_key', None)

class DomainLookup:
    def __init__(self, proxy=None):
        self.proxy = {"http": proxy, "https": proxy} if proxy else None
        self.shodan_api_key = load_config()
        self.shodan_api = shodan.Shodan(self.shodan_api_key) if self.shodan_api_key else None

    def get_ip(self, domain):
        """Retrieve the IP address of a domain."""
        try:
            return socket.gethostbyname(domain)
        except socket.gaierror:
            return "Could not resolve domain."

    def get_whois(self, domain):
        """Retrieve WHOIS information of a domain."""
        try:
            return whois_lookup.whois(domain)
        except Exception as e:
            return f"Error: {e}"

    def get_dns_records(self, domain):
        """Retrieve DNS records of a domain."""
        records = {}
        try:
            for record_type in ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA', 'PTR']:  # Added PTR for reverse DNS
                try:
                    answers = dns.resolver.resolve(domain, record_type)
                    records[record_type] = [answer.to_text() for answer in answers]
                except dns.resolver.NoAnswer:
                    records[record_type] = "No record found."
                except dns.resolver.NXDOMAIN:
                    return "Domain does not exist."
        except Exception as e:
            return f"Error: {e}"
        return records

    def get_subdomains(self, domain, wordlist_file=None):
        """Brute-force subdomain enumeration using a wordlist file or default list."""
        subdomains = {}
        if wordlist_file:
            try:
                with open(wordlist_file, 'r') as f:
                    wordlist = [line.strip() for line in f.readlines()]
            except Exception as e:
                return f"Error reading wordlist: {e}"
        else:
            wordlist = ['www', 'mail', 'ftp', 'blog', 'api']
        
        for sub in wordlist:
            subdomain = f"{sub}.{domain}"
            try:
                subdomains[subdomain] = socket.gethostbyname(subdomain)
            except socket.gaierror:
                subdomains[subdomain] = "Not found"
        return subdomains

    def get_shodan_info(self, domain):
        """Retrieve domain-related information from Shodan."""
        if not self.shodan_api:
            return "Shodan API key not configured."
        try:
            ip = self.get_ip(domain)
            if "Could not resolve domain." in ip:
                return ip
            return self.shodan_api.host(ip)
        except shodan.APIError as e:
            return f"Shodan Error: {e}"

    def reverse_ip_lookup(self, ip):
        """Perform a reverse IP lookup to find associated domains."""
        try:
            return socket.gethostbyaddr(ip)
        except socket.herror:
            return "No reverse DNS record found."

# Example Usage
if __name__ == "__main__":
    lookup_tool = DomainLookup()
    domain = "example.com"
    ip_address = lookup_tool.get_ip(domain)
    print("IP Address:", ip_address)
    print("WHOIS Info:", lookup_tool.get_whois(domain))
    print("DNS Records:", lookup_tool.get_dns_records(domain))
    print("Subdomains:", lookup_tool.get_subdomains(domain, wordlist_file="subdomains.txt"))
    print("Shodan Info:", lookup_tool.get_shodan_info(domain))
    print("Reverse IP Lookup:", lookup_tool.reverse_ip_lookup(ip_address))
