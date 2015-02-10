#!/bin/bash
KUB_IP=$1
CLUSTER_SIZE=$2
x=1

while [[ $x -le $CLUSTER_SIZE ]]; do
	~/kubernetes_cluster_automation/bin/kubecfg -h http://$KUB_IP:8080 delete pods/drupal$x
	~/kubernetes_cluster_automation/bin/kubecfg -h http://$KUB_IP:8080 delete pods/docker-registry$x
	~/kubernetes_cluster_automation/bin/kubecfg -h http://$KUB_IP:8080 delete pods/haproxy$x
	x=$((x+1))
done

DRUPAL_IMAGES=`docker images|grep drupal|wc -l`
DRUPAL_PS=`docker ps|grep drupal:latest|awk '{print $1}'`
while [[ $DRUPAL_IMAGES != 0 ]]; do
	docker rm -f $DRUPAL_PS
	sudo docker ps -a | grep Exit | awk '{print $1}' | sudo xargs docker rm -f > /dev/null 2>&1
	docker rmi -f drupal
	docker rmi -f localhost:5000/drupal
	DRUPAL_IMAGES=`docker images|grep drupal|wc -l`
	DRUPAL_PS=`docker ps|grep drupal:latest|awk '{print $1}'`
done
