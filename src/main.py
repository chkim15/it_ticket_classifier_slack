from pathlib import Path
import logging
import sys

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from src.api.app import app
from src.config.config import Config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("Starting IT Ticket Classification Service...")
        
        # Log configuration details
        logger.info("Checking configurations...")
        if not Config.SLACK_BOT_TOKEN:
            raise ValueError("SLACK_BOT_TOKEN not found in environment variables")
        if not Config.SLACK_SIGNING_SECRET:
            raise ValueError("SLACK_SIGNING_SECRET not found in environment variables")
        
        # Check if model files exist
        model_path = Path('data/models/lightgbm_model.pkl')
        encoder_path = Path('data/models/label_encoder.pkl')
        
        if not model_path.exists():
            raise FileNotFoundError("Model file not found. Please ensure model is trained and saved.")
        if not encoder_path.exists():
            raise FileNotFoundError("Label encoder file not found. Please ensure model is trained and saved.")
        
        logger.info("All checks passed. Starting Flask application...")
        
        # Run the Flask app
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True
        )

    except Exception as e:
        logger.error(f"Error starting service: {str(e)}")
        raise

if __name__ == "__main__":
    main()