#!/bin/bash
KUB_IP=$1
DRUPAL_ID=$2


if [ $DRUPAL_ID == 1 ]
then
	# create local registry; build, tag and push drupal image
	git clone https://github.com/freeminder/kubernetes_cluster_automation && \
	kubernetes_cluster_automation/kubecfg -h http://$KUB_IP:8080 -c kubernetes_cluster_automation/pods/myregistry1.yaml create pods/ && \
	git clone https://github.com/freeminder/drupal_allin2 && \
	docker build -t drupal drupal_allin2 && docker tag drupal localhost:5000/drupal && docker push localhost:5000/drupal
	# create drupal pod
	kubernetes_cluster_automation/kubecfg -h http://$KUB_IP:8080 -c kubernetes_cluster_automation/pods/drupal$DRUPAL_ID.yaml create pods/
else
	# create local registry; build, tag and push drupal image
	git clone https://github.com/freeminder/kubernetes_cluster_automation && \
	mv kubernetes_cluster_automation/pods/myregistry1.yaml kubernetes_cluster_automation/pods/myregistry$DRUPAL_ID.yaml && \
	sed -i s/docker-registry1/docker-registry${DRUPAL_ID}/ kubernetes_cluster_automation/pods/docker-registry$DRUPAL_ID.yaml && \
	kubernetes_cluster_automation/kubecfg -h http://$KUB_IP:8080 -c kubernetes_cluster_automation/pods/myregistry$DRUPAL_ID.yaml create pods/ && \
	git clone https://github.com/freeminder/drupal_allin2 && \
	docker build -t drupal drupal_allin2 && docker tag drupal localhost:5000/drupal && docker push localhost:5000/drupal
	# create drupal pod
	mv kubernetes_cluster_automation/pods/drupal1.yaml kubernetes_cluster_automation/pods/drupal$DRUPAL_ID.yaml
	sed -i s/drupal1/drupal${DRUPAL_ID}/ kubernetes_cluster_automation/pods/drupal$DRUPAL_ID.yaml
	kubernetes_cluster_automation/kubecfg -h http://$KUB_IP:8080 -c kubernetes_cluster_automation/pods/drupal$DRUPAL_ID.yaml create pods/
fi
