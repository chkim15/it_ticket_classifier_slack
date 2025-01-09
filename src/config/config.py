import os
from dotenv import load_dotenv
from pathlib import Path

# Get the root directory and load environment variables
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(Path(ROOT_DIR, '.env'))

class Config:
    # Slack configs
    SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
    SLACK_SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET')
    SLACK_CLIENT_ID = os.getenv('SLACK_CLIENT_ID')
    SLACK_CLIENT_SECRET = os.getenv('SLACK_CLIENT_SECRET')

    # Snowflake configs
    SNOWFLAKE_USER = os.getenv('SNOWFLAKE_USER')
    SNOWFLAKE_PASSWORD = os.getenv('SNOWFLAKE_PASSWORD')
    SNOWFLAKE_ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT')
    SNOWFLAKE_WAREHOUSE = os.getenv('SNOWFLAKE_WAREHOUSE')
    SNOWFLAKE_DATABASE = os.getenv('SNOWFLAKE_DATABASE')
    SNOWFLAKE_SCHEMA = os.getenv('SNOWFLAKE_SCHEMA')