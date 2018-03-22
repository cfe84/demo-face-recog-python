import azure.storage.blob as azureblob
import os
from datetime import datetime, timezone, timedelta

STORAGE_ACCOUNT = os.environ["STORAGE_ACCOUNT"]
ACCOUNT_KEY = os.environ["ACCOUNT_KEY"]
container_name = "people"

block_blob_service = azureblob.BlockBlobService(account_name=STORAGE_ACCOUNT, account_key=ACCOUNT_KEY)

def get_SAS_for_blob(block_blob_service, container_name, blob_name):
    sas_token = block_blob_service.generate_blob_shared_access_signature(container_name, blob_name, azureblob.BlobPermissions.READ, datetime.now(timezone.utc) + timedelta(hours=4))
    container_sas_url = "https://{}.blob.core.windows.net/{}?{}".format(STORAGE_ACCOUNT, container_name, sas_token)
    return container_sas_url

def create_SAS_for_all_files_in_container(block_blob_service, container_name):
    lst = block_blob_service.list_blobs(container_name)
    return map((lambda blob: get_SAS_for_blob(block_blob_service, container_name, blob.name)), lst)

urls = create_SAS_for_all_files_in_container(block_blob_service, container_name)

for url in urls:
    print(url)