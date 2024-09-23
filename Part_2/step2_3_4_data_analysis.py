from azure.storage.blob import BlobServiceClient
# from azure.storage.filedatalake import DataLakeServiceClient
from azure.identity import DefaultAzureCredential
import pandas as pd
from io import StringIO

# step 2: read data from azure storage account

account_name = "dataengineerv1"
container_name = "raw"
blob_name = "tourism_dataset.csv"

credential = DefaultAzureCredential()

account_url = f"https://{account_name}.blob.core.windows.net/"
blob_service_client = BlobServiceClient(account_url=account_url, credential=credential)
container_client = blob_service_client.get_container_client(container_name)
blob_client = container_client.get_blob_client(blob=blob_name)

blob_data = blob_client.download_blob().readall()

csv_data = StringIO(blob_data.decode('utf-8'))
df = pd.read_csv(csv_data)

print(df.head())

# step 3: perform data analysis

# group and aggregate data
average_rate_by_country = df.groupby('Country')['Rating'].mean().reset_index()

average_rate_by_country.columns = ['Country', 'Average_Rating_by_Country']

"""
SELECT Country, AVG(Rating) AS Average_Rating_by_Country
FROM tourism_dataset
GROUP BY country;
"""

# indentify top categories
average_rate_by_category = df.groupby('Category')['Rating'].mean().reset_index()
average_rate_by_category.columns = ['Category', 'Average_Rating_by_Category']
average_rate_by_category = average_rate_by_category.sort_values(by='Average_Rating_by_Category', ascending=False).reset_index(drop=True)
top_3_categories = average_rate_by_category.head(3)

for index, row in top_3_categories.iterrows():
    print(f"Top {index+1} Category: {row['Category']}, Rate: {row['Average_Rating_by_Category']}")

"""
SELECT Category, AVG(Rating) AS Average_Rating_by_Category
FROM tourism_dataset
GROUP BY category
ORDER BY Average_Rating DESC
LIMIT 3;
"""

# Step 4 export results and save to VM

# integrate results
final_results = pd.concat([average_rate_by_country, average_rate_by_category], axis=1)

# write results to csv
container_name = "zheng-wang"
blob_name = "Zheng-Wang/Zheng-Wang.csv"
csv_string = final_results.to_csv(index=False)
csv_bytes = str.encode(csv_string)

# upload to Azure Storage
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
blob_client.upload_blob(csv_bytes, overwrite=True)