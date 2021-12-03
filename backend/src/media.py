#!/usr/bin/env python3
"""
Utility functions to convert a .mp4 file into HlS, upload to AWS, and remove
local .mp4 and HLS files, and more.

See this guide for bash implementation:
https://ryanparman.com/posts/2018/serving-bandwidth-friendly-video-with-hls/
"""

from pathlib import Path
import gzip
import integv
import os
import shutil
import subprocess
import sys
import boto3

def verify_mp4_integrity(mp4_file) -> bool:
    """
    Check the integrity of a .mp4 file

    :param mp4_file: The file obj to check
    :return: True if valid
    """
    return integv.verify(mp4_file, file_type="mp4")

def convert_mp4_to_hsl(path_to_mp4: str) -> str:
    """
    Convert a .mp4 file to a .fmp4 folder

    :param path_to_mp4: The path to the .mp4 file
    :return: Path to .fmp4 folder
    """
    # Remove file extension
    # path/to/file.mp4 -> path/to/file
    path_no_ext = os.path.splitext(path_to_mp4)[0]
    # Call git submodule containing python executable video2hls
    subprocess.run(["video2hls/video2hls", "--debug", "--output",
                    f"{path_no_ext}.fmp4", "--hls-type", "fmp4", f"{path_to_mp4}"])
    # Remove original .mp4
    os.remove(path_to_mp4)
    return f"{path_no_ext}.fmp4"

def compress_fmp4(path_to_fmp4: str) -> None:
    """
    Find all .m3u8 playlist files in a .fmp4 folder and gzip them.
    Maintains the original .m3u8 file extension.

    :param path_to_fmp4: The path to the .fmp4 file
    """
    # for all .m3u8 files
    for path in Path(path_to_fmp4).rglob('*.m3u8'):
        filepath = os.path.join(path_to_fmp4, path.name)
        # compress into .gz
        with open(filepath, 'rb') as f_in, gzip.open(filepath + '.gz', 'wb') as f_out:
            f_out.writelines(f_in)
        # overwrite original
        os.replace(filepath + '.gz', filepath)
    print("Compressed all files with gzip")

def upload_to_aws(s3, bucket_name: str, bucket_region: str, path_to_fmp4: str) -> str:
    """
    Upload all the necessary files for HLS support contained in a .fmp4 to AWS

    :s3: The boto3 S3 client
    :bucket_name: The name of the S3 bucket
    :bucket_region: The location of the S3 bucket
    :param path_to_fmp4: The path to the .fmp4 file
    :return: The .m3u8 URL hosted on AWS
    """
    # Get filename
    # path/to/dir.fmp4 -> dir.fmp4
    fmp4_filename = os.path.basename(path_to_fmp4)
    # Upload all .m3u8 files
    for path in Path(path_to_fmp4).rglob('*.m3u8'):
        filepath = os.path.join(path_to_fmp4, path.name)
        with open(filepath, 'rb') as f:
            key = path.name
            s3.upload_fileobj(f, bucket_name, f"hls/{fmp4_filename}/{key}",
                              ExtraArgs={'ContentType': 'application/vnd.apple.mpegurl',
                                         'ACL': 'public-read',
                                         'ContentEncoding': 'gzip',
                                         'CacheControl': 'max-age=31536000,public'
                                         })
    # Upload video "posters"
    for path in Path(path_to_fmp4).rglob('*.jpg'):
        filepath = os.path.join(path_to_fmp4, path.name)
        with open(filepath, 'rb') as f:
            key = path.name
            s3.upload_fileobj(f, bucket_name, f"hls/{fmp4_filename}/{key}",
                              ExtraArgs={'ContentType': 'image/jpeg',
                                         'ACL': 'public-read',
                                         'CacheControl': 'max-age=31536000,public'
                                         })
    # Upload fragmented .mp4 files
    for path in Path(path_to_fmp4).rglob('*.mp4'):
        filepath = os.path.join(path_to_fmp4, path.name)
        with open(filepath, 'rb') as f:
            key = path.name
            s3.upload_fileobj(f, bucket_name, f"hls/{fmp4_filename}/{key}",
                              ExtraArgs={'ContentType': 'video/mp4',
                                         'ACL': 'public-read',
                                         'CacheControl': 'max-age=31536000,public'
                                         })
    object_url = get_object_url(bucket_name, bucket_region, fmp4_filename)
    return object_url

def get_object_url(bucket_name: str, bucket_region: str, fmp4_filename: str) -> str:
    """ Get the index.m3u8's object URL for a specific HLS upload """
    return f"https://{bucket_name}.s3.{bucket_region}.amazonaws.com/hls/{fmp4_filename}/index.m3u8"

def remove_fmp4(path_to_fmp4: str) -> None:
    """
    Remove the .fmp4 folder

    :param path_to_fmp4: The path to the .fmp4 file
    """
    shutil.rmtree(path_to_fmp4)

def main() -> None:
    from botocore.client import Config
    from dotenv import load_dotenv
    # load environment variables
    load_dotenv()
    # constants
    ACCESS_KEY_ID = str(os.environ.get("ACCESS_KEY_ID")).strip()
    SECRET_ACCESS_KEY = str(os.environ.get("SECRET_ACCESS_KEY")).strip()
    REGION_NAME = 'us-east-2'
    BUCKET_NAME = 'appdev-backend-final'
    s3 = boto3.client('s3', region_name=REGION_NAME, endpoint_url=f'https://s3.{REGION_NAME}.amazonaws.com',
                  aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY,
                      config=Config(signature_version='s3v4'))
    if len(sys.argv) < 2:
        print("Usage: <FILENAME>.py path/to/file.mp4")
        return
    # The workflow
    path_to_mp4 = sys.argv[1]
    with open(path_to_mp4, 'rb') as f:
        if not verify_mp4_integrity(f):
            print("Corrupt MP4")
            return
    path_to_fmp4 = convert_mp4_to_hsl(path_to_mp4)
    compress_fmp4(path_to_fmp4)
    url = upload_to_aws(s3, BUCKET_NAME, REGION_NAME, path_to_fmp4)
    print(url)
    remove_fmp4(path_to_fmp4)

if __name__ == '__main__':
    main()
