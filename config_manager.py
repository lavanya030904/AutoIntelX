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
    if st.button("⬅ Back to Home"):
        st.switch_page("toolui_oneoption.py")
    
    config = load_config()
    
    st.subheader("Set Your API Keys")
    openai_key = st.text_input("OpenAI API Key", config['API_KEYS'].get('openai_api_key', ''))
    shodan_key = st.text_input("Shodan API Key", config['API_KEYS'].get('shodan_api_key', ''))
    hibp_key = st.text_input("HaveIBeenPwned API Key", config['API_KEYS'].get('hibp_api_key', ''))
    hunter_key = st.text_input("Hunter.io API Key", config['API_KEYS'].get('hunter_api_key', ''))
    maxmind_key = st.text_input("MaxMind API Key", config['API_KEYS'].get('maxmind_api_key', ''))
    ipquality_key = st.text_input("IPQualityScore API Key", config['API_KEYS'].get('ipqualityscore_api_key', ''))
    
    if st.button("Save API Keys"):
        config['API_KEYS']['openai_api_key'] = openai_key
        config['API_KEYS']['shodan_api_key'] = shodan_key
        config['API_KEYS']['hibp_api_key'] = hibp_key
        config['API_KEYS']['hunter_api_key'] = hunter_key
        config['API_KEYS']['maxmind_api_key'] = maxmind_key
        config['API_KEYS']['ipqualityscore_api_key'] = ipquality_key
        save_config(config)

if __name__ == "__main__":
    main()
