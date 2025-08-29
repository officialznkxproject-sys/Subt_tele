import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8140097143:AAGBguxo76FrRLYsCueea-haCXEfVO126Fo")
OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "XyraaEx")
OWNER_ID = os.environ.get("OWNER_ID", "083821223529")

# API Keys
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
AUDD_API_KEY = os.environ.get("AUDD_API_KEY", "")
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY", "")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "")

# Premium configuration
PREMIUM_PRICE = 50000  # Rp 50,000
PREMIUM_DURATION = 30  # 30 days

# Database path
DATABASE_PATH = os.environ.get("DATABASE_PATH", "suntbot.db")
