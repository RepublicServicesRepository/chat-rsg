from app.agents.tools.base import BaseTool
from backend.app.agents.tools.rsg.ask_kmt import ask_kmt_tool
from backend.app.agents.tools.rsg.ask_sop import ask_sop_tool
#from app.agents.tools.rsg.mpu import mpu_tool


def get_available_tools() -> list[BaseTool]:
    tools: list[BaseTool] = []
    tools.append(ask_kmt_tool)
    tools.append(ask_sop_tool)
    #tools.append(mpu_tool) #will be added later when ES APIs are ready
    return tools


def get_tool_by_name(name: str) -> BaseTool:
    for tool in get_available_tools():
        if tool.name == name:
            return tool
    raise ValueError(f"Tool with name {name} not found")