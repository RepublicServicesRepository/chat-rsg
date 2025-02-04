from decimal import Decimal
import json
from app.agents.tools.rsg.common.gis import get_poly
import logging

# add logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Custom JSON encoder for Decimal
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)  # or str(obj) for precision
        return super(DecimalEncoder, self).default(obj)

def lookup_address(address,city,state,zip,lob):
    try:
        result = get_poly({'address':address,'city':city,'state':state,'zip':zip}, lob)
        info_pro_division = result.get('infoproDivision')
        lawson_divison = result.get('lawsonDivision')
        polygon = result.get('polygonId')
        return {
            "info_pro_division": info_pro_division,
            "lawson_divison": lawson_divison,
            "polygon": polygon
        }
    except Exception as e:
        logger.error(f'An error occurred: {e}')
        return {"error": "Error invoking GIS API" + str(e)}
    

def convert_params_to_dict(params_list: list):
    """Convert a list of parameters to a dictionary.

    :param params_list: list containing params,
    e.g. [{"name": "report_id", "value": "42"}]
    :return: dictionary containing params, e.g. {"report_id": "42"}
    """
    params_dict = {
        param.get("name"): param.get("value")
        for param in params_list
        if param.get("name") is not None
    }

    return params_dict


    