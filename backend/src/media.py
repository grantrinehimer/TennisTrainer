#!/usr/bin/env python3

import os
import boto3
from botocore.exceptions import ClientError
from botocore.client import Config
from dotenv import load_dotenv
import requests  # For testing file uploading with presigned url.

# load environment variables
load_dotenv()

# constants
ACCESS_KEY_ID = str(os.environ.get("ACCESS_KEY_ID")).strip()
SECRET_ACCESS_KEY = str(os.environ.get("SECRET_ACCESS_KEY")).strip()
REGION_NAME = 'us-east-2'
BUCKET_NAME = 'appdev-backend-final'

# global Amazon S3 client
s3 = boto3.client('s3', region_name=REGION_NAME, endpoint_url=f'https://s3.{REGION_NAME}.amazonaws.com',
                  aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY,
                  config=Config(signature_version='s3v4'))


def create_presigned_url(object_name: str, expiration: int = 3600):
    """Generate a presigned URL to share an S3 object

    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    # Generate a presigned URL for the S3 object
    try:
        response = s3.generate_presigned_url('get_object',
                                             Params={'Bucket': BUCKET_NAME,
                                                     'Key': object_name},
                                             ExpiresIn=expiration)
    except ClientError as e:
        print(e)
        return None
    # The response contains the presigned URL
    return response


def create_presigned_url_post(object_name: str, expiration: int = 3600):
    """Generate a presigned URL that allows the client to upload a file using a POST request.

    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: dictionary containing url and pertinent information for POST request
    """

    try:
        response = s3.generate_presigned_post(BUCKET_NAME, object_name, ExpiresIn=expiration)
    except ClientError as e:
        print(e)
        return None

    return response


def upload(filename: str) -> None:
    with open(filename, "rb") as f:
        s3.upload_fileobj(f, BUCKET_NAME, filename)


def main() -> None:
    # Generate a presigned S3 POST URL
    object_name = 'test2.jpg'
    response = create_presigned_url_post(object_name)
    if response is None:
        exit(1)

    # Demonstrate how another Python program can use the presigned URL to upload a file
    with open(object_name, 'rb') as f:
        files = {'file': (object_name, f)}
        http_response = requests.post(response['url'], data=response['fields'], files=files)
    # If successful, returns HTTP status code 204
    print(f'File upload HTTP status code: {http_response.status_code}')


if __name__ == '__main__':
    main()
