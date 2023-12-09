from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os

connection_string = "ENTER_CONNECTION_STRING_HERE"  #
container_name = "langchaincontainer"
blob_name = "langchainstoragegroup"
directory_path = "Data"

blob_service_client = BlobServiceClient.from_connection_string(connection_string)

for root, dirs, files in os.walk(directory_path):
    for file in files:
        file_path = os.path.join(root, file)
        blob_name = os.path.relpath(file_path, directory_path)

        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=blob_name
        )

        with open(file_path, "rb") as data:
            blob_client.upload_blob(data)

        print(f"Data  {file_path} has been uploaded! {blob_name} under this blob!")
