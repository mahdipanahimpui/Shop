import boto3
from django.conf import settings
import os



class Bucket:
    """
    CDN Bucket manager

    init method creates connection

    NOTE:
        none of these mothods ar async. use public interface in tasks.py module instead.

    """
    def __init__(self):

        session = boto3.session.Session()

        self.connection = session.client(
            service_name=settings.AWS_SERVICE_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL
        )


    def get_objects(self):
        result = self.connection.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        if result['KeyCount']:
            return result['Contents']
        
        return None
    

    def deltete_object(self, key):
        self.connection.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
        return True # it is require to return True in not returned def, python return None automatically
    

    def download_object(self, key):
        path = os.path.join(settings.AWS_LOCAL_STORAGE, key)
        dir = os.path.dirname(path)
        file_name = os.path.basename(path)

        # Create directories if they don't exist
        os.makedirs(dir, exist_ok=True)

        # AWS_LOCAL_STORAGE used where to download
        with open(path , 'wb') as f:
            self.connection.download_fileobj(settings.AWS_STORAGE_BUCKET_NAME, key, f)


bucket = Bucket()