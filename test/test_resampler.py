from src.utils.data_resampler import DataResampler
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_resampling():
    try:
        logger.info("Starting resampling test...")
        
        # Initialize resampler
        resampler = DataResampler()
        
        # Load data
        logger.info("Loading data from processed directory...")
        df = resampler.load_data()
        logger.info(f"Loaded data shape: {df.shape}")
        
        # Perform resampling
        logger.info("Starting resampling process...")
        X_balanced, y_balanced = resampler.resample_data(df)
        logger.info(f"Resampling completed!")
        logger.info(f"Final X shape: {X_balanced.shape}")
        logger.info(f"Final y shape: {y_balanced.shape}")
        
        # Save resampled data
        logger.info("Saving resampled data...")
        save_dir = resampler.save_resampled_data(X_balanced, y_balanced)
        logger.info(f"Saved resampled data to: {save_dir}")
        
    except Exception as e:
        logger.error(f"Error during testing: {str(e)}")
        raise

if __name__ == "__main__":
    test_resampling()