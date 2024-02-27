import requests
import base64
import json
import variable_for_PAT_Token

# Azure DevOps organization URL
org_url = 'https://dev.azure.com/your organization'

# Project name
project = 'Your Project name'

# Parent PBI ID
parent_pbi_id = '155'  # Replace this with the actual ID of PBI 155

# Request headers
headers = {
    'Content-Type': 'application/json-patch+json',  # Update the Content-Type
    'Authorization': 'Basic ' + base64.b64encode(bytes(':' + variable_for_PAT_Token.pat, 'ascii')).decode('ascii')
}

# Bug details
bug_details = {
    'op': 'add',
    'path': '/fields/System.Title',
    'value': 'Sample Bug'  # Title of the bug
}

# Task details
task_details = {
    'op': 'add',
    'path': '/fields/System.Title',
    'value': 'Sample Task'  # Title of the task
}

# Work item details for the bug
bug_work_item = [
    bug_details,
    {
        'op': 'add',
        'path': '/relations/-',
        'value': {
            'rel': 'System.LinkTypes.Hierarchy-Reverse',
            'url': f'{org_url}/{project}/_apis/wit/workitems/{parent_pbi_id}',
            'attributes': {
                'comment': 'Added to PBI 155 test2'
            }
        }
    }
]

# API endpoint for creating a work item (bug)
bug_api_url = f'{org_url}/{project}/_apis/wit/workitems/$bug?api-version=6.0'

# Send POST request to create the bug
bug_response = requests.post(bug_api_url, headers=headers, json=bug_work_item)

# Check if the request was successful
if bug_response.status_code != 200:
    print("Failed to create bug:", bug_response.text)
    exit()

# Task work item details
task_work_item = [
    task_details,
    {
        'op': 'add',
        'path': '/relations/-',
        'value': {
            'rel': 'System.LinkTypes.Hierarchy-Reverse',
            'url': f'{org_url}/{project}/_apis/wit/workitems/{bug_response.json()["id"]}',
            'attributes': {
                'comment': 'Added to Bug created'
            }
        }
    }
]

# API endpoint for creating a work item (task)
task_api_url = f'{org_url}/{project}/_apis/wit/workitems/$task?api-version=6.0'

# Send POST request to create the task
task_response = requests.post(task_api_url, headers=headers, json=task_work_item)

# Check if the request was successful
if task_response.status_code != 200:
    print("Failed to create task:", task_response.text)
else:
    print("Task and Bug created successfully!")
