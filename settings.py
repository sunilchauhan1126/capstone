from dotenv import load_dotenv 
import os 
load_dotenv() 
DB_NAME = os.environ.get("DB_NAME") 
DB_USER = os.environ.get("DB_USER") 
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_CONN_STRING = os.environ.get("DB_CONN_STRING")
TEST_DB_NAME = os.environ.get("TEST_DB_NAME")

DB_NAME_RENDER = os.environ.get("DB_NAME_RENDER") 
DB_USER_RENDER = os.environ.get("DB_USER_RENDER") 
DB_PASSWORD_RENDER = os.environ.get("DB_PASSWORD_RENDER")
DB_CONN_STRING_RENDER = os.environ.get("DB_CONN_STRING_RENDER")

DATABASE_URL = os.environ.get("DATABASE_URL")
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
ALGORITHMS = os.environ.get("ALGORITHMS")
API_AUDIENCE = os.environ.get("API_AUDIENCE")

