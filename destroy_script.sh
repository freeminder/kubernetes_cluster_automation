#!/bin/bash
KUB_IP=$1
HOST_ID=$2

cd ~
kubernetes_cluster_automation/kubecfg -h http://$KUB_IP:8080 delete pods/drupal$HOST_ID
kubernetes_cluster_automation/kubecfg -h http://$KUB_IP:8080 delete pods/docker-registry$HOST_ID
sleep 5
docker rmi -f drupal
docker rmi -f localhost:5000/drupal
sudo docker ps -a | grep Exit | awk '{print $1}' | sudo xargs docker rm
docker rmi -f localhost:5000/drupal
