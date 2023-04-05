from dotenv import dotenv_values

config = dotenv_values('.env')

# \\\\\\\\\\\\\\\ DATABASE \\\\\\\\\\\\\\\\\\\

DB_NAME = config['DATABASE_NAME']
DB_HOST = config['DATABASE_HOST']
DB_USERNAME = config['DATABASE_USERNAME']
DB_PASSWORD = config['DATABASE_PASSWORD']
DB_DRIVER = config['DATABASE_DRIVER']
DB_URL = f"{DB_DRIVER}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# \\\\\\\\\\\\\\\\\ AUTH \\\\\\\\\\\\\\\\\\\\\\\\\

IGDB_CLIENT_ID = config['IGDB_CLIENT_ID']
IGDB_CLIENT_SECRET = config['IGDB_CLIENT_SECRET']
IGDB_ACCESS_TOKEN = config['IGDB_ACCESS_TOKEN']