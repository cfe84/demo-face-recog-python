# face_recognition

Demo of python face_recognition pulling and pushing to Azure Blob Storage for Azure Batch

This does the following:
```
+----------------------------+                         +-------------------------------+
|                            |                         |                               |
|                            |                         |                               |
|     Input Blob             |                         |        Output Blob            |
|                            | <---------+             |                               |
|                            |           |             |                               |
|                            |           |             |                               |
+-----------+----------------+           |             +--------------+----------------+
            ^                            |                            ^
            |                            +                            |
            |                     Retrieve using shared               +
        List|all blobs            access signature             Put using shared
            |                            +                     access signature
            |                            |                            +
            |                            |                            |
   +--------+-----------+                |                    +-------+-------+
   |    createTasks.py  |                +---------------------|launch.py     |
   +--------------------+                                     +---------------+
           Push|task for all blobs                          Execute all|tasks on nodes
               |                +----------------+                     |
               +-----------------> Azure Batch +-----------------------+
                                |                |
                                +----------------+

```

- You need to setup a pool using the tasks in setup.sh, using Ubuntu 16.04
- Update createTasks.py to use the pool id
- Upload pictures of people in a `people` container on your storage account
- Create a container called `output` in your storage account.
- Add environment variables:
    - STORAGE_ACCOUNT: account name
    - ACCOUNT_KEY: account key
    - BATCH_ACCOUNT_NAME, BATCH_ACCOUNT_URL, BATCH_ACCOUNT_KEY: pick from properties
- Zip all and deploy on Azure Batch as an application called `face_recognition`.
- Run `python3 createTasks.py` on your own machine, and wait.