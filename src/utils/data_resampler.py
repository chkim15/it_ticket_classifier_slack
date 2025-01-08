import pandas as pd
import numpy as np
from collections import Counter
from sklearn.preprocessing import LabelEncoder
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import SMOTE
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class DataResampler:
    def __init__(self, data_dir=None, upsampling_num=45000, downsampling_num=25000):
        self.data_dir = data_dir or Path('data/processed')
        self.upsampling_num = upsampling_num
        self.downsampling_num = downsampling_num
        self.label_encoder = LabelEncoder()

    def load_data(self):
        """Load data from processed directory."""
        try:
            logger.info("Loading base DataFrame...")
            df_path = self.data_dir / 'snowflake_embedding_less_asterisk_cleaned.csv'
            df = pd.read_csv(df_path)
            
            logger.info("Loading embeddings...")
            embeddings_path = self.data_dir / 'multilingual_embeddings.npy'
            embeddings = np.load(embeddings_path)
            
            logger.info("Combining data...")
            df['MULTILINGUAL_E5LARGE_EMBEDDING'] = list(embeddings)
            
            return df
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")

    def resample_data(self, df):
        """Perform downsampling of OTHER class and upsampling of minority classes."""
        logger.info("Starting resampling process...")
        
        # Extract features and target
        logger.info("Extracting features and target...")
        X = np.vstack(df['MULTILINGUAL_E5LARGE_EMBEDDING'].values)
        Y = df['SIMPLIFIED_CATEGORY'].values

        # Print original distribution
        original_counts = df['SIMPLIFIED_CATEGORY'].value_counts().to_dict()
        logger.info(f"Original class distribution: {original_counts}")

        # Downsample 'OTHER' class
        logger.info(f"Downsampling 'OTHER' class to {self.downsampling_num} samples...")
        rus = RandomUnderSampler(
            sampling_strategy={'OTHER': self.downsampling_num}, 
            random_state=42
        )
        X_res, y_res = rus.fit_resample(X, Y)
        logger.info("Downsampling completed.")

        # Separate 'OTHER' and minority classes
        logger.info("Separating 'OTHER' and minority classes...")
        other_indices = [i for i, label in enumerate(y_res) if label == 'OTHER']
        minority_indices = [i for i, label in enumerate(y_res) if label != 'OTHER']

        X_other = X_res[other_indices]
        y_other = y_res[other_indices]
        X_minority = X_res[minority_indices]
        y_minority = y_res[minority_indices]

        # Calculate desired counts for SMOTE
        logger.info("Calculating SMOTE sampling strategy...")
        other_classes_counts = {k: v for k, v in original_counts.items() if k != 'OTHER'}
        scaling_factor = self.upsampling_num / sum(other_classes_counts.values())
        desired_counts = {
            label: int(count * scaling_factor) 
            for label, count in other_classes_counts.items()
        }

        # Apply SMOTE to minority classes
        logger.info("Applying SMOTE to minority classes...")
        smote = SMOTE(
            sampling_strategy={
                label: desired_counts[label] 
                for label in Counter(y_minority).keys()
            },
            random_state=42
        )
        X_minority_resampled, y_minority_resampled = smote.fit_resample(X_minority, y_minority)
        logger.info("SMOTE completed.")

        # Combine resampled data
        logger.info("Combining resampled data...")
        X_balanced = np.vstack((X_other, X_minority_resampled))
        y_balanced = np.concatenate((y_other, y_minority_resampled))

        # Print final distribution
        balanced_counts = Counter(y_balanced)
        logger.info(f"Final class distribution: {dict(balanced_counts)}")

        return X_balanced, y_balanced

    def save_resampled_data(self, X_balanced, y_balanced, save_dir=None):
        """Save resampled data to disk."""
        save_dir = save_dir or self.data_dir / 'resampled'
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)

        try:
            logger.info("Saving resampled features...")
            np.save(save_dir / 'X_balanced.npy', X_balanced)
            
            logger.info("Saving resampled labels...")
            np.save(save_dir / 'y_balanced.npy', y_balanced)
            
            logger.info("Saving metadata...")
            metadata = {
                'X_shape': X_balanced.shape,
                'y_shape': y_balanced.shape,
                'class_distribution': dict(Counter(y_balanced)),
                'upsampling_num': self.upsampling_num,
                'downsampling_num': self.downsampling_num,
                'timestamp': pd.Timestamp.now().isoformat()
            }
            
            pd.DataFrame([metadata]).to_json(
                save_dir / 'resampling_metadata.json',
                orient='records'
            )
            
            logger.info(f"All data saved to: {save_dir}")
            return save_dir
        except Exception as e:
            raise Exception(f"Error saving resampled data: {str(e)}")