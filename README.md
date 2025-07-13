# AutoIntelX 🔍🛡️

**AutoIntelX** is an advanced automated **OSINT (Open Source Intelligence)** tool designed to streamline the process of gathering intelligence across domains, emails, usernames, social media profiles, and geolocation data. It integrates a Python backend with a modern **Streamlit** frontend, enabling both novice and experienced users to perform investigations efficiently.

---

## 🚀 Features

- 🔗 **Correlation Engine**: Cross-link different data points to find patterns and relationships.
- 🌐 **Domain Lookup**: Get detailed information about any domain.
- 📧 **Email Lookup**: Validate email leaks or breaches using external APIs.
- 🧭 **Geolocation Lookup**: Retrieve approximate location data based on IP.
- 👤 **Username Lookup**: Search usernames across multiple platforms.
- 📱 **Social Media Discovery**: Find social media presence related to email or usernames.
- 🌍 **Web Scraper Module**: Automate web-based intelligence gathering.
- ⚙️ **Config Manager**: Simple configuration and API key handling.

---

## 🧰 Technology Stack

- **Frontend**: [Streamlit](https://streamlit.io/) for interactive UI
- **Backend**: Python 3
- **APIs Used**: OpenAI,Shodan,HaveIBeenPawned,Hunter.io,MaxMind,IPQualityScore etc
- **Other Libraries**: `requests`, `json`, `configparser`, etc.

---

## 📁 Project Structure
AutoIntelX/
│
├── config.ini # Stores API keys and user settings

├── config_manager.py # Handles config parsing

├── corelationsupdate.py # Correlation engine logic

├── domainlookupupdate.py # Domain intelligence gathering

├── emaillookupupdate.py # Email breach check and metadata

├── geolocationupdate.py # IP-based geolocation

├── requirements.txt # Dependencies

├── socialmediaupdate.py # Social media OSINT

├── toolui_oneoption.py # Streamlit UI interface

├── usernamelookup.py # Multi-platform username search

├── webscrapperupdate.py # Web scraping automation


---

## 🔧 Installation

1. **Clone the repository**
<pre> '''bash
git clone https://github.com/lavanya030904/AutoIntelX.git
cd AutoIntelX''' </pre>

## 🙌 Acknowledgements
- Streamlit
- Python
- OSINT community and tools that inspire ethical investigation work

⚠️ This tool is built for educational and ethical research purposes only. Please respect privacy and follow all applicable laws when using AutoIntelX.

