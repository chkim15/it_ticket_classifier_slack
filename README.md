# IT Ticket Classification System
Advanced ML pipeline for automating IT support ticket categorization using Snowflake embeddings and LightGBM.

## Project Overview
Built an end-to-end machine learning system that:
- Automatically classifies IT support tickets into 8 categories
- Achieves 83% precision and 96% precision@2 (correct category in top 2 predictions)
- Trained on 500K+ historical tickets
- Integrates with Slack for real-time classification

## Technical Implementation

### Data Pipeline Architecture
1. **Data Collection & Preprocessing**
   - Snowflake data warehouse integration
   - Custom SQL queries for filtering valid tickets
   - Intelligent message cleaning (removing system messages, handling special characters)
   - Robust handling of multi-turn conversations

2. **Feature Engineering**
   - multilingual-e5-large embeddings (1024-dimensional vectors)
   - Ticket message + triage information combined representation
   - Handles both chat and email formats
   - Filters out heavily masked data (>20% masking ratio)

3. **Class Balancing**
   - Hybrid resampling approach:
     * Undersampling majority class (OTHER) to 25,000 samples
     * SMOTE upsampling minority classes to 45,000 total
   - Maintains class distribution integrity
   - Prevents information loss from aggressive downsampling

### Model Architecture
1. **Core Model**: LightGBM Classifier

2. **Performance Metrics**
   - Precision: 83%
   - Precision@2: 96%

### Tech Stack & Infrastructure
```
Data Processing:
- Python 3.10
- Pandas & NumPy
- Snowflake Connector

Machine Learning:
- LightGBM (GPU-enabled)
- scikit-learn
- imblearn

Deployment:
- Flask API
- Slack Bot Integration
- Docker
```

## Project Structure
```
.
├── src/
│   ├── models/
│   │   └── trainer.py          # LightGBM model implementation
│   ├── utils/
│   │   ├── data_preprocessor.py  # Data cleaning & preprocessing
│   │   ├── data_resampler.py     # Class balancing logic
│   │   └── snowflake_connector.py # Database operations
│   └── main.py                  # Pipeline orchestration
├── data/
│   └── processed/              # Processed embeddings & models
├── tests/
│   ├── test_resampler.py
│   └── test_model.py
├── requirements.txt
└── README.md
```

## Key Features & Business Impact
1. **Automated Classification**
   - Real-time ticket categorization
   - Handles 8 distinct ticket categories
   - Graceful handling of edge cases

2. **Production Readiness**
   - Modular, maintainable code architecture
   - Comprehensive logging system
   - Robust error handling
   - GPU acceleration support

3. **Performance Optimization**
   - Efficient memory management for large embeddings
   - Optimized data preprocessing pipeline
   - Scalable class balancing approach

4. **Business Value**
   - 80% reduction in initial response time
   - Improved ticket routing accuracy
   - Reduced manual categorization effort
   - Enhanced service level agreement (SLA) compliance

## Future Roadmap
1. **Technical Improvements**
   - Model versioning system
   - A/B testing framework
   - Real-time monitoring dashboard
   - Automated retraining pipeline

2. **Feature Extensions**
   - Multi-label classification support
   - Additional language support
   - Custom embedding fine-tuning
   - Confidence threshold optimization
