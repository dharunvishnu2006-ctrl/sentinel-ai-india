import logging
import os

import requests
from dotenv import load_dotenv

from src.retry import retry

logger = logging.getLogger(f"sentinel.{__name__}")

load_dotenv()

CLOUDSHIELD_URL = os.environ.get("CLOUDSHIELD_URL", "http://localhost:5000/status")
AUTOPILOT_URL = os.environ.get("AUTOPILOT_URL", "http://localhost:5001/status")
CLOUDSHIELD_API_KEY = os.environ.get("CLOUDSHIELD_API_KEY", "")


@retry(times=2, backoff=1)
def _fetch(url, api_key=None):
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    response = requests.get(url, headers=headers, timeout=5)
    response.raise_for_status()
    return response.json()


def get_cloudshield_status():
    try:
        data = _fetch(CLOUDSHIELD_URL, api_key=CLOUDSHIELD_API_KEY)
        logger.info("CloudShield status fetched successfully")
        return {"status": "online", "data": data}
    except Exception as e:
        logger.warning(f"CloudShield unreachable: {e}")
        return {"status": "degraded", "data": None}


def get_autopilot_status():
    try:
        data = _fetch(AUTOPILOT_URL)
        logger.info("AutoPilot status fetched successfully")
        return {"status": "online", "data": data}
    except Exception as e:
        logger.warning(f"AutoPilot unreachable: {e}")
        return {"status": "degraded", "data": None}
