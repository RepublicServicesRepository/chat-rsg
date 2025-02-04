import json
import logging

from app.agents.tools.base import  StructuredTool
from langchain_core.pydantic_v1 import BaseModel, Field

from app.agents.tools.rsg.common.kb_helper import retrieve_item
from app.agents.tools.rsg.common.utils import lookup_address
from app.agents.tools.rsg.common.utils import DecimalEncoder

DIV_LEVEL_POLYGON_ID = "DSP0000"

# add logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class AskKmtInput(BaseModel):
  
    address: str = Field(description="customer's street address from the input address")
    city: str = Field(description="customer's city from the input address")
    state: str = Field(description="customer's state from the input address")
    zip: str = Field(description="customer's zip from the input address")
    item: str = Field(description="the item that the customer has question about")

def ask_kmt(
    address: str, city:str, state: str, zip: str, item: str
) -> dict:
    
    if address is None or city is None or state is None or item is None:
        return "Error: Address and Item are required"

    #get division and polygon for the address using gis api
    gis_info = lookup_address(address,city,state,zip,'residential')

    info_pro_division = f"DIV_{gis_info.get('info_pro_division')}"
    polygon = gis_info["polygon"]

    #retieve the chunks from the KB
    results = retrieve_item(item, info_pro_division,polygon,DIV_LEVEL_POLYGON_ID)

    # Serialize data with Decimal values
    chunks = json.dumps(results, cls=DecimalEncoder)
    chunks_json = json.loads(chunks)

    return {
        "address": address,
        "city": city,
        "state": state,
        "division": info_pro_division,
        "polygon": polygon,
        "item": item,
        "chunks": chunks_json
    }

ask_kmt_tool = StructuredTool.from_function(
    func=ask_kmt,
    name="ask_kmt",
    description="This tool is used for customer service at a Trash pickup company. Context is around if a specific item can be recycled or picked up as trash. Retrive the KMT content associated to the customer's address and the item they are asking about",
    args_schema=AskKmtInput,
    
)