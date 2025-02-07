from app.agents.tools.base import BaseTool
from app.agents.tools.rsg.ask_kmt.tool import ask_kmt_tool
from app.agents.tools.rsg.ask_sop.tool import ask_sop_tool
from app.agents.tools.rsg.mpu.tool import mpu_tool
from app.agents.tools.rsg.ask_jeff.tool import ask_jeff_tool


def get_available_tools() -> list[BaseTool]:
    tools: list[BaseTool] = []
    tools.append(ask_kmt_tool)
    tools.append(ask_sop_tool)
    tools.append(mpu_tool) 
    tools.append(ask_jeff_tool) 
    return tools


def get_tool_by_name(name: str) -> BaseTool:
    for tool in get_available_tools():
        if tool.name == name:
            return tool
    raise ValueError(f"Tool with name {name} not found")