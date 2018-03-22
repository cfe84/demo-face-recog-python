import azure.storage.blob as azureblob
import os
from datetime import datetime, timezone, timedelta

STORAGE_ACCOUNT = os.environ["STORAGE_ACCOUNT"]
ACCOUNT_KEY = os.environ["ACCOUNT_KEY"]
INPUT_CONTAINER_NAME = "people"
OUTPUT_CONTAINER_NAME = "output"

block_blob_service = azureblob.BlockBlobService(account_name=STORAGE_ACCOUNT, account_key=ACCOUNT_KEY)

def get_SAS_for_container(block_blob_service, container_name):
    permission = azureblob.ContainerPermissions(read=False, write=True)
    sas_token = block_blob_service.generate_container_shared_access_signature(container_name, permission, datetime.now(timezone.utc) + timedelta(hours=4))
    return sas_token
    
def get_write_SAS_for_blob(block_blob_service, container_name, blob_name):
    token = get_SAS_for_container(block_blob_service, container_name)
    url = "https://{}.blob.core.windows.net/{}/{}?{}".format(STORAGE_ACCOUNT, container_name, blob_name, token)
    return url

def get_SAS_URL_for_blob(block_blob_service, container_name, blob_name):
    sas_token = block_blob_service.generate_blob_shared_access_signature(container_name, blob_name, azureblob.BlobPermissions.READ, datetime.now(timezone.utc) + timedelta(hours=4))
    container_sas_url = "https://{}.blob.core.windows.net/{}/{}?{}".format(STORAGE_ACCOUNT, container_name, blob_name, sas_token)
    return container_sas_url

def generate_task_for_blob(block_blob_service, blob_name):
    input_url = get_SAS_URL_for_blob(block_blob_service, INPUT_CONTAINER_NAME, blob_name)
    output_url = get_write_SAS_for_blob(block_blob_service, OUTPUT_CONTAINER_NAME, blob_name)
    command = "python3 launch.py \"{}\" \"{}\"".format(input_url, output_url)
    return command

def generate_tasks_for_all_blobs(block_blob_service):
    lst = block_blob_service.list_blobs(INPUT_CONTAINER_NAME)
    return map((lambda blob: generate_task_for_blob(block_blob_service, blob.name)), lst)

tasks = generate_tasks_for_all_blobs(block_blob_service)
for task in tasks:
    print(task)

print(get_write_SAS_for_blob(block_blob_service, "output", "something.jpg"))