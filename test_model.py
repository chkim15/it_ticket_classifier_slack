from src.utils.data_resampler import DataResampler
from src.models.trainer import ModelTrainer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_model_training():
    try:
        # Load and resample data
        logger.info("Loading and resampling data...")
        resampler = DataResampler()
        df = resampler.load_data()
        X_balanced, y_balanced = resampler.resample_data(df)
        
        # Initialize trainer
        trainer = ModelTrainer(use_gpu=False)  
        
        # Prepare data
        X_train, X_test, y_train, y_test = trainer.prepare_data(
            X_balanced, 
            y_balanced,
            resampler.label_encoder
        )
        
        # Train model
        trainer.train(X_train, y_train)
        
        # Evaluate model
        metrics = trainer.evaluate(X_test, y_test)
        
        # Save model
        trainer.save_model()
        
        logger.info("Training pipeline completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during model training: {str(e)}")
        raise

if __name__ == "__main__":
    test_model_training()