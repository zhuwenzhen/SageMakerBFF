"""
video_io.py
----------------
This file holds all the utilities to convert video to frame

@author Zhu, Wenzhen (zhu_wenzhen@icloud.com)
@date   09/15/2021
"""

import boto3
import logging
from botocore.exceptions import ClientError


def fetch_all_files(bucket_name, suffix, level=None, keyword=None):
    """
    Fetch all files with a specific suffix at a given level from S3 bucket
    :param bucket_name : str
        Name of the bucket
    :param suffix : str
        Suffix of files to fetch
        example: 'jpg', 'csv', 'xls', or '.jpg', '.csv', '.xls'
    :param level : int
        Specify which level's files
    :return: all files with given suffix in a proper level

    Example:
    To fetch all .txt files:
    >>> fetch_all_files(bucket_name, suffix='txt')
    To fetch all .txt files in level 3:
    >>> fetch_all_files(bucket_name, suffix='txt', level=3)
    To fetch all .txt files with 'ABBYY9' in the file name:
    >>> fetch_all_files(bucket_name, suffix='txt', keyword='ABBYY9')
    """
    s3 = boto3.resource("s3")
    s3_bucket = s3.Bucket(bucket_name)
    files = []
    for obj in s3_bucket.objects.all():
        key = obj.key
        if key.endswith(suffix):
            if keyword:
                if keyword in key:
                    files.append(key)
            else:
                files.append(key)

    if level:
        res = []
        for file in files:
            file2list = file.split("/")
            if len(file2list) == level + 1:
                res.append(file)
        return res
    else:
        return files


def upload_file(file_name, bucket, object_name=None):
    """
    Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client("s3")
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
