#!/usr/bin/env python

# Usage
#send_to_s3.py "<local_file_path>" "<s3_path>"

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('local_file_path', help="path to local file to be copied to s3")
parser.add_argument('s3_path', help="path to use inside s3 bucket 'home-0xdiag-datasets'")
args = parser.parse_args()

import sys
import os

# should just be one line, but you never know
with open('/home/hduser/.ec2/aws_id') as f:
    lines = f.read().splitlines()
aws_id = lines[0]
print "  Using aws_id:", aws_id

with open('/home/hduser/.ec2/aws_key') as f:
    lines = f.read().splitlines()
aws_key = lines[0]
print "  Using aws_key:", aws_key

from boto.s3.connection import S3Connection
from boto.s3.key import Key

# Initiate a S3 connection using key and secret
conn = S3Connection(aws_id, aws_key)

# The bucket name
bucket = 'home-0xdiag-datasets'
pb = conn.get_bucket(bucket)

# Make an S3 key using the bucket
k = Key(pb)
file_name_to_use_in_s3 = "%s/%s"%(args.s3_path, os.path.basename(args.local_file_path))
# Set the name of the file to use in S3
# S3 doesn't have the concept of directories
# Use / in the file name to mimic the directory path
k.name = file_name_to_use_in_s3
# Get the file from S3
k.get_contents_to_filename(args.local_file_path)
print "  Got %s to %s"%(file_name_to_use_in_s3, args.local_file_path)