from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.identity import DefaultAzureCredential
import os


def upload_file_to_blob(account_name, container_name, file_path, blob_name):
    try:
        credential = DefaultAzureCredential()

        account_url = f"https://{account_name}.blob.core.windows.net/"
        blob_service_client = BlobServiceClient(account_url=account_url, credential=credential)

        # Create the container if it does not exist
        container_client = blob_service_client.get_container_client(container_name)
        if not container_client.exists():
            print(f"Container '{container_name}' does not exist. Creating new container.")
            container_client.create_container()

        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        # check if the file exists locally
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' does not exist.")
            return

        # Upload the file to the blob
        with open(file_path, "r") as file:
            blob_client.upload_blob(file.read(), overwrite=True)
            print(f"File '{file_path}' uploaded to Blob storage as '{blob_name}'.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    account_name = "your_account_name"
    container_name = "your_container_name"
    file_path = "path/to/your/local/file"
    blob_name = "your_blob_name" 

    upload_file_to_blob(account_name, container_name, file_path, blob_name)