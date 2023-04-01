# gatepasscode
郑州大学通行码，适配北门、东门、南门。

## Usage
Fork 本仓库，创建一个GitHUb Action(.\github\workflows\main.yml)来更新每天的通行码。
需要四个secrets变量，分别为`UID_PWD`,`EMAIL`,`USERNAME`,`TOKEN`
* `UID_PWD`：
将你的账号密码使用`#`拼接起来
* `EMAIL,USERNAME`：
git使用的邮箱和GitHub用户名，具体请参考`.\github\workflows\main.yml`。
* `TOKEN`：
个人设置里面找到开发者选项，选择`Personal access tokens (classic)`。

创建一个GitHub Pages来部署静态网站。