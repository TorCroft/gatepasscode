from os import getenv
from src.core import ZZU_Gate_Passcode
from src.utils import (
    utc_time_string,
    write_info_into_config,
    generate_markdown_from_template,
)

def main():
    user = ZZU_Gate_Passcode()
    user.run()

    ACTOR = getenv("GITHUB_ACTOR")
    RECORD_TIME = utc_time_string()

    write_info_into_config(
        config_data={
            "last_update_time": RECORD_TIME,
            "actor": ACTOR,
            "passcode_url": user.code_url,
        }
    )

    generate_markdown_from_template(actor=ACTOR, record_time=RECORD_TIME, **user.stats)

    if not user.login_success:
        exit(1)

if __name__ == "__main__":
    main()
