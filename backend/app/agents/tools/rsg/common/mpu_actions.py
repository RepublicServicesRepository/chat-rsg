"""MPU Bedrock Agent Action Group Actions.

This module represents vraious actions of MPU Bedrock Agent Action Group.
"""

import logging
import json
from app.agents.tools.rsg.lib.es_api import invoke_es_api
from app.agents.tools.rsg.lib.utils import lookup_address

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ACTIVE = "active"
INACTIVE = "inactive"

def get_account_site(address: str,city:str,state:str,zip:str) -> dict:
    
    #get division and polygon for the address using gis api
    gis_info = lookup_address(address,city,state,zip,None)
    if gis_info.get("error"):
        return gis_info

    info_pro_division  = gis_info["info_pro_division"]
    lawson_divison = gis_info["lawson_divison"]
    
    # invoke es account api to get account info using the address
    end_point = (
        f"account/v2/accounts?division={info_pro_division}&address_line1={address}s&city={city}&state={state}&accountStatus=open&siteStatus=open&displayEntity=All"
    )

    response = invoke_es_api(end_point, request_type="GET", payload={})
    logger.info(f"Response from ES Accounts API: {response.json()}")

    if response.status_code != 200:
        logger.error(f"Error invoking ES Accounts API.  \
                     Status Code: {response.status_code}")
        return {"error": "Error invoking ES Accounts API", "endPoint": end_point,"statusCode": response.status_code}

    if (
        len(response.json()["data"]) > 0
        and len(response.json()["data"][0]["sites"]) > 0
    ):
        data = response.json()["data"][0]
        sites = data["sites"]
        return {
            "accountId": data["accountId"],
            "infoproAccountNumber": data["infoproAccountNumber"],
            "siteId": sites[0][
                "odsSiteId"
            ],  # should only be 1 site for site address hash
            "status": ACTIVE,
            "divisionId": info_pro_division,
            "lawsonDivision": lawson_divison,
        }
    else:
        logger.info(f"No account found for site address: {address}. {city}, {state}")   
        return {"status": INACTIVE, "error": "Account/Site Inactive or Not Found"}   


def get_container(account_id: str, site_id: str, container_type: str) -> dict:
    """Get conteiner for the given account and site and of the specified type.

    :return: Dictionary containing container info.
    """
    logger.info(
        f"Getting containers for Account: {account_id}. Site: {site_id}. "
        f"Type: {container_type}"
    )

    # invoke es container api to get containers for the account and site
    end_point = (
        f"account/v1/accounts/{account_id}/sites/{site_id}/containers"
        "?displayEntity=all&containerStatus=open"
    )
    response = invoke_es_api(end_point, request_type="GET", payload={})

    if response.status_code != 200:
        logger.error(f"Error invoking ES Accounts API.  \
                     Status Code: {response.status_code}")
        return {"error": "Error invoking ES Accounts API"}

    logger.info(f"Response from ES Accounts API: {response.json()}")

    if len(response.json()["data"]) > 0:
        containers = response.json()["data"]
        for container in containers:
            # eg. Solid Waste or Recycling
            if container["wasteTypeDescription"] == container_type:
                return {
                    "containerId": container["containerId"],
                    "infoProContainerId": container["infoProContainerId"],
                    "containerType": container["wasteTypeDescription"],
                }
        return {"error": "No Active Container found for the given container type"}
    else:
        logger.info(
            f"No Active Containers Found for  Account: {account_id}" f"Site: {site_id}."
        )
        return {"error": "No Active Containers found for the given account and site"}


def get_container_schedule(division_id: str, container_id: str, mpu_date: str) -> dict:
    """Get schedule for the given container id.

    :param container_id: Container id for which the schedule is to be fetched.
    :param division_id: Division id for which the schedule is to be fetched.
    :param mpu_date: MPU Date for which the schedule is to be fetched.
    :return: Dictionary containing container schedule.
    """
    logger.info(f"Get schedule for container:{container_id}. Division:{division_id}")

    # invoke es container api to get container route
    end_point = f"routes/v1/container/{container_id}/routes"
    response = invoke_es_api(end_point, request_type="GET", payload={})
    if response.status_code != 200:
        logger.error(f"Error invoking ES Container Routes API.  \
                     Status Code: {response.status_code}")
        return {"error": "Error invoking ES Container Routes API"}

    logger.info(f"Response from ES Container Routes API: {response.json()}")
    if len(response.json()["data"]) == 0:
        return {"error": "No Routes found for the container"}

    route = response.json()["data"][0].get("route")

    # invoke es get active route details API to get route details
    end_point = (
        f"routes/v1/divisions/{division_id}/routes/active/{route}/details"
        f"?dateServiced={mpu_date}&displayEntity=All"
    )
    response = invoke_es_api(end_point, request_type="GET", payload={})
    if response.status_code != 200:
        logger.error(f"Error invoking ES Active Route Details API.  \
                     Status Code: {response.status_code}")
        return {"error": "Error invoking ES Active Route Details API"}

    logger.info(f"Response from ES Active Route Details: {response.json()}")
    routes = response.json()["data"]
    if len(routes) == 0:
        return {"error": "No Active Route details found for the route"}

    # now go thu the routes and find the route details for the container
    for route in routes:
        if (
            route.get("odsContainerId") is not None
            and str(route.get("odsContainerId")) == container_id
        ):
            logger.info(f"Route details found for the container: {container_id}")
            logger.info(f"Route details: {route}")
            return {
                "containerId": container_id,
                "status": route.get("status"),
                "dateServiced": route.get("dateServiced"),
                "updatedDate": route.get("updateDate"),
                "containerNotes": route.get("completeURNote"),
            }

    return {"error": "No Active Route details found for the container in the route"}


def get_division_announcements(lawsonDivision: str) -> dict:
    """Get announcements for the given division id.

    :param division_id: Division id for which the announcements are to be fetched.
    :return: Dictionary containing division announcements.
    """
    logger.info(f"Getting division announcements for lawson division: {lawsonDivision}")

    # invoke es container api to get containers for the account and site
    end_point = f"operations/v1/divisions/{lawsonDivision}/divisionAlerts"

    response = invoke_es_api(end_point, request_type="GET", payload={})

    if response.status_code != 200:
        logger.error(f"Error invoking ES Accounts API.  \
                     Status Code: {response.status_code}")
        return {"error": "Error invoking ES Accounts API"}

    logger.info(f"Response from ES Accounts API: {response.json()}")

    announcements = ""
    if len(response.json()["data"]) > 0:
        alerts = response.json()["data"]
        for alert in alerts:
            announcements += alert["alertMessage"] + " | "

    return {"lawsonDivision": lawsonDivision, "announcements": announcements}


def create_case(infopro_container_id: str, mpu_date: str) -> dict:
    """Create a case for the given case details.

    :param infopro_container_id
    :param mpu_date
    :return: Dictionary containing case creation details.
    """
    logger.info("Creating Case")
    logger.info(f"InfoproContainerId: {infopro_container_id} MPU Date: {mpu_date}")
    # eg. infopro_container_id = "05000000100000101"
    payload = json.dumps(
        {
            "accountId": infopro_container_id[3:10],
            "siteId": infopro_container_id[10:15],
            "containerId": infopro_container_id[15:],
            "division": infopro_container_id[0:3],
            "serviceRequest": {  # todo: need to update the service request details
                "preferredContactMethod": "",
                "servicePlanDate": mpu_date,
                "requestType": "SERVICE",
                "serviceCode": "CGB",
                "poNumber": "",
                "numberOfLifts": "1",
                "orderNote": "",
                "reasonCode": "",
                "serviceCommitmentDate": mpu_date,
                "userName": "MPU-Agent",
                "sourceId": "Missed Pickup Request",
                "description": "Missed Pickup",
            },
        }
    )
    print(f"Service Request Payload: {payload}")

    # invoke es customer request api to create a case
    end_point = "customerrequest/v1/customer-requests"

    response = invoke_es_api(end_point, request_type="POST", payload=payload)

    if response.status_code != 200:
        logger.error(f"Error invoking ES Accounts API.  \
                     Status Code: {response.status_code}")
        return {"error": "Error invoking ES Accounts API"}

    logger.info(f"Response from ES Accounts API: {response.json()}")

    return {"caseNumber": response.json()["data"]["caseNumber"]}
