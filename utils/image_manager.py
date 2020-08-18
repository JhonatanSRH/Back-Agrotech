from google.cloud import storage


#def upload_blob(path_file, img_name):
def upload_blob(path_file, img_name):
    try:
        path_file = "C:/Users/Jhonatan/Pictures"
        img_name = "uapisimo.jpg"
        """Uploads a file to the bucket."""
        # bucket_name = "your-bucket-name"
        # source_file_name = "local/path/to/file"
        # destination_blob_name = "storage-object-name"

        storage_client = storage.Client()
        bucket = storage_client.bucket("imgrepo")
        blob = bucket.blob(img_name)

        blob.upload_from_filename(path_file)

        print(
            "File {} uploaded to {}.".format(
                path_file, img_name
            )
        )
    except Exception as error:
        print(error)

"""
from google.cloud import storage
client = storage.Client()
bucket = storage.Bucket("my-bucket-name", user_project='my-project')
all_blobs = list(client.list_blobs(bucket))
"""
