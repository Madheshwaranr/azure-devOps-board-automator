import pandas as pd
import json
import requests
import variable
import base64

# Step 1: Read Bug from Excel
def read_bug_from_excel(file_path):
    try:
        df = pd.read_excel(file_path)
        bug_data = []
        for index, row in df.iterrows():
            bug_data.append({'Title': row['Title']})
        return bug_data
    except Exception as e:
        print(f"Error reading bug data from Excel file: {e}")
        return []

# Step 2: Authenticate with Azure DevOps
def authenticate_azure_devops(pat):
    headers = {
        'Content-Type': 'application/json-patch+json',  # Update the Content-Type
        'Authorization': 'Basic ' + base64.b64encode(bytes(':' + variable.pat, 'ascii')).decode('ascii')
    }
    return headers

# Step 3: Create Bug in Azure DevOps
def create_bug_in_azure_devops(bug_data, headers, organization_url, project_name):
    url = f"{organization_url}/{project_name}/_apis/wit/workitems/$Bug?api-version=6.0"
    for bug in bug_data:
        payload = [
            {
                "op": "add",
                "path": "/fields/System.Title",
                "value": bug["Title"]
            }
        ]
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print(response.json()["id"])
        else:
            print(f"Failed to create bug '{bug["Title"]}'. Status code: {response.status_code}, Error: {response.text}")

if __name__ == "__main__":
    excel_file_path = 'sample.xlsx'  # Path to your Excel file
    azure_devops_pat = variable.pat # Replace with your PAT
    organization_url = 'https://dev.azure.com/your organization'  # Azure DevOps organization URL
    project_name = 'Your Project name'  # Project name

    # Step 1: Read Bug from Excel
    bug_titles = read_bug_from_excel(excel_file_path)
    if not bug_titles:
        print("No bug titles found in the Excel file. Exiting.")
        exit()

    # Step 2: Authenticate with Azure DevOps
    headers = authenticate_azure_devops(azure_devops_pat)

    # Step 3: Create Bug in Azure DevOps
    create_bug_in_azure_devops(bug_titles, headers, organization_url, project_name)