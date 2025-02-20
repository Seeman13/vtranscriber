import os
from dotenv import load_dotenv

load_dotenv()

API_URL=os.getenv('API_URL')
GPT_API_KEY = os.getenv('GPT_API_KEY')
GPT_CONDITION = os.getenv('GPT_CONDITION')
GPT_CONDITION2 = os.getenv('GPT_CONDITION2')
GPT_MAX_TOKENS = int(os.getenv('GPT_MAX_TOKENS', 3000))
GPT_MODEL = os.getenv('GPT_MODEL', 'gpt-4')
