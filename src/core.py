import re
import requests
from bs4 import BeautifulSoup
from .utils import get_user_config, download_img, retry


class LoginFailedException(Exception):
    def __init__(self, message=None):
        self.message = message
        super().__init__(self.message)


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

        self.login_success = False

        self.ptopid = ""
        self.sid = ""
        self.base_url = "https://jksb.v.zzu.edu.cn"
        self.login_url = self.base_url + "/vls6sss/zzujksb.dll/login"
        self.pass_url = self.base_url + "/vls6sss/zzujksb.dll/gettongxing?ptopid={}&door=0001&sid={}"
        
        self.reason = ""
        self.code_url = ""

    @retry(retries=3, delay=10)
    def login(self) -> bool:
        body = {
            "uid": self.id,
            "upw": self.pwd,
            "smbtn": "进入健康状况上报平台",
            "hh28": "750",
        }
        r = requests.post(self.login_url, headers=self.header, data=body)
        text = r.text.encode(r.encoding).decode(r.apparent_encoding)
        match = re.search(r"ptopid=(\w+)\&sid=(\w+)\"", text)
        try:
            self.ptopid = match.group(1)
            self.sid = match.group(2)
        except (AttributeError, IndexError):
            if "密码输入错误" in text:
                self.reason = "Incorrect password"
            elif "未检索到用户账号" in text:
                self.reason = "Account doesn't exist"
            elif "验证码" in text:
                self.reason = "Verification code is required"
            else:
                self.reason = "Unknown"
            return False
        else:
            return True

    def get_gate_passcode(self) -> bool:
        r = requests.get(self.pass_url.format(self.ptopid, self.sid), headers=self.header)
        text = r.text.encode(r.encoding).decode(r.apparent_encoding)
        soup = BeautifulSoup(text, "html.parser")
        div_tag = soup.find("div", attrs={"id": "bak_0"}).find("div")
        self.code_url: str = (self.base_url + div_tag["style"].split("url(")[1].split(")")[0])
        return download_img(self.code_url)

    def run(self) -> bool:
        self.login_success = self.login()

        if not self.login_success:
            # "登录失败 ..."
            return False
        else:
            self.get_gate_passcode()
        
    @property    
    def stats(self):
        return {
            "login_status": "Success ✅" if self.login_success else f"Fail ❌ |\n| **Login Failed Reason** | {self.reason}",
            "code_image_url": self.code_url
        }
