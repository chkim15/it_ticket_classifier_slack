import joblib
import numpy as np
from pathlib import Path
import snowflake.connector
from src.utils.snowflake_connector import SnowflakeConnector  # absolute import
import logging

logger = logging.getLogger(__name__)

class PredictionService:
    def __init__(self):
        self.model_dir = Path('data/models')
        self.model = joblib.load(self.model_dir / 'lightgbm_model.pkl')
        self.label_encoder = joblib.load(self.model_dir / 'label_encoder.pkl')
        self.snow_conn = SnowflakeConnector()

    def get_embedding(self, text):
        query = """
        SELECT SNOWFLAKE.CORTEX.EMBED_TEXT_1024(
            'multilingual-e5-large', 
            %s
        ) as embedding
        """
        result = self.snow_conn.execute_query(query, params=(text,))
        return np.array(result['EMBEDDING'].iloc[0])

    def predict(self, text):
        embedding = self.get_embedding(text)
        embedding = embedding.reshape(1, -1)
        
        # Get prediction probabilities
        proba = self.model.predict_proba(embedding)
        
        # Get top 2 predictions
        top_2_indices = np.argsort(proba[0])[-2:][::-1]
        predictions = self.label_encoder.inverse_transform(top_2_indices)
        probabilities = proba[0][top_2_indices]
        
        return {
            'predictions': [
                {'category': pred, 'probability': float(prob)}
                for pred, prob in zip(predictions, probabilities)
            ]
        }