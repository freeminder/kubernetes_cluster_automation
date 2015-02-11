#!/bin/bash

# find master drupal pod and backup settings
DRUPAL_MASTER_CHECK=`docker ps|grep drupal1`
DRUPAL_ID=`docker ps|grep drupal:latest|awk '{print $1}'`
if [[ $DRUPAL_MASTER_CHECK != "" ]]
then
	sleep 20
	sudo docker exec -i -t $DRUPAL_ID cp -f /var/www/sites/default/settings.php /var/www/sites/default/settings.orig
fi
