import azure.storage.blob as azureblob
import azure.batch as azurebatch
import azure.batch.batch_auth as batchauth
import os
from datetime import datetime, timezone, timedelta
import time
import calendar

STORAGE_ACCOUNT = os.environ["STORAGE_ACCOUNT"]
ACCOUNT_KEY = os.environ["ACCOUNT_KEY"]
INPUT_CONTAINER_NAME = "people"
OUTPUT_CONTAINER_NAME = "output"
APP_PACKAGE_NAME = "face_recognition"

BATCH_ACCOUNT_NAME = os.environ["BATCH_ACCOUNT_NAME"]
BATCH_ACCOUNT_KEY = os.environ["BATCH_ACCOUNT_KEY"]
BATCH_ACCOUNT_URL = os.environ["BATCH_ACCOUNT_URL"]

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

def generate_command_for_blob(block_blob_service, blob_name):
    input_url = get_SAS_URL_for_blob(block_blob_service, INPUT_CONTAINER_NAME, blob_name)
    output_url = get_write_SAS_for_blob(block_blob_service, OUTPUT_CONTAINER_NAME, blob_name)
    command = "/bin/bash -c \"python3 $AZ_BATCH_APP_PACKAGE_{}/launch.py \'{}\' \'{}\'\"".format(APP_PACKAGE_NAME, input_url, output_url)
    return command

def generate_commands_for_all_blobs(block_blob_service):
    lst = block_blob_service.list_blobs(INPUT_CONTAINER_NAME)
    return list(map((lambda blob: generate_command_for_blob(block_blob_service, blob.name)), lst))


def create_job(batch_service_client, job_id, pool_id):
    job = azurebatch.models.JobAddParameter(
        job_id,
        azurebatch.models.PoolInformation(pool_id=pool_id))
    batch_service_client.job.add(job)
    
def enqueue_tasks(batch_service_client, job_id, commands):
    print('Adding {} tasks to job [{}]...'.format(len(commands), job_id))

    tasks = list()

    idx = 0

    for command in commands: 
        tasks.append(azurebatch.models.TaskAddParameter(
            id='Task{}'.format(idx),
            command_line=command,
            application_package_references=[azurebatch.models.ApplicationPackageReference(APP_PACKAGE_NAME)]
            )
        )
        idx = idx + 1
    batch_service_client.task.add_collection(job_id, tasks)

batch_credentials = batchauth.SharedKeyCredentials(BATCH_ACCOUNT_NAME,
                                                   BATCH_ACCOUNT_KEY)
batch_client = azurebatch.BatchServiceClient(
    batch_credentials,
    base_url=BATCH_ACCOUNT_URL)

jobid = "Job-{}".format(calendar.timegm(time.gmtime()))
commands = generate_commands_for_all_blobs(block_blob_service)
create_job(batch_client, jobid, "face_rec")
enqueue_tasks(batch_client, jobid, commands)