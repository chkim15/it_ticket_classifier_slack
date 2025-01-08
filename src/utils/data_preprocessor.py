import pandas as pd
import re
from pathlib import Path

class DataPreprocessor:
    def __init__(self):
        self.root_dir = Path(__file__).resolve().parent.parent.parent

    def preprocess_data(self, df):
        """Main preprocessing function that runs all steps."""
        df = self.clean_conversation_messages(df)
        df = self.filter_short_conversations(df)
        df = self.add_simplified_categories(df)
        df = self.process_triage_messages(df)
        return df

    def clean_conversation_messages(self, df):
        df = df.copy()
        df['CONVERSATION_MESSAGES'] = (df['CONVERSATION_MESSAGES']
            .str.split('Out:.,').str[0]
            .str.replace('In:.,', '')
            .apply(lambda x: re.sub(r'\n|\r', ' ', x) if isinstance(x, str) else x))
        return df

    def filter_short_conversations(self, df, min_words=10):
        return df[df['CONVERSATION_MESSAGES']
                 .str.replace(r'[^\w\s]', '', regex=True)
                 .str.split()
                 .str.len() >= min_words]

    def add_simplified_categories(self, df):
        # Read category mapping
        category_file = self.root_dir / 'data' / 'simplified_categories.xlsx'
        df_categories = pd.read_excel(category_file)
        df_categories = df_categories[['AGENT_LABELED_CATEGORY', 'SIMPLIFIED_CATEGORY']]
        df_categories['SIMPLIFIED_CATEGORY'] = (df_categories['SIMPLIFIED_CATEGORY']
            .fillna('OTHER')
            .replace('Unknown', 'OTHER'))
        
        # Merge with main dataframe
        df = pd.merge(df, df_categories, on='AGENT_LABELED_CATEGORY', how='left')
        return df[['CONVERSATION_ID', 'CONVERSATION_CHANNEL', 'AGENT_LABELED_APPLICATION',
                  'TRIAGE_MESSAGES', 'AGENT_LABELED_CATEGORY', 'SIMPLIFIED_CATEGORY', 
                  'CONVERSATION_MESSAGES']]

    def process_triage_messages(self, df):
        df['Extracted_TRIAGE'] = df['TRIAGE_MESSAGES'].apply(self._extract_triage_info)
        df['MESSAGE_PLUS_TRIAGE'] = df['Extracted_TRIAGE'] + ' ' + df['CONVERSATION_MESSAGES']
        return df

    def extract_triage_info(text):
        """Extract relevant information from TRIAGE_MESSAGES."""
        if not isinstance(text, str) or text == '':
            return ''
        
        # Extract from first type
        if '**Request type**' in text:
            request_type_match = re.search(r'\*\*Request type\*\*\n (.+)', text)
            additional_details_match = re.search(r'\*\*Additional details\*\*\n (.+)', text)
            request_type = request_type_match.group(1) if request_type_match else ''
            additional_details = additional_details_match.group(1) if additional_details_match else ''
            return f"My request type is {request_type}, There are some additional detail which is {additional_details}"
        
        # Extract from second type
        elif '**What can we help you with?**' in text:
            help_match = re.search(r'\*\*What can we help you with\?\*\*\n (.+)', text)
            assistance_match = re.search(r'\*\*What do you need assistance with\?\*\*\n (.+)', text)
            additional_details_match = re.search(r'\*\*Additional details\*\*\n (.+)', text)
            help_info = help_match.group(1) if help_match else ''
            assistance_info = assistance_match.group(1) if assistance_match else ''
            additional_details = additional_details_match.group(1) if additional_details_match else ''
            return f"I want you to help me with {help_info}. I want you to assist me with {assistance_info}. There are some additional details that {additional_details}"
        
        return ''