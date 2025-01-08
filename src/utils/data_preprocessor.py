import pandas as pd
import re

def clean_conversation_messages(df):
    """Clean conversation messages by removing Out messages and In:., prefix."""
    df = df.copy()
    # Remove anything that comes after "Out:.,"
    df['CONVERSATION_MESSAGES'] = df['CONVERSATION_MESSAGES'].str.split('Out:.,').str[0]
    
    # Delete "In:., "
    df['CONVERSATION_MESSAGES'] = df['CONVERSATION_MESSAGES'].str.replace('In:.,', '')
    
    # Replace '\n， \r' with space
    df['CONVERSATION_MESSAGES'] = df['CONVERSATION_MESSAGES'].apply(
        lambda x: re.sub(r'\n|\r', ' ', x) if isinstance(x, str) else x
    )
    
    return df

def filter_short_conversations(df, min_words=10):
    """Remove conversations with fewer than min_words words."""
    return df[df['CONVERSATION_MESSAGES']
              .str.replace(r'[^\w\s]', '', regex=True)
              .str.split()
              .str.len() >= min_words]

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