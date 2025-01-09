# from slack_sdk import WebClient
# from slack_sdk.errors import SlackApiError
# from src.config.config import Config
# from src.api.services.prediction import PredictionService
# import logging

# logger = logging.getLogger(__name__)

# class SlackHandler:
#     def __init__(self):
#         self.client = WebClient(token=Config.SLACK_BOT_TOKEN)
#         self.prediction_service = PredictionService()

#     def handle_message(self, message_text, channel_id, thread_ts=None):
#         try:
#             # Get prediction
#             prediction_result = self.prediction_service.predict(message_text)
            
#             # Format response
#             response = self._format_prediction_response(prediction_result)
            
#             # Send response
#             self.client.chat_postMessage(
#                 channel=channel_id,
#                 text=response,
#                 thread_ts=thread_ts
#             )
            
#         except SlackApiError as e:
#             logger.error(f"Error sending message: {e.response['error']}")
#         except Exception as e:
#             logger.error(f"Error processing message: {str(e)}")

#     def _format_prediction_response(self, prediction_result):
#         predictions = prediction_result['predictions']
#         response = "I predict this ticket belongs to these categories:\n"
        
#         for i, pred in enumerate(predictions, 1):
#             probability_percentage = round(pred['probability'] * 100, 2)
#             response += f"{i}. {pred['category']} ({probability_percentage}% confidence)\n"
            
#         return response

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from src.config.config import Config
from src.api.services.prediction import PredictionService
import logging

logger = logging.getLogger(__name__)

class SlackHandler:
    def __init__(self):
        self.client = WebClient(token=Config.SLACK_BOT_TOKEN)
        self.prediction_service = PredictionService()  # Add this line

    def handle_message(self, message_text, channel_id, thread_ts=None):
        try:
            # Get prediction
            prediction_result = self.prediction_service.predict(message_text)
            
            # Format blocks for interactive message
            blocks = self._format_prediction_response(prediction_result)
            
            # Send response
            self.client.chat_postMessage(
                channel=channel_id,
                blocks=blocks,
                text="New ticket classification"
            )
            
        except SlackApiError as e:
            logger.error(f"Error sending message: {e.response['error']}")
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")

    def _format_prediction_response(self, prediction_result):
        predictions = prediction_result['predictions']
        top_prediction = predictions[0]  # Get the highest confidence prediction
        
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "It looks like you want to do the following. Is it correct?"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{top_prediction['category']}*\nConfidence: {round(top_prediction['probability'] * 100, 2)}%"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Yes",
                            "emoji": True
                        },
                        "style": "primary",
                        "action_id": "correct_classification"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Connect me to human agent",
                            "emoji": True
                        },
                        "style": "danger",
                        "action_id": "need_human"
                    }
                ]
            }
        ]
        
        return blocks