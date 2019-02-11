#!/bin/bash

# mysql credentials
MYSQL_USER="mysql_username"
MYSQL_PASS="mysql_passowrd"

# dump all databases into temp folder
mysqldump -u "$MYSQL_USER" -p"$MYSQL_PASS"  --all-databases > /tmp/mysqldump.sql

# compress dump into filename with timestamp in name
nf=/tmp/mysqldump-$(date +%Y%m%d%H%M%S).zip
zip $nf /tmp/mysqldump.sql
rm /tmp/mysqldump.sql

# put into the S3 bucket
# s3cmd is free utility program for manage S3
# https://github.com/s3tools/s3cmd
s3cmd --storage-class=STANDARD_IA put $nf s3://bucket-mysql-dump

# remove local zipped dump file
rm $nf
