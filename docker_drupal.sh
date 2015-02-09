#!/bin/bash
KUB_IP=$1
HOST_ID=$2
MYSQL_MASTER=$3

if [ $HOST_ID == 1 ]
then
	# build, tag and push drupal image
	cd ~
	rm -fr drupal_allin
	git clone https://github.com/freeminder/drupal_allin
	docker build -t drupal drupal_allin && sleep 20 && docker tag drupal localhost:5000/drupal && docker push localhost:5000/drupal
	# create drupal pod
	kubernetes_cluster_automation/kubecfg -h http://$KUB_IP:8080 -c kubernetes_cluster_automation/pods/drupal$HOST_ID.yaml create pods/
	# patch drupal settings
	sleep 20
	DRUPAL_ID=`docker ps|grep drupal:latest|awk '{print $1}'`
	sudo docker exec -i -t $DRUPAL_ID cp -f /var/www/sites/default/settings.php /var/www/sites/default/settings.orig
else
	# replace IP of mysql master in drupal image; build, tag and push drupal image
	cd ~
	rm -fr drupal_allin
	git clone https://github.com/freeminder/drupal_allin
	if [[ $MYSQL_MASTER == *"10"* ]]
	then
		sed -i s/gcomm\\:\\/\\//gcomm\\:\\/\\/${MYSQL_MASTER}/ drupal_allin/my.cnf;
	fi
	docker build -t drupal drupal_allin && docker tag drupal localhost:5000/drupal && docker push localhost:5000/drupal
	# create drupal pod
	cd ~
	mv kubernetes_cluster_automation/pods/drupal1.yaml kubernetes_cluster_automation/pods/drupal$HOST_ID.yaml
	pwd
	sed -i s/drupal1/drupal${HOST_ID}/ kubernetes_cluster_automation/pods/drupal$HOST_ID.yaml
	kubernetes_cluster_automation/kubecfg -h http://$KUB_IP:8080 -c kubernetes_cluster_automation/pods/drupal$HOST_ID.yaml create pods/
	# patch drupal settings
	sleep 120
	DRUPAL_ID=`docker ps|grep drupal:latest|awk '{print $1}'`
	sudo docker exec -i -t $DRUPAL_ID cp -f /var/www/sites/default/settings.orig /var/www/sites/default/settings.php
fi
