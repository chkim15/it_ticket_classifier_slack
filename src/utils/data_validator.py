import pandas as pd
import numpy as np
from pathlib import Path

class DataValidator:
    def __init__(self, output_dir=None):
        self.output_dir = output_dir or Path('data/processed')
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def process_embeddings(self, embedding_df, conversation_df):
        """Process and validate the embeddings data."""
        # Filter conversation data
        conversation_df = conversation_df[['CONVERSATION_ID', 'VALIDATED_CATEGORY']]

        # Merge datasets
        df = pd.merge(embedding_df, conversation_df, on='CONVERSATION_ID', how='left')
        
        # Filter validated categories
        df = df[(df['VALIDATED_CATEGORY'] == True) | (df['SIMPLIFIED_CATEGORY'] == 'OTHER')]
        
        # Filter out heavily masked data
        df = df[df['MESSAGE_PLUS_TRIAGE'].str.count(r'\*') < (0.2 * df['MESSAGE_PLUS_TRIAGE'].str.len())]
        
        # Convert embeddings to numpy array
        df['MULTILINGUAL_E5LARGE_EMBEDDING'] = df['MULTILINGUAL_E5LARGE_EMBEDDING'].apply(
            lambda x: np.array(x, dtype=np.float32)
        )
        
        return df

    def save_processed_data(self, df):
        """Save the processed data and embeddings."""
        # Save embeddings
        embeddings_path = self.output_dir / 'multilingual_embeddings.npy'
        np.save(embeddings_path, np.stack(df['MULTILINGUAL_E5LARGE_EMBEDDING'].values))
        
        # Save DataFrame without embeddings
        csv_path = self.output_dir / 'snowflake_embedding_less_asterisk_cleaned.csv'
        df.drop(columns=['MULTILINGUAL_E5LARGE_EMBEDDING']).to_csv(csv_path, index=False)
        
        return embeddings_path, csv_path