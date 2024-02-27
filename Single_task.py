
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
    'Content-Type': 'application/json-patch+json',  # Update the Content-Type
    'Authorization': 'Basic ' + base64.b64encode(bytes(':' + variable_for_PAT_Token.pat, 'ascii')).decode('ascii')
}

# Work item details
work_item = [
    {
        'op': 'add',
        'path': '/fields/System.Title',
        'value': 'Sample Task'  # Title of the task
    }
]

# API endpoint for creating a work item
api_url = f'{org_url}/{project}/_apis/wit/workitems/$task?api-version=6.0'

# Send POST request to create a work item
response = requests.post(api_url, headers=headers, json=work_item)

# Check if the request was successful
if response.status_code == 200:
    print("Task created successfully!")
else:
    print("Failed to create task:", response.text)
