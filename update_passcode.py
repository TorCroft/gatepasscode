import re
import requests
import os
import json
from bs4 import BeautifulSoup
from datetime import datetime, timezone

def write_info_into_config(**kwargs):
    config = {
        "last_update_time": datetime.strftime(datetime.utcnow().replace(tzinfo=timezone.utc), "%Y-%m-%d %H:%M:%S %Z"),
        **kwargs
    }
    with open('./page/config.json', 'w', encoding='utf-8') as config_file:
        json.dump(config, config_file)

def get_user_config():
    if os.getenv("UID_PWD") is None:
        from dotenv import load_dotenv
        print("从.env文件中加载环境变量 ...")
        load_dotenv()
    return os.getenv('UID_PWD').split('&')


def download_img(image_url):
    print(f"Downloading image from {image_url}")
    response = requests.get(image_url)
    with open('./page/images/passcode.png', 'wb') as f:
        f.write(response.content)
    print('Download completed ...')
    return True


class Core(object):
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0',
        'referer': 'https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/first0?fun2=a',
        "Content-Type": 'application/x-www-form-urlencoded'
    }

    def __init__(self) -> None:
        uid_pwd = get_user_config()
        self.id = uid_pwd[0]
        self.pwd = uid_pwd[1]

        self.text = ''
        self.bs4 = None
        self.ptopid = None
        self.sid = None
        self.base_url = "https://jksb.v.zzu.edu.cn"
        self.login_url = self.base_url + "/vls6sss/zzujksb.dll/login"
        self.pass_url = self.base_url + "/vls6sss/zzujksb.dll/gettongxing?ptopid={}&door=0001&sid={}"
        self.code_url = ""

    def login(self) -> bool:
        self.form = {
            "uid": self.id,
            "upw": self.pwd,
            "smbtn": "进入健康状况上报平台",
            "hh28": "750"
        }
        for i in range(3):
            try:
                r = requests.post(self.login_url, headers=self.header, data=self.form, timeout=(200, 200))
            except:
                if i == 2:
                    raise print('Please check your Internet connection ...')
            else:
                self.text = r.text.encode(r.encoding).decode(r.apparent_encoding)
                matchObj = re.search(r'ptopid=(\w+)\&sid=(\w+)\"', self.text)
                break
        try:
            self.ptopid = matchObj.group(1)
            self.sid = matchObj.group(2)
        except requests.exceptions.RequestException as e:
            print(f'Login failed ... {e}')
            return False
        except (AttributeError, IndexError):
            if '密码输入错误' in self.text:
                message = 'Wrong password ...'
            elif '未检索到用户账号' in self.text:
                message = "Account doesn't exist ..."
            elif '验证码' in self.text:
                message = "Verification code is required ..."
            else:
                message = "Unknown reason ..."
            print(message,self.text)
            return False
        else:
            print("Successfully logged in ...")
            return True

    def get_gate_passcode(self) -> bool:
        try:
            r = requests.get(self.pass_url.format(self.ptopid, self.sid),headers=self.header)
            self.text = r.text.encode(r.encoding).decode(r.apparent_encoding)
            self.bs4 = BeautifulSoup(self.text, 'html.parser')
            div_tag = self.bs4.find('div', attrs={"id": "bak_0"}).find('div')
            self.code_url:str = self.base_url + div_tag['style'].split('url(')[1].split(')')[0]
            return download_img(self.code_url)
        except Exception as e:
            print(f'Download failed ... {e}')
            return False

    def run(self) -> bool:
        print("Preparing to log in ...")
        if not self.login():
            print("登录失败 ...")
            return False
        else:
            self.get_gate_passcode()


if __name__ == "__main__":
    test_user = Core()
    test_user.run()
    write_info_into_config(passcode_url=test_user.code_url)
