import os



class Config(object):
      BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
      API_ID = int(os.environ.get("APP_ID", 12345))
      API_HASH = os.environ.get("API_HASH")
      OMDB_API_KEY = os.environ.get("OMDB_API_KEY")
      DB_URL = os.environ.get("DATABASE_URL", "")
      if OMDB_API_KEY:
          key = OMDB_API_KEY
      else:
          key = None
