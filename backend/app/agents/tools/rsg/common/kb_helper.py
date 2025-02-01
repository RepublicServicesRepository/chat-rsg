from app.agents.tools.rsg.lib.kb import KB
import os

#function to retrieve relavant conetnt from KB for a given KMT item
def retrieve_item(item,division_number, polygon_id,div_level_polygon_id):    
 
    kb = KB(region=os.environ.get("KB_REGION"),
            kb_id=os.environ.get("KB_ID"),
            kb_params={
                "maxTokens": os.environ.get("KB_MAX_TOKENS"),
                "temperature": os.environ.get("KB_TEMPERATURE"),
                "topP": os.environ.get("KB_TOP_P")
            },
            max_search_results = os.environ.get("KB_MAX_SEARCH_RESULTS")
    )
    
    kb_input = get_kb_item_input(item) #item is the item to be searched
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