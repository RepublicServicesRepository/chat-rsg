import json
import logging

from app.agents.tools.base import  StructuredTool
from langchain_core.pydantic_v1 import BaseModel, Field

from app.agents.tools.rsg.ask_jeff.kb_helper import retrieve_jeff
from app.agents.tools.rsg.common.utils import DecimalEncoder

# add logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class AskJeffInput(BaseModel):
    topic: str = Field(description="topic or subject of the input prompt or question")
    input: str = Field(description="user's input prompt or question")

def ask_jeff_tool(
    input: str,
    topic: str
) -> dict:
    
    if input is None:
        return "Error: Input is required"
    if topic is None:
        return "Error: Unable to determine the topic"
    
    logger.info(f"User qustion/prompt/input: {input}")
    logger.info(f"Topic: {topic}")

    #retieve the chunks from sop
    results = retrieve_jeff(topic,input)
    logger.info(f"Results: {results}")

    # Serialize data with Decimal values
    chunks = json.dumps(results, cls=DecimalEncoder)
    chunks_json = json.loads(chunks)

    return {
        "input": input,
        "chunks": chunks_json
    }

ask_sop_tool = StructuredTool.from_function(
    func=ask_jeff_tool,
    name="AskJeff",
    description="This tool is utilized by software developers to access various developer documentation to procvide  \
            answers to their questions related to a specific topic . \
            The function takes a string parameter named topic that determines the topic of hte question and another \
            string input describing the user's question or prompt \
            It then searches the developer knowledgbase to retrieve relevant content that addresses the given input ",
    args_schema=AskJeffInput,
    
)