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
        access_token='Your own github access token',
        workflow_id='main.yml'
    )

```

## Create a workflow dispatch event via iOS Shortcuts
![](https://github.com/TorCroft/gatepasscode/blob/main/README_IMAGES/shortcuts_eg_1.png)
* 这里的`Dictionary`包含你的Workflow信息，可存放多个Workflow，每个键值对以`string: dict`的形式存放。`string`是自己指定的的Workflow名称，`dict`是该Workflow需要包含的信息，包含`owner`, `repo`, `workflowID`, `token`, `ref` 五项。
### 这是一个Workflow示例
![](https://github.com/TorCroft/gatepasscode/blob/main/README_IMAGES/shortcuts_eg_2.png)
