from app.agents.tools.base import BaseTool
from app.agents.tools.internet_search import internet_search_tool
from app.agents.tools.rsg.ask_kmt import ask_kmt_tool
from app.agents.tools.rsg.mpu_tool import mpu_tool  


def get_available_tools() -> list[BaseTool]:
    tools: list[BaseTool] = []
    tools.append(internet_search_tool)
    tools.append(ask_kmt_tool)
    tools.append(mpu_tool)
    return tools


def get_tool_by_name(name: str) -> BaseTool:
    for tool in get_available_tools():
        if tool.name == name:
            return tool
    raise ValueError(f"Tool with name {name} not found")