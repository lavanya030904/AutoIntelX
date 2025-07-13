import streamlit as st
import asyncio
from geolocationupdate import GeolocationIPAnalysis
from domainlookupupdate import DomainLookup
from emaillookupupdate import EmailLeakSearch
from usernamelookup import UsernameLookup
from socialmediaupdate import SocialMediaOSINT
from corelationsupdate import DataCorrelation

st.set_page_config(page_title="OSINT Tool", page_icon="🕵️")
st.title("AutoIntelX")
st.markdown("An Advanced Open Source Intelligence (OSINT) tool for gathering and correlating information.")

# Navigation Button for API Configuration
if st.button("Configure API Keys 🔑"):
    st.switch_page("pages/config_manager_updated.py")

# User Inputs
ip = st.text_input("Enter IP Address:")
domain = st.text_input("Enter Domain Name:")
email = st.text_input("Enter Email ID:")
username = st.text_input("Enter Username:")

# Run analysis if at least one input is provided
if st.button("Run OSINT Analysis"):
    if not (ip or domain or email or username):
        st.warning("Please enter at least one field to start the analysis.")
    else:
        st.write("Starting OSINT Analysis...")

        # Initialize tools
        geo_tool = GeolocationIPAnalysis()
        domain_tool = DomainLookup()
        email_tool = EmailLeakSearch()
        username_tool = UsernameLookup()
        social_tool = SocialMediaOSINT()
        correlation_tool = DataCorrelation()

        results = {}

        # Run Geolocation & IP Analysis
        if ip:
            st.write("Running IP Analysis...")
            results["IP Info"] = geo_tool.get_ip_location(ip)
            results["ASN Info"] = geo_tool.get_ip_asn(ip)
            results["Reverse DNS"] = geo_tool.reverse_dns_lookup(ip)

        # Run Domain Lookup
        if domain:
            st.write("Running Domain Lookup...")
            results["Domain IP"] = domain_tool.get_ip(domain)
            results["WHOIS Info"] = domain_tool.get_whois(domain)
            results["DNS Records"] = domain_tool.get_dns_records(domain)

        # Run Email Lookup
        if email:
            st.write("Running Email Leak Search...")
            results["Email Breaches"] = email_tool.search_email_breaches(email)
            results["Email Sources"] = email_tool.search_email_sources(email)

        # Run Username Lookup
        if username:
            st.write("Running Username Lookup...")
            results["Username Lookup"] = asyncio.run(username_tool.lookup(username))

            # Run Social Media OSINT
            st.write("Running Social Media OSINT...")
            results["Twitter Data"] = social_tool.search_twitter_user(username)
            results["Reddit Data"] = social_tool.search_reddit_user(username)
            results["Instagram Data"] = social_tool.search_instagram_user(username)
            results["LinkedIn Data"] = social_tool.search_linkedin_user(username)

        # Correlate Data if multiple inputs exist
        if sum(bool(x) for x in [ip, domain, email, username]) > 1:
            st.write("Correlating Data...")
            if username:
                correlation_tool.add_data_point(username, {"email": email, "ip": ip})
            if email:
                correlation_tool.add_data_point(email, {"breaches": results.get("Email Breaches"), "sources": results.get("Email Sources")})
            if ip:
                correlation_tool.add_data_point(ip, {"asn_info": results.get("ASN Info"), "reverse_dns": results.get("Reverse DNS")})
            if domain:
                correlation_tool.add_data_point(domain, {"whois": results.get("WHOIS Info"), "dns_records": results.get("DNS Records")})

            # Add relationships
            if username and email:
                correlation_tool.add_relationship(username, email, "email_association")
            if username and ip:
                correlation_tool.add_relationship(username, ip, "ip_association")
            if username and domain:
                correlation_tool.add_relationship(username, domain, "domain_association")

            results["Anomalies Detected"] = correlation_tool.detect_anomalies()

        # Display Results
        st.subheader("Results:")
        st.json(results)
        st.success("OSINT Analysis Complete!")
