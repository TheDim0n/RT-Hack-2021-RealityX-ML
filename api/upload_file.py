import boto3

from .config import Settings

def upload_file(source: str, camera: str, filename: str, weights: str):
    settings = Settings()
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net/',
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )
    s3.upload_file(source, "reality-x", f"{weights}_preds/{camera}/{filename}")
    return f"https://s3.yandexcloud.net/reality-x/{weights}_preds/{camera}/{filename}"
