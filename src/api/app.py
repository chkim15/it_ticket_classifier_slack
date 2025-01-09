# from flask import Flask, request, jsonify
# import sys
# from pathlib import Path

# # Add project root to Python path
# project_root = str(Path(__file__).parent.parent.parent)
# sys.path.append(project_root)

# from src.api.services.prediction import PredictionService
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# app = Flask(__name__)
# prediction_service = PredictionService()

# @app.route('/health', methods=['GET'])
# def health_check():
#     return jsonify({'status': 'healthy'})

# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         data = request.json
#         if 'text' not in data:
#             return jsonify({'error': 'No text provided'}), 400
            
#         result = prediction_service.predict(data['text'])
#         return jsonify(result)
        
#     except Exception as e:
#         logger.error(f"Prediction error: {str(e)}")
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)

from flask import Flask, request, jsonify
import sys
from pathlib import Path
import logging
import hmac
import hashlib
import json

# Add project root to Python path (keep this at the top)
project_root = str(Path(__file__).parent.parent.parent)
sys.path.append(project_root)

# Now import our modules after setting up the path
from src.api.services.prediction import PredictionService
from src.api.services.slack_handler import SlackHandler
from src.config.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
prediction_service = PredictionService()
slack_handler = SlackHandler()

def verify_slack_request():
    timestamp = request.headers.get('X-Slack-Request-Timestamp', '')
    signature = request.headers.get('X-Slack-Signature', '')
    
    # Create basestring
    basestring = f"v0:{timestamp}:{request.get_data(as_text=True)}"
    
    # Calculate signature
    my_signature = 'v0=' + hmac.new(
        Config.SLACK_SIGNING_SECRET.encode(),
        basestring.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(my_signature, signature)

@app.route('/slack/events', methods=['POST'])
def slack_events():
    logger.info("Received Slack event")
    logger.info(f"Request data: {request.get_data()}")
    logger.info(f"Request JSON: {request.json}")
    
    data = request.json
    
    # Handle URL verification challenge
    if data and 'type' in data and data['type'] == 'url_verification':
        challenge = data.get('challenge')
        logger.info(f"Received challenge: {challenge}")
        response = {'challenge': challenge}
        logger.info(f"Sending response: {response}")
        return jsonify(response)
    
    # Verify request is from Slack (only after verification)
    if not verify_slack_request():
        return jsonify({'error': 'Invalid request'}), 403
    
    # Handle message events
    if data['type'] == 'event_callback':
        event = data['event']
        if event['type'] == 'message' and 'bot_id' not in event:
            slack_handler.handle_message(
                message_text=event['text'],
                channel_id=event['channel'],
                thread_ts=event.get('thread_ts', event['ts'])
            )
    
    return jsonify({'status': 'ok'})

# Keep existing routes
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        if 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
            
        result = prediction_service.predict(data['text'])
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/test', methods=['GET'])
def test():
    return jsonify({'status': 'working'})

@app.route('/slack/actions', methods=['POST'])
def slack_actions():
    # Parse the request payload
    data = json.loads(request.form.get('payload'))
    
    action_id = data['actions'][0]['action_id']
    channel_id = data['channel']['id']
    user_id = data['user']['id']
    
    if action_id == 'correct_classification':
        slack_handler.client.chat_postMessage(
            channel=channel_id,
            text=f"Thanks! I'll process your request right away."
        )
    elif action_id == 'need_human':
        slack_handler.client.chat_postMessage(
            channel=channel_id,
            text=f"I'll connect you with a human agent shortly. <@{user_id}>"
        )
    
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')