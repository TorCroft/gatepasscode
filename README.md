# gatepasscode
郑州大学主校区通行码，适配北门、东门、南门。

## Usage
Fork 本仓库，创建一个GitHUb Action(./github/workflows/main.yml)来更新每天的通行码。
需要四个secrets变量，分别为`UID_PWD`,`EMAIL`,`USERNAME`,`TOKEN`
* `UID_PWD`：
账号密码都是健康打卡平台的，将你的账号密码使用`#`拼接起来，exp: 你的账号是123456789，密码是password，那么`UID_PWD`的值应该是`123456789#password`，密码默认是身份证后八位。用于python脚本爬取新的通行码图片。
* `EMAIL,USERNAME`：
git使用的邮箱和GitHub用户名，具体请参考`./github/workflows/main.yml`，用于git push推送新的通行码图片到仓库（该图片每天一换）。
* `TOKEN`：
个人设置里面找到开发者选项，选择`Personal access tokens (classic)`。
### 如何生成密钥
* 在个人设置页面，找到Setting（参考）
* 选择开发者设置Developer setting
* 选择个人访问令牌Personal access tokens，然后选中生成令牌Generate new token
* 设置token的有效期，访问权限等，选择要授予此令牌token的范围或权限。我们需要勾选`repo`和`workflow`。
* 生成令牌Generate token。

### 如何创建一个GitHub Pages来部署静态网站
* Settings -> Pages -> Build and deployment, Sorce选择Github Actions，选择静态HTML网站，然后yml文件选择`./github/workflows/static.yml`。
