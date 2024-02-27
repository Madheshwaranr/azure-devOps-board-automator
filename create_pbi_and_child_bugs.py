import requests
import base64
import json
import variable_for_PAT_Token

org_url = 'https://dev.azure.com/your organization'
project = 'Your Project name'
headers = {
    'Content-Type': 'application/json-patch+json',  # Updated content type
    'Authorization': 'Basic ' + base64.b64encode(bytes(':' + variable_for_PAT_Token.pat, 'ascii')).decode('ascii')
}

# Create the bug item payload with parent-child relationship
bug_item = [{
    'op': 'add',
    'path': '/fields/System.Title',
    'value': 'Sample Bug1',
    'relations': [
        {
            'rel': 'System.LinkTypes.Hierarchy-Reverse',
            'url': f'{org_url}/{project}/_apis/wit/workItems/63',  # ID of the Product Backlog work item
            'attributes': {
                'comment': 'Added as a child bug'
            }
        }
    ]
}]

api_url = f'{org_url}/{project}/_apis/wit/workitems/$Bug?api-version=6.0'

response = requests.post(api_url, headers=headers, json=bug_item)

print(response.status_code)
print(response.json())  # Print response body for debugging purposes