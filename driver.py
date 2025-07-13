import asyncio
from geoloacation import GeolocationIPAnalysis
from domainlookup import DomainLookup
from emaillookup import EmailLeakSearch
from usernamelookup import UsernameLookup
from socialmedia import SocialMediaOSINT
from corelationnew import DataCorrelation

def run_osint(ip, domain, email, username):
    """Run OSINT pipeline for the given IP, domain, email, and username."""
    print("Starting OSINT Analysis...")
    
    # Initialize tools
    geo_tool = GeolocationIPAnalysis()
    domain_tool = DomainLookup()
    email_tool = EmailLeakSearch()
    username_tool = UsernameLookup()
    social_tool = SocialMediaOSINT()
    correlation_tool = DataCorrelation()
    
    # Run Geolocation & IP Analysis
    print("Running IP Analysis...")
    ip_info = geo_tool.get_ip_location(ip)
    asn_info = geo_tool.get_ip_asn(ip)
    reverse_dns = geo_tool.reverse_dns_lookup(ip)
    
    # Run Domain Lookup
    print("Running Domain Lookup...")
    domain_ip = domain_tool.get_ip(domain)
    whois_info = domain_tool.get_whois(domain)
    dns_records = domain_tool.get_dns_records(domain)
    
    # Run Email Lookup
    print("Running Email Leak Search...")
    email_breaches = email_tool.search_email_breaches(email)
    email_sources = email_tool.search_email_sources(email)
    
    # Run Username Lookup
    print("Running Username Lookup...")
    username_results = asyncio.run(username_tool.lookup(username))
    
    # Run Social Media OSINT
    print("Running Social Media OSINT...")
    twitter_data = social_tool.search_twitter_user(username)
    reddit_data = social_tool.search_reddit_user(username)
    insta_data = social_tool.search_instagram_user(username)
    linkedin_data = social_tool.search_linkedin_user(username)
    
    # Correlate Data
    print("Correlating Data...")
    correlation_tool.add_data_point(username, {"email": email, "ip": ip})
    correlation_tool.add_data_point(email, {"breaches": email_breaches, "sources": email_sources})
    correlation_tool.add_data_point(ip, {"asn_info": asn_info, "reverse_dns": reverse_dns})
    correlation_tool.add_data_point(domain, {"whois": whois_info, "dns_records": dns_records})
    correlation_tool.add_relationship(username, email, "email_association")
    correlation_tool.add_relationship(username, ip, "ip_association")
    correlation_tool.add_relationship(username, domain, "domain_association")
    
    # Detect anomalies & generate reports
    anomalies = correlation_tool.detect_anomalies()
    correlation_tool.visualize_graph()
    correlation_tool.generate_report()
    
    # Print Results
    print("--- OSINT RESULTS ---")
    print("IP Info:", ip_info)
    print("ASN Info:", asn_info)
    print("Reverse DNS:", reverse_dns)
    print("Domain IP:", domain_ip)
    print("WHOIS Info:", whois_info)
    print("DNS Records:", dns_records)
    print("Username Lookup:", username_results)
    print("Email Breaches:", email_breaches)
    print("Email Sources:", email_sources)
    print("Twitter Data:", twitter_data)
    print("Reddit Data:", reddit_data)
    print("Instagram Data:", insta_data)
    print("LinkedIn Data:", linkedin_data)
    print("Anomalies Detected:", anomalies)
    print("Report Generated: correlation_report.txt")

# Run OSINT for example values
if __name__ == "__main__":
    run_osint("8.8.8.8", "example.com", "john.doe@gmail.com", "test_user123")
