import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN")
    GITHUB_API_BASE_URL : str = os.getenv("GITHUB_API_BASE_URL", "https://api.github.com")

settings = Settings()
