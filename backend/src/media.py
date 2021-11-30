#!/usr/bin/env python3

import os
import boto3
from botocore.exceptions import ClientError
from botocore.client import Config
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# constants
ACCESS_KEY_ID = str(os.environ.get("ACCESS_KEY_ID")).strip()
SECRET_ACCESS_KEY = str(os.environ.get("SECRET_ACCESS_KEY")).strip()
REGION_NAME = 'us-east-2'

# global Amazon S3 client
s3 = boto3.client('s3', region_name=REGION_NAME, endpoint_url=f'https://s3.{REGION_NAME}.amazonaws.com', config=Config(signature_version='s3v4'))

def create_presigned_url(object_name: str, expiration: int = 3600):
    """Generate a presigned URL to share an S3 object

    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    # Generate a presigned URL for the S3 object
    try:
        response = s3.generate_presigned_url('get_object',
                                                    Params={'Bucket': 'appdev-backend-final',
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        print(e)
        return None
    # The response contains the presigned URL
    return response

def upload(filename: str) -> None:
    with open(filename, "rb") as f:
        s3.upload_fileobj(f, 'appdev-backend-final', filename)

def main() -> None:
    upload("test.jpg")
    url = create_presigned_url("test.jpg")
    print(url)

if __name__ == '__main__':
    main()
