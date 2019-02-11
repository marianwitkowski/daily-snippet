<?php

/*
install mongodb PHP driver
https://github.com/mongodb/mongo-php-driver 
and include autoload.php 
*/
require_once "vendor/autoload.php";

error_reporting(E_ERROR);
set_time_limit(0);

/*
Generate private/public keys for encrypt backup file
openssl req -x509 -newkey rsa:2048 -keyout private-key.pem -nodes -out public-key.pem -subj "/CN=unused"
*/

$PUBLIC_KEY = "public-key.pem";

$connection_string = "mongodb://localhost:27017";
$client = new MongoDB\Client($connection_string);

foreach ($client->listDatabases() as $databaseInfo) {
    $db = $databaseInfo->getName();
    
    // create dump for database
    $cmd = "mongodump --quiet -d '$db' --out=/mnt/dump ";
    system($cmd);
    
    // compress dump
    $cmd = "tar -cvzf /mnt/dump/$db.tar.gz /mnt/dump/$db ";
    system($cmd);
    
    // delete plain dump
    $cmd = "rm -Rf /mnt/dump/$db ";
    system($cmd);
    
    // encrypt compressed dump
    $cmd = "openssl smime -encrypt -aes-256-cbc -binary -in /mnt/dump/$db.tar.gz -outform DER -out /mnt/dump/$db.tar.gz.enc $PUBLIC_KEY ";

    // put into the S3 bucket
    // s3cmd is free utility program for manage S3
    // https://github.com/s3tools/s3cmd
    $cmd = "s3cmd put /mnt/dump/$db.tar.gz.enc s3://dump-mongo-backup ";
    system($cmd);
    
    // clean unused files
    unlink("/mnt/dump/$db.tar.gz");
    unlink("/mnt/dump/$db.tar.gz.enc");
    
}

?>
