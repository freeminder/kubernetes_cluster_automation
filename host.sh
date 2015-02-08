#!/bin/bash
KUB_IP=$1
HOST_ID=$2
MYSQL_MASTER=$3

if [ $HOST_ID == 1 ]
then
	# create local registry; build, tag and push drupal image
	git clone https://github.com/freeminder/kubernetes_cluster_automation && \
	kubernetes_cluster_automation/kubecfg -h http://$KUB_IP:8080 -c kubernetes_cluster_automation/pods/myregistry1.yaml create pods/ && \
	git clone https://github.com/freeminder/drupal_allin2 && \
	docker build -t drupal drupal_allin2 && docker tag drupal localhost:5000/drupal && docker push localhost:5000/drupal
	# create drupal pod
	kubernetes_cluster_automation/kubecfg -h http://$KUB_IP:8080 -c kubernetes_cluster_automation/pods/drupal$HOST_ID.yaml create pods/
else
	# create local registry
	git clone https://github.com/freeminder/kubernetes_cluster_automation && \
	mv kubernetes_cluster_automation/pods/myregistry1.yaml kubernetes_cluster_automation/pods/myregistry$HOST_ID.yaml && \
	sed -i s/docker-registry1/docker-registry${HOST_ID}/ kubernetes_cluster_automation/pods/myregistry$HOST_ID.yaml && \
	kubernetes_cluster_automation/kubecfg -h http://$KUB_IP:8080 -c kubernetes_cluster_automation/pods/myregistry$HOST_ID.yaml create pods/ && \
	# replace IP of mysql master in drupal image; build, tag and push drupal image
	git clone https://github.com/freeminder/drupal_allin2
	if [[ $MYSQL_MASTER == *"10"* ]]
	then
		sed -i s/gcomm\\:\\/\\//gcomm\\:\\/\\/${MYSQL_MASTER}/ drupal_allin2/my.cnf;
	fi
	docker build -t drupal drupal_allin2 && docker tag drupal localhost:5000/drupal && docker push localhost:5000/drupal
	# create drupal pod
	mv kubernetes_cluster_automation/pods/drupal1.yaml kubernetes_cluster_automation/pods/drupal$HOST_ID.yaml
	sed -i s/drupal1/drupal${HOST_ID}/ kubernetes_cluster_automation/pods/drupal$HOST_ID.yaml
	kubernetes_cluster_automation/kubecfg -h http://$KUB_IP:8080 -c kubernetes_cluster_automation/pods/drupal$HOST_ID.yaml create pods/
fi
