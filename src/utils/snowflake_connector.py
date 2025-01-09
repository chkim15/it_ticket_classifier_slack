import os
from dotenv import load_dotenv
import snowflake.connector
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas
from pathlib import Path

class SnowflakeConnector:
    def __init__(self):
        ROOT_DIR = Path(__file__).resolve().parent.parent.parent
        load_dotenv(Path(ROOT_DIR, '.env'))
        self.conn = self._get_connection()

    def _get_connection(self):
        return snowflake.connector.connect(
            user=os.getenv('SNOWFLAKE_USER'),
            password=os.getenv('SNOWFLAKE_PASSWORD'),
            account=os.getenv('SNOWFLAKE_ACCOUNT'),
            warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
            database=os.getenv('SNOWFLAKE_DATABASE'),
            schema=os.getenv('SNOWFLAKE_SCHEMA')
        )

    def execute_query(self, query, params=None):
        """Execute a SQL query with optional parameters."""
        try:
            cur = self.conn.cursor()
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
                
            if cur.description:  # If query returns results
                results = cur.fetchall()
                column_names = [desc[0] for desc in cur.description]
                return pd.DataFrame(results, columns=column_names)
            return None
        
        finally:
            cur.close()

    def write_to_snowflake(self, df, table_name):
        """Write pandas DataFrame to Snowflake table."""
        return write_pandas(self.conn, df, table_name, auto_create_table=True)

    def close(self):
        self.conn.close()