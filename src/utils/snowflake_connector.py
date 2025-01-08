import os
from dotenv import load_dotenv
import snowflake.connector
from pathlib import Path

# Get the root directory and load environment variables
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(Path(ROOT_DIR, '.env'))

def get_snowflake_connection():
    """Create and return a Snowflake connection using environment variables."""
    try:
        conn = snowflake.connector.connect(
            user=os.getenv('SNOWFLAKE_USER'),
            password=os.getenv('SNOWFLAKE_PASSWORD'),
            account=os.getenv('SNOWFLAKE_ACCOUNT'),
            warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
            database=os.getenv('SNOWFLAKE_DATABASE'),
            schema=os.getenv('SNOWFLAKE_SCHEMA')
        )
        return conn
    except Exception as e:
        print(f"Error connecting to Snowflake: {str(e)}")
        raise

def execute_query(query):
    """Execute a SQL query and return results as a pandas DataFrame."""
    try:
        conn = get_snowflake_connection()
        cur = conn.cursor()
        cur.execute(query)
        results = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        cur.close()
        conn.close()
        return pd.DataFrame(results, columns=column_names)
    except Exception as e:
        print(f"Error executing query: {str(e)}")
        raise