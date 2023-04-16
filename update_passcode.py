import re
import requests
import os
from bs4 import BeautifulSoup


def download_img(image_url):
    response = requests.get(image_url)
    with open('./page/images/passcode.png', 'wb') as f:
        f.write(response.content)
    print('Download completed ...')
    return True


class Core(object):
    def __init__(self) -> None:
        env_uid_pwd = os.environ.get('uid_and_pwd')
        if env_uid_pwd:
            uid_pwd = env_uid_pwd.split("&")
            self.id = uid_pwd[0]
            self.pwd = uid_pwd[1]
        else:
            # 本地运行时使用
            self.id = input("Input Your Uid >")
            self.pwd = input("Input Your Password >")

        self.text = ''
        self.bs4 = None
        self.ptopid = None
        self.sid = None
        self.base_url = "https://jksb.v.zzu.edu.cn/"
        self.login_url = "https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/login"
        self.pass_url = "https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/gettongxing?ptopid={}&door=0001&sid={}"

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0',
            'referer': 'https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/first0?fun2=a',
            "Content-Type": 'application/x-www-form-urlencoded'
        }

    def login(self) -> bool:
        self.form = {
            "uid": self.id,
            "upw": self.pwd,
            "smbtn": "进入健康状况上报平台",
            "hh28": "750"
        }
        for i in range(3):
            try:
                r = requests.post(self.login_url, headers=self.headers, data=self.form, timeout=(200, 200))
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
        except:
            if '密码输入错误' in self.text:
                message = 'Wrong password ...'
            elif '未检索到用户账号' in self.text:
                message = "Account doesn't exist ..."
            elif '验证码' in self.text:
                message = "Verification code is required ..."
            else:
                message = "Unknown reason ..."
            print(message)
            return False
        else:
            print("Successfully logged in ...")
            return True

    def get_gate_passcode(self) -> bool:
        try:
            r = requests.get(self.pass_url.format(self.ptopid, self.sid))
            self.text = r.text.encode(r.encoding).decode(r.apparent_encoding)
            self.bs4 = BeautifulSoup(self.text, 'html.parser')
            div_tag = self.bs4.find('div', attrs={"id": "bak_0"}).find('div')
            code_url = self.base_url + div_tag['style'].split('url(')[1].split(')')[0]
            return download_img(code_url)
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
