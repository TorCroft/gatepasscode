from datetime import datetime, timedelta
import json


def load_data_from_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def convert_utc_to_utc8(utc_time_str: str) -> datetime:
    return datetime.strptime(utc_time_str, "%Y-%m-%d %H:%M:%S %Z") + timedelta(hours=8)

def get_date_str(input_time: datetime):
    return datetime.strftime(input_time, "%Y/%m/%d %H:%M:%S")


MD_TEMPLATE = """## GatePasscode Log
| **Record Time (UTC+8)** | **Actor** | **URL** |
| --------------- | --------  | ------- |
| {time} | {actor} | {passcode_url} |"""


if __name__ == "__main__":
    latest_record = load_data_from_json("./page/config.json")
    time_str = get_date_str(convert_utc_to_utc8(latest_record["last_update_time"]))
    print(MD_TEMPLATE.format(time=time_str, **latest_record))
