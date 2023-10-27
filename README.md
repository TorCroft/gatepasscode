# gatepasscode
郑州大学主校区通行码，适配北门、东门、南门。

* 本仓库的GitHub Action的触发器中不再包含定时器，本人只在需要时运行Action更新通行码图片。iOS可使用[Shortcuts](https://apps.apple.com/app/shortcuts/id915249334) APP，利用API触发。这里给出示例 [API触发Workflow](https://github.com/TorCroft/gatepasscode/blob/main/How-to-Run-Workflow-via-API.md) ，示例中包含使用Python和Shortcuts请求API触发Workflow。
### [GitHub Pages 部署成果](https://190854876.github.io/gatepasscode/)
![示例](https://github.com/TorCroft/gatepasscode/blob/main/README_IMAGES/WebsitePreview.png)

## Usage
Fork 本仓库，创建一个GitHUb Action(./github/workflows/main.yml)来更新每天的通行码。
需要三个secrets变量，分别为`UID_PWD`,`EMAIL`,`USERNAME`。
* `UID_PWD`：账号密码都是健康打卡平台的，将你的账号密码使用`&`拼接起来。<br>Exp: 你的账号是123456789，密码是password，那么`UID_PWD`的值应该是`123456789&password`，密码默认是身份证后八位。用于Python脚本爬取新的通行码图片。
* `EMAIL`：git使用的邮箱，具体请参考`./github/workflows/main.yml`，用于git push推送新的通行码图片到仓库（该图片每天一换）。
* `USERNAME`:GitHub的用户名，用于git push推送新的通行码图片到仓库（该图片每天一换）。

<br>![示例](https://github.com/TorCroft/gatepasscode/blob/main/README_IMAGES/secrets.jpg)

### 如何创建一个GitHub Pages来部署静态网站
* Settings -> Pages -> Build and deployment
* Source选择`Github Actions`，选择`Static HTML`<br>![](https://github.com/TorCroft/gatepasscode/blob/main/README_IMAGES/page.jpg)
* 要指定的yml设置为如下内容
``` yml
# Simple workflow for deploying static content to GitHub Pages
name: Deploy HTML to Pages

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
          # Upload ./page
          path: './page'
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v2
```
### 注意
* 如需要定时器，请自行在Action`Update passcode image`中的`on`添加以下代码
``` yaml
  schedule:
    - cron: '0 20 * * *'
```
修改后为
``` yaml
on:
  # 手动触发入口
  workflow_dispatch:
  # 定时器，UTC时间每天的20:00
  schedule:
    - cron: '0 20 * * *'
```
* 在`deploy-github-pages.yml`中添加了workflow_run触发器，Action `Update passcode image`运行完毕后会触发`Deploy HTML to Pages`的运行。
