import json
import logging

from app.agents.tools.base import  StructuredTool
from langchain_core.pydantic_v1 import BaseModel, Field

from backend.app.agents.tools.rsg.ask_sop.kb_helper import retrieve_sop
from app.agents.tools.rsg.common.utils import DecimalEncoder

# add logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class AskSopInput(BaseModel):
  
    input: str = Field(description="user's input prompt or question")

def ask_sop(
    input: str
) -> dict:
    
    if input is None:
        return "Error: Input is required"
    
    logger.info(f"User qustion/prompt/input: {input}")

    #retieve the chunks from sop
    results = retrieve_sop(input)
    logger.info(f"Results: {results}")

    # Serialize data with Decimal values
    chunks = json.dumps(results, cls=DecimalEncoder)
    chunks_json = json.loads(chunks)

    return {
        "input": input,
        "chunks": chunks_json
    }

ask_sop_tool = StructuredTool.from_function(
    func=ask_sop,
    name="ask_kmt",
    description="This tool is used for customer service at a Trash pickup company. Retreives the relevant content for the standard oeprating procedure for the user's scenario/input/question",
    args_schema=AskSopInput,
    
)