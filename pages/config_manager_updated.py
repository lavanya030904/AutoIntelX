import streamlit as st
import configparser
import os

CONFIG_FILE = "config.ini"

def load_config():
    """Load existing configuration or create a new one if not found."""
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
    else:
        config['API_KEYS'] = {
            'openai_api_key': '',
            'shodan_api_key': '',
            'hibp_api_key': '',
            'hunter_api_key': '',
            'maxmind_api_key': '',
            'ipqualityscore_api_key': ''
        }
        config['Twitter'] = {
            'api_key': '',
            'api_secret': '',
            'access_token': '',
            'access_secret': ''
        }
        config['Reddit'] = {
            'client_id': '',
            'client_secret': '',
            'user_agent': ''
        }
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)
    return config

def save_config(config):
    """Save updated configuration to file."""
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)
    st.success("API keys updated successfully!")

def main():
    st.set_page_config(page_title="OSINT Tool - API Key Configuration", page_icon="🔑")
    
    st.title("OSINT Tool - API Key Configuration")
    
    # Add a button to return to the home page or previous screen
    if st.button("⬅ Back to Home"):
        st.switch_page("toolui_oneoption.py")  # Using rerun to switch back to the home page or desired page
    
    # Load configuration file (existing or create new)
    config = load_config()
    
    # Create the form to input API keys
    st.subheader("Set Your API Keys")
    
    # API keys for general APIs
    openai_key = st.text_input("OpenAI API Key", config['API_KEYS'].get('openai_api_key', ''))
    shodan_key = st.text_input("Shodan API Key", config['API_KEYS'].get('shodan_api_key', ''))
    hibp_key = st.text_input("HaveIBeenPwned API Key", config['API_KEYS'].get('hibp_api_key', ''))
    hunter_key = st.text_input("Hunter.io API Key", config['API_KEYS'].get('hunter_api_key', ''))
    maxmind_key = st.text_input("MaxMind API Key", config['API_KEYS'].get('maxmind_api_key', ''))
    ipquality_key = st.text_input("IPQualityScore API Key", config['API_KEYS'].get('ipqualityscore_api_key', ''))
    
    # API keys for Twitter
    twitter_api_key = st.text_input("Twitter API Key", config['Twitter'].get('api_key', ''))
    twitter_api_secret = st.text_input("Twitter API Secret", config['Twitter'].get('api_secret', ''))
    twitter_access_token = st.text_input("Twitter Access Token", config['Twitter'].get('access_token', ''))
    twitter_access_secret = st.text_input("Twitter Access Secret", config['Twitter'].get('access_secret', ''))
    
    # API keys for Reddit
    reddit_client_id = st.text_input("Reddit Client ID", config['Reddit'].get('client_id', ''))
    reddit_client_secret = st.text_input("Reddit Client Secret", config['Reddit'].get('client_secret', ''))
    reddit_user_agent = st.text_input("Reddit User Agent", config['Reddit'].get('user_agent', ''))
    
    # Button to save the API keys
    if st.button("Save API Keys"):
        # Update the API keys in the configuration
        config['API_KEYS']['openai_api_key'] = openai_key
        config['API_KEYS']['shodan_api_key'] = shodan_key
        config['API_KEYS']['hibp_api_key'] = hibp_key
        config['API_KEYS']['hunter_api_key'] = hunter_key
        config['API_KEYS']['maxmind_api_key'] = maxmind_key
        config['API_KEYS']['ipqualityscore_api_key'] = ipquality_key
        
        # Update the Twitter keys
        config['Twitter']['api_key'] = twitter_api_key
        config['Twitter']['api_secret'] = twitter_api_secret
        config['Twitter']['access_token'] = twitter_access_token
        config['Twitter']['access_secret'] = twitter_access_secret
        
        # Update the Reddit keys
        config['Reddit']['client_id'] = reddit_client_id
        config['Reddit']['client_secret'] = reddit_client_secret
        config['Reddit']['user_agent'] = reddit_user_agent
        
        # Save the updated configuration
        save_config(config)

if __name__ == "__main__":
    main()
