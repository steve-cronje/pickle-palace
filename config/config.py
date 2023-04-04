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

SECRET_KEY = config['SECRET_KEY']
ALGORITHM = config['ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = int(config['ACCESS_TOKEN_EXPIRE_MINUTES'])