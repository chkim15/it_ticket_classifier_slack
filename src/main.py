from utils.snowflake_connector import SnowflakeConnector
from utils.data_preprocessor import DataPreprocessor
from config.sql_queries import INITIAL_CLEAN_QUERY, FETCH_CLEAN_DATA_QUERY, CREATE_EMBEDDINGS_QUERY
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # Initialize connections and processors
        logger.info("Initializing Snowflake connection and data preprocessor...")
        snow_conn = SnowflakeConnector()
        preprocessor = DataPreprocessor()

        # Create initial clean data table
        logger.info("Creating clean data table in Snowflake...")
        snow_conn.execute_query(INITIAL_CLEAN_QUERY)

        # Fetch the clean data
        logger.info("Fetching clean data from Snowflake...")
        combined_data = snow_conn.execute_query(FETCH_CLEAN_DATA_QUERY)

        # Preprocess the data
        logger.info("Preprocessing data...")
        processed_data = preprocessor.preprocess_data(combined_data)

        # Write processed data back to Snowflake
        logger.info("Writing processed data back to Snowflake...")
        snow_conn.write_to_snowflake(processed_data, "CLEAN_DATA_10WORDS_FINAL")

        # Create embeddings
        logger.info("Creating Snowflake embeddings...")
        snow_conn.execute_query(CREATE_EMBEDDINGS_QUERY)

        logger.info("Processing completed successfully!")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise
    finally:
        snow_conn.close()

if __name__ == "__main__":
    main()