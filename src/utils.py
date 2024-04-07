import requests
import json
from os import getenv
from datetime import datetime, UTC
from functools import wraps
from typing import Callable, Any
from time import sleep


TEMPLATE = """## GatePasscode Log
| **Key** | **Value** |
|-----------------------|---------------------|
| **Actor**             | {actor}             |
| **Login Status**      | {login_status}      |
| **Record Time**       | {record_time}       |
| **Code Image URL**    | {code_image_url}    |"""


def generate_markdown_from_template(**data):
    markdown_table = TEMPLATE.format(**data)
    print(markdown_table)


def retry(retries: int = 3, delay: float = 1) -> Callable:
    """
    Attempt to call a function, if it fails, try again with a specified delay.

    :param retries: The max amount of retries you want for the function call
    :param delay: The delay (in seconds) between each function retry
    :return:
    """

    # Don't let the user use this decorator if they are high
    if retries < 1 or delay <= 0:
        raise ValueError("Are you high, mate?")

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for i in range(
                1, retries + 1
            ):  # 1 to retries + 1 since upper bound is exclusive

                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    # Break out of the loop if the max amount of retries is exceeded
                    if i == retries:
                        break
                    else:
                        sleep(delay)  # Add a delay before running the next iteration

        return wrapper

    return decorator


def utc_time_string():
    utc_time = datetime.now(UTC)
    return datetime.strftime(utc_time, "%Y-%m-%d %H:%M:%S %Z")


def write_info_into_config(config_data: dict):
    with open("./page/config.json", "w", encoding="utf-8") as config_file:
        json.dump(config_data, config_file)


def get_user_config():
    if (uid_pid := getenv("UID_PWD")) is None:
        from dotenv import load_dotenv

        print("从.env文件中加载环境变量 ...")
        load_dotenv()
        uid_pid = getenv("UID_PWD")
    return uid_pid.split("&")


def download_img(image_url):
    response = requests.get(image_url)
    with open("./page/images/passcode.png", "wb") as f:
        f.write(response.content)
    return True
