from pydantic_settings import BaseSettings


class MinioSettings(BaseSettings):
    minio_url: str
    minio_access_key: str
    minio_secret_key: str

class DatabaseSettings(BaseSettings):
    database_uri: str