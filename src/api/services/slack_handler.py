from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from src.config.config import Config
from src.api.services.prediction import PredictionService
import logging

logger = logging.getLogger(__name__)

class SlackHandler:
    def __init__(self):
        self.client = WebClient(token=Config.SLACK_BOT_TOKEN)
        self.prediction_service = PredictionService()

    def handle_message(self, message_text, channel_id, thread_ts=None):
        try:
            # Get prediction
            prediction_result = self.prediction_service.predict(message_text)
            
            # Format response
            response = self._format_prediction_response(prediction_result)
            
            # Send response
            self.client.chat_postMessage(
                channel=channel_id,
                text=response,
                thread_ts=thread_ts
            )
            
        except SlackApiError as e:
            logger.error(f"Error sending message: {e.response['error']}")
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")

    def _format_prediction_response(self, prediction_result):
        predictions = prediction_result['predictions']
        response = "I predict this ticket belongs to these categories:\n"
        
        for i, pred in enumerate(predictions, 1):
            probability_percentage = round(pred['probability'] * 100, 2)
            response += f"{i}. {pred['category']} ({probability_percentage}% confidence)\n"
            
        return response