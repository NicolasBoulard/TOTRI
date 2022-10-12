from os import environ
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    TELEGRAM_API_KEY = environ.get("TELEGRAM_API_KEY")
    TOTAL_API_URL = environ.get("TOTAL_API_URL")
