import requests
import base64
import json
import variable_for_PAT_Token

# Azure DevOps organization URL
org_url = 'https://dev.azure.com/your organization'

# Project name
project = 'Your Project name'

# Request headers
headers = {
    'Content-Type': 'application/json-patch+json',
    'Authorization': 'Basic ' + base64.b64encode(bytes(':' + variable_for_PAT_Token.pat, 'ascii')).decode('ascii')
}

# Create a PBI
pbi_details = {
    'op': 'add',
    'path': '/fields/System.Title',
    'value': 'Sample PBI'
}
pbi_api_url = f'{org_url}/{project}/_apis/wit/workitems/$Product Backlog Item?api-version=6.0'
pbi_response = requests.post(pbi_api_url, headers=headers, data=json.dumps([pbi_details]))

if pbi_response.status_code != 200:
    print("Failed to create PBI:", pbi_response.text)
    exit()

pbi_id = pbi_response.json()["id"]
print("Product Backlog Item created with ID:", pbi_id)


# Create a Bug under the PBI
bug_details = [
    {
        "op": "add",
        "path": "/fields/System.Title",
        "value": "Sample bug"
    },
    {
        "op": "add",
        "path": "/relations/-",
        "value": {
            "rel": "System.LinkTypes.Hierarchy-Reverse",
            "url": f"{org_url}/{project}/_apis/wit/workitems/{pbi_id}",
            "attributes": {
                "name": "Parent"
            }
        }
    }
]

bug_api_url = f'{org_url}/{project}/_apis/wit/workitems/$Bug?api-version=6.0'
bug_response = requests.post(bug_api_url, headers=headers, data=json.dumps(bug_details))

if bug_response.status_code != 200:
    print("Failed to create bug:", bug_response.text)
    exit()

bug_id = bug_response.json()["id"]
print("Bug created with ID:", bug_id)


# Create multiple tasks under the Bug
additional_tasks = ['test1', 'test2']

task_api_url = f'{org_url}/{project}/_apis/wit/workitems/$Task?api-version=6.0'

for task_title in additional_tasks:
    task_details = [
        {
            "op": "add",
            "path": "/fields/System.Title",
            "value": task_title
        },
        {
            "op": "add",
            "path": "/relations/-",
            "value": {
                "rel": "System.LinkTypes.Hierarchy-Reverse",
                "url": f"{org_url}/{project}/_apis/wit/workitems/{bug_id}",
                "attributes": {
                    "name": "Parent"
                }
            }
        }
    ]

    task_response = requests.post(task_api_url, headers=headers, data=json.dumps(task_details))

    if task_response.status_code != 200:
        print(f"Failed to create task '{task_title}':", task_response.text)
    else:
        print(f"Task '{task_title}' created successfully under Bug:", bug_id)