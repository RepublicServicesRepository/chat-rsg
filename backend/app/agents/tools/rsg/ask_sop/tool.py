import json
import logging

from app.agents.tools.base import  StructuredTool
from langchain_core.pydantic_v1 import BaseModel, Field

from app.agents.tools.rsg.ask_sop.kb_helper import retrieve_sop
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
    name="AskSOP",
    description="This tool is utilized by customer service representatives at a Trash pickup and recycle company. \
            to access Standard Operating Procedures (SOPs) related to variious customer's questions about their trash. \
            The function takes a string input describing the user's scenario, question, or specific situation. \
            It then searches the company's SOP database to retrieve relevant content that addresses the given input \
            The returned dictionary contains step-by-step instructions, guidelines, or protocols \
            that the customer service representative should follow to handle the specific situation or  \
            answer the customer's question. This ensures consistency in service delivery and adherence \
            to company policies across various customer interactions.",
    args_schema=AskSopInput,
    
)