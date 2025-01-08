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

CREATE_EMBEDDINGS_QUERY = """
CREATE TABLE SNOWFLAKE_EMBEDDING_TRIAGE_FINAL AS
select CONVERSATION_ID, SIMPLIFIED_CATEGORY, CONVERSATION_CHANNEL, MESSAGE_PLUS_TRIAGE,
SNOWFLAKE.CORTEX.EMBED_TEXT_1024('multilingual-e5-large', MESSAGE_PLUS_TRIAGE) as multilingual_e5large_embedding
from CLEAN_DATA_10WORDS_Final
"""

FETCH_EMBEDDINGS_QUERY = """
select * from SNOWFLAKE_EMBEDDING_TRIAGE_FINAL
"""

FETCH_VALIDATED_DATA_QUERY = """
select * from class_shared_data.class_dataset.conversation_dataset
"""