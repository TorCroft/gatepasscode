# gatepasscode
郑州大学主校区通行码，适配北门、东门、南门。<br>[GitHub Pages 部署成果](https://torcroft.github.io/gatepasscode/)<br>[![Update passcode image](https://github.com/TorCroft/gatepasscode/actions/workflows/main.yml/badge.svg)](https://github.com/TorCroft/gatepasscode/actions/workflows/main.yml)<br>[![Deploy static content to Pages](https://github.com/TorCroft/gatepasscode/actions/workflows/static.yml/badge.svg)](https://github.com/TorCroft/gatepasscode/actions/workflows/static.yml)

## Usage
Fork 本仓库，创建一个GitHUb Action(./github/workflows/main.yml)来更新每天的通行码。
需要三个secrets变量，分别为`UID_PWD`,`EMAIL`,`USERNAME`
* `UID_PWD`：
账号密码都是健康打卡平台的，将你的账号密码使用`#`拼接起来。<br>Exp: 你的账号是123456789，密码是password，那么`UID_PWD`的值应该是`123456789#password`，密码默认是身份证后八位。用于python脚本爬取新的通行码图片。
* `EMAIL`：
git使用的邮箱，具体请参考`./github/workflows/main.yml`，用于git push推送新的通行码图片到仓库（该图片每天一换）。
* `USERNAME`:
GitHub的用户名，用于git push推送新的通行码图片到仓库（该图片每天一换）。

### 如何创建一个GitHub Pages来部署静态网站
* Settings -> Pages -> Build and deployment, Sorce选择Github Actions，选择静态HTML网站，然后yml文件选择`./github/workflows/static.yml`。
