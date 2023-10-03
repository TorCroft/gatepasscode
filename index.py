from src.core import ZZU_Gate_Passcode
from src.utils import write_info_into_config

if __name__ == "__main__":
    test_user = ZZU_Gate_Passcode()
    test_user.run()
    write_info_into_config(passcode_url=test_user.code_url)
