import numpy as np
from lightgbm import LGBMClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import logging
from pathlib import Path
import joblib

logger = logging.getLogger(__name__)

class ModelTrainer:
    def __init__(self, use_gpu=False):  # Default to CPU
        self.best_params = {
            'colsample_bytree': 0.7715490096744506,
            'learning_rate': 0.09741465956967921,
            'max_depth': 9,
            'min_child_samples': 37,
            'n_estimators': 169,
            'num_leaves': 90,
            'reg_alpha': 0.09536592999298432,
            'reg_lambda': 0.3981311006973933,
            'subsample': 0.946224464192131,
            'random_state': 42,
            'n_jobs': 1,
            'verbose': -1
        }
        
        # Add GPU parameters only if GPU is available
        if use_gpu:
            self.best_params.update({
                'device': 'gpu',
                'gpu_device_id': 0
            })
            
        self.model = None
        self.label_encoder = None

    def prepare_data(self, X_balanced, y_balanced, label_encoder=None):
        """Prepare data for training."""
        logger.info("Preparing data for training...")
        
        # Initialize and fit label encoder if not provided
        if label_encoder is None:
            self.label_encoder = LabelEncoder()
            y_balanced_encoded = self.label_encoder.fit_transform(y_balanced)
        else:
            self.label_encoder = label_encoder
            # Fit the encoder if it hasn't been fit yet
            if not hasattr(self.label_encoder, 'classes_'):
                y_balanced_encoded = self.label_encoder.fit_transform(y_balanced)
            else:
                y_balanced_encoded = self.label_encoder.transform(y_balanced)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_balanced, 
            y_balanced_encoded,
            test_size=0.2, 
            random_state=42, 
            stratify=y_balanced_encoded
        )
        
        # Convert to float32
        X_train = X_train.astype(np.float32)
        X_test = X_test.astype(np.float32)
        
        logger.info(f"Train set shape: {X_train.shape}")
        logger.info(f"Test set shape: {X_test.shape}")
        
        return X_train, X_test, y_train, y_test

    def train(self, X_train, y_train):
        """Train the model with best parameters."""
        logger.info("Starting model training with best parameters...")
        
        self.model = LGBMClassifier(**self.best_params)
        self.model.fit(X_train, y_train)
        
        logger.info("Model training completed")
        return self.model

    def evaluate(self, X_test, y_test):
        """Evaluate the model."""
        logger.info("Evaluating model...")
        
        y_pred = self.model.predict(X_test)
        
        # Convert labels back to original strings
        y_test_labels = self.label_encoder.inverse_transform(y_test)
        y_pred_labels = self.label_encoder.inverse_transform(y_pred)
        
        # Get classification report
        report_dict = classification_report(y_test_labels, y_pred_labels, output_dict=True)
        report_str = classification_report(y_test_labels, y_pred_labels)
        
        logger.info("Classification Report:")
        logger.info("\n" + report_str)
        
        return report_dict

    def save_model(self, save_dir=None):
        """Save the trained model and metadata."""
        save_dir = Path(save_dir or 'data/models')
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # Save model
        model_path = save_dir / 'lightgbm_model.pkl'
        joblib.dump(self.model, model_path)
        
        # Save label encoder
        encoder_path = save_dir / 'label_encoder.pkl'
        joblib.dump(self.label_encoder, encoder_path)
        
        logger.info(f"Model saved to: {model_path}")
        logger.info(f"Label encoder saved to: {encoder_path}")
        
        return save_dir