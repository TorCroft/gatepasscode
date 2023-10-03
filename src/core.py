import re
import requests
from bs4 import BeautifulSoup
from .utils import get_user_config, download_img
from .logger import logger


class ZZU_Gate_Passcode:
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0",
        "referer": "https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/first0?fun2=a",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    def __init__(self) -> None:
        uid_pwd = get_user_config()
        self.id = uid_pwd[0]
        self.pwd = uid_pwd[1]

        self.ptopid = ""
        self.sid = ""
        self.base_url = "https://jksb.v.zzu.edu.cn"
        self.login_url = self.base_url + "/vls6sss/zzujksb.dll/login"
        self.pass_url = self.base_url + "/vls6sss/zzujksb.dll/gettongxing?ptopid={}&door=0001&sid={}"
        
        self.code_url = ""

    def login(self) -> bool:
        body = {
            "uid": self.id,
            "upw": self.pwd,
            "smbtn": "进入健康状况上报平台",
            "hh28": "750",
        }
        for i in range(3):
            try:
                r = requests.post(
                    self.login_url,
                    headers=self.header,
                    data=body,
                    timeout=(200, 200),
                )
            except:
                if i == 2:
                    raise requests.exceptions.RequestException("No Internet Connection ...")
            else:
                text = r.text.encode(r.encoding).decode(r.apparent_encoding)
                match = re.search(r"ptopid=(\w+)\&sid=(\w+)\"", text)
                break
        try:
            self.ptopid = match.group(1)
            self.sid = match.group(2)
        except (AttributeError, IndexError):
            if "密码输入错误" in text:
                message = "Wrong password ..."
            elif "未检索到用户账号" in text:
                message = "Account doesn't exist ..."
            elif "验证码" in text:
                message = "Verification code is required ..."
            else:
                message = "Unknown reason ..."
            logger.debug(message)
            return False
        else:
            logger.info("Successfully logged in ...")
            return True

    def get_gate_passcode(self) -> bool:
        try:
            r = requests.get(self.pass_url.format(self.ptopid, self.sid), headers=self.header)
            text = r.text.encode(r.encoding).decode(r.apparent_encoding)
            soup = BeautifulSoup(text, "html.parser")
            div_tag = soup.find("div", attrs={"id": "bak_0"}).find("div")
            self.code_url: str = self.base_url + div_tag["style"].split("url(")[1].split(")")[0]
            return download_img(self.code_url)
        except Exception as e:
            logger.error(f"Download failed ... {e}")
            return False

    def run(self) -> bool:
        logger.info("Preparing to log in ...")
        if not self.login():
            logger.info("登录失败 ...")
            return False
        else:
            self.get_gate_passcode()
