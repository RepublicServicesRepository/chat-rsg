from app.agents.tools.rsg.common.kb import KB
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#function to retrieve relavant conetnt from KB for a given input and topic
def retrieve_jeff(topic,input):    

    max_tokens = os.environ.get("ASK_JEFF_KB_MAX_TOKENS")
    if max_tokens is None:
        max_tokens = 512
    else:
        max_tokens = int(max_tokens)

    kb_temperature = os.environ.get("ASK_JEFF_KB_TEMPERATURE")
    if kb_temperature is None:
        kb_temperature = 0.4
    else:
        kb_temperature = float(kb_temperature)

    kb_top_p = os.environ.get("ASK_JEFF_KB_TOP_P")
    if kb_top_p is None:
        kb_top_p = 0.98
    else:
        kb_top_p = float(kb_top_p)

    max_search_results = os.environ.get("ASK_JEFF_KB_MAX_SEARCH_RESULTS")
    if max_search_results is None:
        max_search_results = 10
    else:
        max_search_results = int(max_search_results)

    #initialize the KB
    kb = KB(region=os.environ.get("ASK_JEFF_KB_REGION"),
            kb_id=os.environ.get("ASK_JEFF_KB_ID"),
            kb_params={
                "maxTokens": max_tokens,
                "temperature": kb_temperature,
                "topP": kb_top_p
            },
            max_search_results = max_search_results
    )
    
    logger.info("KB Initialized")
    
    topic_filter = {
        "equals": {
            "key": "topic",
            "value": topic
        }
    }
    
    items = kb.filter_and_retrieve(input,topic_filter)

    chunks = []
    for item in items["retrievalResults"]:
        chunks.append(item['content']['text'])

    return chunks
     