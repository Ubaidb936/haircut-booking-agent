import os
from dotenv import load_dotenv
                                                                                                                                                                
load_dotenv() 

class Settings:
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
settings = Settings()