import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
# This is for development only, in production use Zeabur environment variables
if os.path.exists('.env'):
    load_dotenv()
    print("Loaded environment variables from .env file")
else:
    print("No .env file found, using system environment variables")

# Bot configuration
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    print("ERROR: BOT_TOKEN environment variable is required!")
    sys.exit(1)

OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "XyraaEx")
OWNER_ID = os.environ.get("OWNER_ID", "083821223529")

# API Keys (these are optional for basic functionality)
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

# Check if required APIs are available for specific features
if not OPENAI_API_KEY:
    print("WARNING: OPENAI_API_KEY not set. AI features will be limited.")
    
if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY not set. Some AI features may not work.")

print("Configuration loaded successfully")
