import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://sujankommalapati:sujan123@cluster0.jkt0l.mongodb.net/medibot')