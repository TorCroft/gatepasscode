# gatepasscode
郑州大学通行码，适配北门、东门、南门。

## Usage
Fork 本仓库，创建一个GitHUb Action(.\github\workflows\main.yml)来更新每天的通行码。
需要四个secrets变量，分别为`UID_PWD`,`EMAIL`,`USERNAME`,`TOKEN`
* `UID_PWD`：
账号密码都是健康打卡平台的，将你的账号密码使用`#`拼接起来，exp: 你的账号是123456789，密码是passcode，那么`UID_PWD`的值应该是`123456789#passcode`，密码默认是身份证后八位。
* `EMAIL,USERNAME`：
git使用的邮箱和GitHub用户名，具体请参考`.\github\workflows\main.yml`，用于git push更新通行码图片（该图片每天一换）。
* `TOKEN`：
个人设置里面找到开发者选项，选择`Personal access tokens (classic)`。

创建一个GitHub Pages来部署静态网站。
