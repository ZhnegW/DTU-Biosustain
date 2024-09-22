import json
from azure.identity import DefaultAzureCredential
from azure.loganalytics import LogAnalyticsDataClient
from azure.loganalytics.models import QueryBody

# Set Log Analytics workspace ID
workspace_id = "your-workspace-id"
credential = DefaultAzureCredential()

client = LogAnalyticsDataClient(credential=credential)

query = """
AzureDiagnostics
| where ResourceId == "/subscriptions/subscription-id/resourceGroups/rg-name/
providers/providerName/resourceType/resourceName"
| limit 10
"""
query_body = QueryBody(query=query)

# Query logs from the workspace
response = client.query(workspace_id=workspace_id, body=query_body)

if response.tables:
    table = response.tables[0]
    logs = []

    for row in table.rows:
        log_entry = dict(zip(table.columns, row))
        logs.append(log_entry)

    log_file = "azure_logs.json"
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=4)

    print(f"Logs saved to {log_file}")
else:
    print("No logs found.")
