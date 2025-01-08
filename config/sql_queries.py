INITIAL_CLEAN_QUERY = """
CREATE TABLE IF NOT EXISTS CLEAN_DATA_Final as( 
WITH first_messages AS (
    -- Identify the first message in each conversation
    SELECT 
        CONVERSATION_ID,
        MESSAGE_ID,
        MESSAGE,
        MESSAGE_DIRECTION,
        SENT_AT,
        ROW_NUMBER() OVER (PARTITION BY CONVERSATION_ID ORDER BY SENT_AT ASC) AS row_num
    FROM class_shared_data.class_dataset.message_dataset
),
[... rest of your SQL query ...]
"""

FETCH_CLEAN_DATA_QUERY = "select * from CLEAN_DATA_Final"