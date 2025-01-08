from utils.snowflake_connector import SnowflakeConnector
from utils.data_preprocessor import DataPreprocessor
from utils.data_resampler import DataResampler
from models.trainer import ModelTrainer
from config.sql_queries import (INITIAL_CLEAN_QUERY, FETCH_CLEAN_DATA_QUERY, 
                              CREATE_EMBEDDINGS_QUERY)
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    try:
        # Step 1: Initial Data Processing
        logger.info("Step 1: Initial Data Processing")
        snow_conn = SnowflakeConnector()
        preprocessor = DataPreprocessor()

        # Create initial clean data table in Snowflake
        logger.info("Creating clean data table in Snowflake...")
        snow_conn.execute_query(INITIAL_CLEAN_QUERY)

        # Fetch clean data
        logger.info("Fetching clean data...")
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

        # Step 2: Data Resampling
        logger.info("\nStep 2: Data Resampling")
        resampler = DataResampler()
        
        # Load processed data
        logger.info("Loading processed data...")
        df = resampler.load_data()
        
        # Perform resampling
        logger.info("Performing resampling...")
        X_balanced, y_balanced = resampler.resample_data(df)
        
        # Save resampled data
        logger.info("Saving resampled data...")
        resampler.save_resampled_data(X_balanced, y_balanced)

        # Step 3: Model Training
        logger.info("\nStep 3: Model Training")
        trainer = ModelTrainer(use_gpu=False)  # Set to True if GPU is available
        
        # Prepare data for training
        logger.info("Preparing training data...")
        X_train, X_test, y_train, y_test = trainer.prepare_data(
            X_balanced, 
            y_balanced,
            resampler.label_encoder
        )
        
        # Train model
        logger.info("Training model...")
        trainer.train(X_train, y_train)
        
        # Evaluate model
        logger.info("Evaluating model...")
        metrics = trainer.evaluate(X_test, y_test)
        
        # Save model
        logger.info("Saving model...")
        trainer.save_model()

        logger.info("\nEntire pipeline completed successfully!")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise
    finally:
        snow_conn.close()

if __name__ == "__main__":
    main()