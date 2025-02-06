from app.agents.tools.rsg.common.kb import KB
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#function to retrieve relavant conetnt from KB for a given KMT item
def retrieve_item(item,division_number, polygon_id,div_level_polygon_id):    

    max_tokens = os.environ.get("KB_MAX_TOKENS")
    if max_tokens is None:
        max_tokens = 512
    else:
        max_tokens = int(max_tokens)

    kb_temperature = os.environ.get("KB_TEMPERATURE")
    if kb_temperature is None:
        kb_temperature = 0.4
    else:
        kb_temperature = float(kb_temperature)

    kb_top_p = os.environ.get("KB_TOP_P")
    if kb_top_p is None:
        kb_top_p = 0.98
    else:
        kb_top_p = float(kb_top_p)

    max_search_results = os.environ.get("KB_MAX_SEARCH_RESULTS")
    if max_search_results is None:
        max_search_results = 10
    else:
        max_search_results = int(max_search_results)

    #initialize the KB
    kb = KB(region=os.environ.get("KB_REGION"),
            kb_id=os.environ.get("KB_ID"),
            kb_params={
                "maxTokens": max_tokens,
                "temperature": kb_temperature,
                "topP": kb_top_p
            },
            max_search_results = max_search_results
    )
    
    logger.info("KB Initialized")

    kb_input = get_kb_item_input(item) #item is the item to be searched
    logger.info("KB Input: " + kb_input)
    kb_metadata_filter = get_kb_item_metadata_filter(division_number,polygon_id,div_level_polygon_id)
    
    items = kb.retrieve(kb_input,kb_metadata_filter)

    chunks = []
    for item in items["retrievalResults"]:
        chunks.append(item['content']['text'])

    return chunks
 
def get_kb_item_input(item):

    #TODO externalize this
    return f"Answer these questions for this item: {item}. \
            - Does the item qualify for pickup based on the given categories or similar items? Consider size and weight. \
            - Are there any weight and dimensions mentioned for the item? \
            - What is the service limit for this item? \
            - When does the disposal service occur, and what is the frequency? \
            - Is scheduling in advance required for disposal service? \
            - Is prepayment required for the disposal service? Answer Yes or No. \
            - How should the item be prepared for disposal? \
            - What are the specific charges or fees for disposal? "
       
#for filtering the KB search. Use Polygn level doc (Muni) ans DIV level doc (DIV)
def get_kb_item_metadata_filter(division_number,polygon_id,div_level_polygon_id):
    #TODO externalize this
    return {
                'orAll': [
                    {
                        'equals': {
                            'key': 'polygon_id',
                            'value': polygon_id
                        }
                    },
                    {
                        'andAll': [
                            {
                                'equals': {
                                    'key': 'division_number',
                                    'value': division_number 
                                }
                            },
                            {
                            'equals': {
                                    'key': 'polygon_id',
                                    'value': div_level_polygon_id 
                                },
                            }
                        ]
                    }
                ]
        }