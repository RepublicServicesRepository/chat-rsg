from app.agents.tools.agent_tool import AgentTool
from app.repositories.models.custom_bot import BotModel
from app.routes.schemas.conversation import type_model_name
from pydantic import BaseModel, Field
import json
import logging

from app.agents.tools.rsg.lib.utils import DecimalEncoder
from app.agents.tools.rsg.lib.mpu_actions import get_account_site, get_container
from app.agents.tools.rsg.lib.mpu_actions import get_container_schedule,get_division_announcements

DIV_LEVEL_POLYGON_ID = "DSP0000"

# add logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class MpuInput(BaseModel):
    address: str = Field(description="customer's street address from the input address")
    city: str = Field(description="customer's city from the input address")
    state: str = Field(description="customer's state from the input address")
    zip: str = Field(description="customer's zip from the input address")
    containerType: str = Field(description="the container type that the customer has question about")
    mpuDate: str = Field(description="the missed pickup date the customer has question about")

def handle_mpu(
    arg: MpuInput, bot: BotModel | None, model: type_model_name | None
) -> dict:
    
    address = arg.address
    city = arg.city
    state = arg.state
    zip = arg.zip
    containerType = arg.containerType
    mpuDate = arg.mpuDate
    
    if address is None or city is None or state is None or containerType is None or mpuDate is None:
        return "Error: Address,Container Type and MPU Date are required"
    
    mpu_ressponse = {}
    try:
        account_site = get_account_site(address, city, state,zip)
        if account_site.get("error") is not None:
            mpu_ressponse["error"] = account_site["error"]
            mpu_ressponse["endPoint"] = account_site["endPoint"]
            mpu_ressponse["statusCode"] = account_site["statusCode"]
        else:
            mpu_ressponse["account_site"] = account_site
            container = get_container(account_site["accountId"], account_site["siteId"], containerType)
            if(container.get("error")) is not None:
                mpu_ressponse["error"] = container["error"]
            else:
                mpu_ressponse["container"] = container
                container_schedule = get_container_schedule(account_site["divisionId"],container["containerId"], mpuDate)
                if(container_schedule.get("error")) is not None:
                    mpu_ressponse["error"] = container_schedule["error"]
                else:
                    mpu_ressponse["container_schedule"] = container_schedule
                    division_announcements = get_division_announcements(account_site["lawsonDivision"])
                    if(division_announcements.get("error")) is not None:
                        mpu_ressponse["error"] = division_announcements["error"]
                    else:
                        mpu_ressponse["division_announcements"] = division_announcements
                        # #create case
                        # case = create_case(container["infoProContainerId"], mpuDate)
                        # if(case.get("error")) is not None:
                        #     mpu_ressponse["error"] = case["error"]
                        # else:
                        #     mpu_ressponse["case"] = case
    except Exception as e:
        logger.error(f"Error in handle_mpu: {e}")
        mpu_ressponse["error"] = f"Exception in handle_mpu: {str(e)}"

    # # Serialize data with Decimal values
    mpu_ressponse_dump = json.dumps(mpu_ressponse, cls=DecimalEncoder)
    mpu_ressponse_json = json.loads(mpu_ressponse_dump)

    return {
        "address": address,
        "city": city,
        "state": state,
        "containerType": containerType,
        "mpuDate": mpuDate,
        "mpuResponse": mpu_ressponse_json
    }
    
mpu_tool = AgentTool(
    name="mpu_tool",
    description="This tool is used for customer service to handle calles about mpu (Missed Pickup) issues. It checks various things like open account/site status, open containers on account and the container is actually scheduled to be pickup and there are no division level delayes. If all checks pass then creates a missed pick up case for the customer.",
    args_schema=MpuInput,
    function=handle_mpu,
)
