# gatepasscode
郑州大学主校区通行码，适配北门、东门、南门。<br>[GitHub Pages 部署成果](https://torcroft.github.io/gatepasscode/)<br>[![Update passcode image](https://github.com/TorCroft/gatepasscode/actions/workflows/main.yml/badge.svg)](https://github.com/TorCroft/gatepasscode/actions/workflows/main.yml)<br>[![Deploy static content to Pages](https://github.com/TorCroft/gatepasscode/actions/workflows/static.yml/badge.svg)](https://github.com/TorCroft/gatepasscode/actions/workflows/static.yml)

## Usage
Fork 本仓库，创建一个GitHUb Action(./github/workflows/main.yml)来更新每天的通行码。
需要三个secrets变量，分别为`UID_PWD`,`EMAIL`,`USERNAME`
* `UID_PWD`：账号密码都是健康打卡平台的，将你的账号密码使用`&`拼接起来。<br>Exp: 你的账号是123456789，密码是password，那么`UID_PWD`的值应该是`123456789&password`，密码默认是身份证后八位。用于Python脚本爬取新的通行码图片。
* `EMAIL`：git使用的邮箱，具体请参考`./github/workflows/main.yml`，用于git push推送新的通行码图片到仓库（该图片每天一换）。
* `USERNAME`:GitHub的用户名，用于git push推送新的通行码图片到仓库（该图片每天一换）。

<br>![示例](https://github.com/TorCroft/gatepasscode/blob/main/README_IMAGES/secrets.jpg)

### 如何创建一个GitHub Pages来部署静态网站
* Settings -> Pages -> Build and deployment
* Source选择`Github Actions`，选择`Static HTML`<br>![示例](https://github.com/TorCroft/gatepasscode/blob/main/README_IMAGES/page.jpg)
* 要指定的yml设置为如下内容
``` yml
# Simple workflow for deploying static content to GitHub Pages
name: Deploy static content to Pages

on:
  workflow_run:
    workflows: ["Update passcode image"]
    types:
      - completed
  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:

# Sets permissions of the GITHUB_TOKEN to allow deployment to GitHub Pages
permissions:
  contents: read
  pages: write
  id-token: write

# Allow only one concurrent deployment, skipping runs queued between the run in-progress and latest queued.
# However, do NOT cancel in-progress runs as we want to allow these production deployments to complete.
concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  # Single deploy job since we're just deploying
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Setup Pages
        uses: actions/configure-pages@v3
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v1
        with:
          # Upload entire repository
          path: './page'
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v2

```
### 注意
* 本仓库的GitHub Action是手动关闭的，本人只在需要时才运行Action更新通行码图片。
* ~~Action`Update passcode image`运行之后，需要运行`Deploy static content to Pages`才能推送更新后的内容到网站。所以我在`Deploy static content to Pages`中添加了定时器，UTC时间（比北京时间慢8小时）每天的20：25部署内容到网站，`Deploy static content to Pages`在开启的情况下UTC时间每天的20：00运行。~~
* 在`static.yml`中添加了workflow_run触发器，Action `Update passcode image`运行完毕后会触发`Deploy static content to Pages`的运行。
