> 📖 Check out the detailed blog post on Medium to learn more!

[![Read Full Article](https://img.shields.io/badge/📖%20Medium-From%20Data%20to%20Automation:%20Revolutionizing%20IT%20Support-black?style=for-the-badge&logo=medium)](https://medium.com/analytics-in-action-columbia-business-school/from-data-to-automation-revolutionizing-it-support-at-electric-4661ab08cf57)

# IT Ticket Classification with Slack Integration

Advanced ML pipeline for automating IT support ticket categorization with Slack Integration.

## Project Overview

Built an end-to-end machine learning system that:

* Automatically classifies IT support tickets into 8 categories
* Achieves 83% precision and 96% precision@2 (correct category in top 2 predictions)
* Trained on 500K+ historical tickets
* Integrates with Slack for real-time classification

## Implementation Journey

### Project Workflow

![Workflow Diagram](assets/workflow.svg)

#### Project Structure

```
.
├── src/
│   ├── api/
│   │   ├── services/
│   │   │   ├── prediction.py      # Prediction logic
│   │   │   └── slack_handler.py   # Slack integration
│   │   └── app.py                 # Flask application
│   ├── models/
│   │   └── trainer.py             # Model training
│   └── utils/
│       ├── data_preprocessor.py   # Data cleaning
│       ├── data_resampler.py      # Class balancing
│       └── data_validator.py      # Filter validated data
│       └── snowflake_connector.py # Database connections
├── data/
│   └── processed/                 # Processed data
├── tests/
│   ├── test_resampler.py
│   └── test_model.py
│   └── test_api.py
├── config/
│   ├── sql_queries.py
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_data_preprocessin.ipynb
│   ├── 03_data_resampling.ipynb
│   ├── 04_build_model.ipynb
│   ├── 05_fine_tuning_lightgbm.ipynb
│   ├── 06_add_threshold.ipynb
├── requirements.txt
└── README.md
```

### 1. Data Pipeline Development

#### Initial Setup & Data Collection

* Connected to Snowflake data warehouse
* Created SQL queries to filter and clean ticket data
* Implemented conversation message handling

#### Feature Engineering

* Generated embeddings using Snowflake's multilingual-e5-large model
* Combined ticket messages with triage information
* Filtered heavily masked data (>20% threshold)

### 2. Model Development

#### Data Resampling

Implemented hybrid resampling strategy:

* Undersampled 'OTHER' class to 25,000 samples
* SMOTE upsampling to 45,000 total samples
* Maintained class distribution integrity

#### Model Training

* Selected LightGBM for final implementation
* Achieved 83% precision, 96% precision@2

#### Performance & Impact

##### Technical Metrics

* Model Precision: 83%
* Precision@2: 96%
* Response Time: < 1 second

##### Business Impact

* Potential cost reduction of $180k/month
* 80% reduction in response time
* Automated categorization

### 3. Future Work

#### Technical Improvements

* Model versioning
* Real-time monitoring
* Automated retraining


## Appendix

### Slack Integration Guide 

#### 1. Slack App Setup
##### Create Slack App
1. Go to `https://api.slack.com/apps`
2. Click "Create New App"
3. Choose "From scratch"
4. Name your app and select workspace

##### Configure Bot Permissions
Under "OAuth & Permissions":
1. Add Bot Token Scopes:
    * chat:write        (Send messages)
    * im:history        (View DM history)  
    * channels:history  (View channel messages)
    * im:write         (Send DMs)
2. Install app to workspace
3. Save Bot User OAuth Token (starts with `xoxb-`)

##### Enable Interactivity
1. Go to "Interactivity & Shortcuts"
2. Turn on Interactivity
3. Add Request URL: `https://your-domain/slack/actions`
4. Save Changes

##### Configure Event Subscriptions
1. Go to "Event Subscriptions"
2. Turn on "Enable Events" 
3. Add Request URL: `https://your-domain/slack/events`
4. Subscribe to bot events:
    * message.im
    * message.channels

#### 2. Core Components

##### Environment Setup
Store these in `.env`: 
* SLACK_BOT_TOKEN=xoxb-your-token 
* SLACK_CLIENT_ID=your-client-id 
* SLACK_CLIENT_SECRET=your-client-secret 
* SLACK_SIGNING_SECRET=your-signing-secret 

##### Key Components
1. Slack Handler (`src/api/services/slack_handler.py`)
   - Manages Slack client connection
   - Formats interactive messages
   - Handles message processing

2. Flask Routes (`src/api/app.py`)
   - /slack/events: Handles incoming messages
   - /slack/actions: Processes button clicks

#### 3. Message Flow
1. User sends message → Slack → `/slack/events`
2. Backend:
   * Processes message using `PredictionService`
   * Formats interactive response
   * Sends back to Slack
3. User clicks button → Slack → `/slack/actions`
4. Backend responds based on user choice

#### 4. Local Development
```bash
# Terminal 1: Start Flask
python src/api/app.py

# Terminal 2: Start ngrok
ngrok http 5000
```
