#!/bin/bash
KUB_IP=$1
HOST_ID=$2

~/kubernetes_cluster_automation/bin/kubecfg -h http://$KUB_IP:8080 delete pods/drupal$HOST_ID
~/kubernetes_cluster_automation/bin/kubecfg -h http://$KUB_IP:8080 delete pods/docker-registry$HOST_ID

DRUPAL_IMAGES=`docker images|grep drupal|wc -l`
while [[ $DRUPAL_IMAGES != 0 ]]; do
	docker rmi -f drupal
	docker rmi -f localhost:5000/drupal
	sudo docker ps -a | grep Exit | awk '{print $1}' | sudo xargs docker rm -f
done

# DOCKER_PS=`docker ps|grep drupal:latest|wc -l`
# while [[ $DOCKER_PS != 0 ]]; do
# 	docker rm -f $DOCKER_PS
# 	sudo docker ps -a | grep Exit | awk '{print $1}' | sudo xargs docker rm -f
# done
