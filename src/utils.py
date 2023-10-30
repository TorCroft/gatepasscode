import requests
import os
import json
from datetime import datetime, UTC
from .logger import logger


def utc_time_string():
    utc_time = datetime.now(UTC)
    return datetime.strftime(utc_time, "%Y-%m-%d %H:%M:%S %Z")


def write_info_into_config(**kwargs):
    config = {
        "last_update_time": utc_time_string(),
        **kwargs,
    }
    with open("./page/config.json", "w", encoding="utf-8") as config_file:
        json.dump(config, config_file)


def get_user_config():
    if os.getenv("UID_PWD") is None:
        from dotenv import load_dotenv

        logger.info("从.env文件中加载环境变量 ...")
        load_dotenv()
    return os.getenv("UID_PWD").split("&")


def download_img(image_url):
    logger.info(f"Downloading image from {image_url}")
    response = requests.get(image_url)
    with open("./page/images/passcode.png", "wb") as f:
        f.write(response.content)
    logger.info("Download completed ...")
    return True
