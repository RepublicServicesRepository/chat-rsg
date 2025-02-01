"""Enterprice Services API Client.

This module represents the API cliet for Enterprise Services for
Accoutn status, Route details etc.
"""

import requests
import datetime
import random
import os
import logging

SOURCE_APPLICATION_NAME = "aip-mpu-bedrock-agent"
SOURCE_USER_NAME = "aip-mpu-bedrock-agent"

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def invoke_es_api(es_end_point: str, request_type: str, payload: dict) -> str:
    """Call ES API.

    This function invokes the provided ES API URL and returns the response.
    """
    ES_API_HOST = os.getenv("ES_API_HOST")
    ES_API_HOST_HEADER = os.getenv("ES_API_HOST_HEADER")
    ES_API_KEY = os.getenv("ES_API_KEY")

    transaction_id = random.randint(10**23, 10**24 - 1)

    headers = {
        "sourceApplicationName": SOURCE_APPLICATION_NAME,
        "sourceUserName": SOURCE_USER_NAME,
        "sourceSystemTransactionID": str(transaction_id),
        "sourceSystemTimeStamp": datetime.datetime.now().strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        ),
        "host": ES_API_HOST_HEADER,
        "Api-Key": ES_API_KEY,
        "Content-Type": "application/json",
    }

    es_end_point_url = f"{ES_API_HOST}/{es_end_point}"

    logger.info(f"Sending ES API Request: {es_end_point_url}")
    response = requests.request(
        request_type, es_end_point_url, headers=headers, data=payload
    )

    return response
