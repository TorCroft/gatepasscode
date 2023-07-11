# Use the REST API to interact with workflows in GitHub Actions
You can use the REST API to view workflows for a repository in GitHub Actions. Workflows automate your software development life cycle with a wide range of tools and services.<br>
These endpoints are available for authenticated users, OAuth Apps, and GitHub Apps. Access tokens require `repo` scope for private repositories and `public_repo` scope for public repositories. GitHub Apps must have the actions permission to use these endpoints.<br>For more information, see [REST-API-Workflows](https://docs.github.com/en/rest/actions/workflows?apiVersion=2022-11-28).

## Create a workflow dispatch event
You can use this endpoint to manually trigger a GitHub Actions workflow run. You can replace `workflow_id` with the workflow file name. For example, you could use `main.yaml`.

| Header parameters  | Info | Required |
|:-------------:|:-------------:|:---------:|
| `access_token`  | Github Access token. Access tokens require `repo` scope for private repositories and `public_repo` scope for public repositories. | Yes |

| Path parameters  | Info | Required |
|:-------------:|:-------------:|:---------:|
| `owner`  | The account owner of the repository. The name is not case sensitive. | Yes |
| `repo`  | The name of the repository without the .git extension. The name is not case sensitive. | Yes |
| `workflow_id`  | The ID of the workflow. You can also pass the workflow file name as a string. | Yes |

| Body parameters  | Info | Required |
|:-------------:|:-------------:|:---------:|
| `ref`  | The git reference for the workflow. The reference can be a branch or tag name. | Yes |
| `inputs`  | Input keys and values configured in the workflow file. The maximum number of properties is 10. Any default properties configured in the workflow file will be used when inputs are omitted. | No |


## Here is an Example in Python
``` Python
from requests import post

def create_a_workflow_dispatch_event(owner: str, repo: str, access_token: str, workflow_id: str, ref: str = 'main', **inputs):
    response = post(
        url=f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches",
        headers={
            'Accept': 'application/vnd.github+json',
            'Authorization': f'token {access_token}',
            'X-GitHub-Api-Version': '2022-11-28'
        },
        json={
            'ref': ref,
            'inputs': inputs
        }
    )
    if response.status_code == 204:
        print('Workflow is successfully requested.')
    else:
        print(f'{response.status_code} {response.reason}')


if __name__ == "__main__":
    create_a_workflow_dispatch_event(
        owner='TorCroft',
        repo='gatepasscode',
        access_token='Your github access token',
        workflow_id='main.yml'
    )

```

## Create a workflow dispatch event via iOS Shortcuts
* 创建一个json文件存放你所有的Workflow信息，下面是一个示例，取名为`config.json`。
``` json
{
    "EpicGamesHelper": {
        "owner": "TorCroft",
        "repo": "EpicGamesHelper",
        "workflowID": "55830746",
        "token": "Your github access token",
        "ref": "main"
    },
    "GatePasscode": {
        "owner": "TorCroft",
        "repo": "gatepasscode",
        "workflowID": "51821099",   // "main.yml" also works.
        "token": "Your github access token",
        "ref": "main"
    },
    "name_of_your_Workflow": {
        "owner": "",
        "repo": "",
        "workflowID": "",
        "token": "Your github access token",
        "ref": "main"
    }
}
```
* 将上述`config.json`存放到[iCloud Drive](https://www.icloud.com.cn/iclouddrive/)中，例如，我存放的路径为`iCloudDrive > Shortcuts Config > config`。
* 在你的iOS设备上[添加捷径](https://www.icloud.com/shortcuts/1e47d37b0cbd41a8b8e213bfec2b7661)，指定`config.json`的文件路径，然后保存即可。
![](https://github.com/TorCroft/gatepasscode/blob/main/README_IMAGES/shortcuts_eg.png)
