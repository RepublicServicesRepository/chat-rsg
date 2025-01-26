import base64
import os

import requests


def get_pdf_info(url) -> tuple[str, bytes]:
    response = requests.get(url)

    if response.status_code == 200:
        content_disposition = response.headers.get("Content-Disposition")
        if content_disposition:
            filename = content_disposition.split("filename=")[1].strip('"')
        else:
            filename = os.path.basename(url)

        file_content_byte = response.content

        return filename, file_content_byte
    else:
        raise Exception(f"Failed to fetch PDF from {url}")


def get_aws_overview() -> tuple[str, bytes]:
    URL = "https://pages.awscloud.com/rs/112-TZM-766/images/Architecting%20on%20AWS.pdf"
    return get_pdf_info(URL)


def get_test_markdown() -> str:
    return "##\nThis is a test text."
