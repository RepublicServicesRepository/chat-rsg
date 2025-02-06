import json
import logging

from app.agents.tools.base import  StructuredTool
from langchain_core.pydantic_v1 import BaseModel, Field

from app.agents.tools.rsg.common.utils import DecimalEncoder
from app.agents.tools.rsg.mpu.mpu_actions import get_account_site, get_container
from app.agents.tools.rsg.mpu.mpu_actions import get_container_schedule,get_division_announcements

# add logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class MpuInput(BaseModel):
    address: str = Field(description="customer's street address from the input address")
    city: str = Field(description="customer's city from the input address")
    state: str = Field(description="customer's state from the input address")
    zip: str = Field(description="customer's zip from the input address")
    containerType: str = Field(description="the container type that the customer has question about")
    mpuDate: str = Field(description="the missed pickup date the customer has question about")

def handle_mpu(
    address:str, city:str, state: str, zip: str, containerType: str, mpuDate: str
) -> dict:
    
    if address is None or city is None or state is None or containerType is None or mpuDate is None:
        return "Error: Address,Container Type and MPU Date are required"
    
    logger.info(f"Address: {address}, City: {city}, State: {state}, Zip: {zip}, Container Type: {containerType}, MPU Date: {mpuDate}")
    
    mpu_ressponse = {}
    try:
        account_site = get_account_site(address, city, state,zip)
        if account_site.get("error") is not None:
            mpu_ressponse["error"] = account_site["error"]
            mpu_ressponse["endPoint"] = account_site["endPoint"]
            mpu_ressponse["statusCode"] = account_site["statusCode"]
        else:
            logger.info(f"Account Site: {account_site}")
            mpu_ressponse["account_site"] = account_site
            container = get_container(account_site["accountId"], account_site["siteId"], containerType)
            if(container.get("error")) is not None:
                mpu_ressponse["error"] = container["error"]
            else:
                logger.info(f"Container: {container}")
                mpu_ressponse["container"] = container
                container_schedule = get_container_schedule(account_site["divisionId"],container["containerId"], mpuDate)
                if(container_schedule.get("error")) is not None:
                    mpu_ressponse["error"] = container_schedule["error"]
                else:
                    logger.info(f"Container Schedule: {container_schedule}")
                    mpu_ressponse["container_schedule"] = container_schedule
                    division_announcements = get_division_announcements(account_site["lawsonDivision"])
                    if(division_announcements.get("error")) is not None:
                        mpu_ressponse["error"] = division_announcements["error"]
                    else:
                        logger.info(f"Division Announcements: {division_announcements}")
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

    logger.info(f"MPU Response: {mpu_ressponse_json}")

    return {
        "address": address,
        "city": city,
        "state": state,
        "containerType": containerType,
        "mpuDate": mpuDate,
        "mpuResponse": mpu_ressponse_json
    }


mpu_tool = StructuredTool.from_function(
    func=handle_mpu,
    name="MPU Tool",
    description= '''
    This tool is utilized by customer service representatives at a Trash pickup and recycle company
    It's designed for customer service representatives to handle calls about Missed Pickup (MPU) issues. The function performs a series of checks to validate and process an MPU claim. It takes the customer's full address (street address, city, state, and zip code), the type of container that was missed, and the date of the missed pickup as input. The tool then performs the following checks:
        1. Verifies if the customer has an open and active account
        2. Confirms the site status is active
        3. Checks if there are open containers on the account
        4. Validates that the specified container is actually scheduled for pickup on the given date
        5. Checks for any division-level delays that might affect the pickup

        The returned dictionary contains the results of these checks and any additional information or instructions for the customer service representative to relay to the customer using a knowledgebase document. If any check fails, the dictionary will include details about why the MPU claim cannot be processed and suggested next steps.
    '''
)
    