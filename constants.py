import os

from dotenv import load_dotenv

load_dotenv()
AI_MODEL = os.getenv("AI_MODEL")
AI_BASE_URL = os.getenv("AI_BASE_URL")
AI_API_KEY = os.getenv("AI_API_KEY")
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")