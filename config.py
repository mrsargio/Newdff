import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram API Configuration
    API_ID = int(os.getenv('24250238', 0))
    API_HASH = os.getenv('cb3f118ce5553dc140127647edcf3720', '')
    BOT_TOKEN = os.getenv('6047785902:AAE59KTfmhRvF8sUSYIzl9wcGnm4FLXiWDk', '')
    
    # Bot Configuration
    ADMIN_IDS = [int(x) for x in os.getenv('6175650047', '').split(',') if x]
