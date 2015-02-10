#!/bin/bash
DRUPAL_MASTER_CHECK=`docker ps|grep drupal1`
DRUPAL_ID=`docker ps|grep drupal:latest|awk '{print $1}'`
if [[ $DRUPAL_MASTER_CHECK == "" ]]
then
	sudo docker exec -i -t $DRUPAL_ID cp -f /var/www/sites/default/settings.orig /var/www/sites/default/settings.php
fi
