import boto3
from botocore.exceptions import ClientError

from app.application.models.config import MinioSettings
from app.domain.files_gateway.entities import StoredFile
from app.domain.files_gateway.gateway import FilesGateway


class MinioGateway(FilesGateway):
    def __init__(self, config: MinioSettings) -> None:
        base_url = config.minio_url
        self.client = boto3.client(
            's3',
            endpoint_url=base_url,
            aws_access_key_id=config.minio_access_key,
            aws_secret_access_key=config.minio_secret_key,
            region_name="us-east-1"
        )

        self.bucket_name = "pdf-bucket"
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self) -> None:
        try:
            self.client.head_bucket(Bucket=self.bucket_name)
        except ClientError:
            self.client.create_bucket(Bucket=self.bucket_name)
            print(f"Bucket '{self.bucket_name}' created.")

    async def get_files(self) -> list[StoredFile]:
        response = self.client.list_objects_v2(Bucket=self.bucket_name)
        files = []

        for obj in response.get("Contents", []):
            key = obj["Key"]
            file_obj = self.client.get_object(Bucket=self.bucket_name, Key=key)
            file_bytes = file_obj["Body"].read()
            files.append(StoredFile(key, file_bytes))

        return files
