#!/bin/bash
KUB_IP=$1
HOST_ID=$2

if [ $HOST_ID == 1 ]
then
	cd ~
	rm -fr kubernetes_cluster_automation
	git clone https://github.com/freeminder/kubernetes_cluster_automation
	kubernetes_cluster_automation/kubecfg -h http://$KUB_IP:8080 -c kubernetes_cluster_automation/pods/myregistry1.yaml create pods/
else
	cd ~
	rm -fr kubernetes_cluster_automation
	git clone https://github.com/freeminder/kubernetes_cluster_automation
	mv kubernetes_cluster_automation/pods/myregistry1.yaml kubernetes_cluster_automation/pods/myregistry$HOST_ID.yaml && \
	sed -i s/docker-registry1/docker-registry${HOST_ID}/ kubernetes_cluster_automation/pods/myregistry$HOST_ID.yaml && \
	kubernetes_cluster_automation/kubecfg -h http://$KUB_IP:8080 -c kubernetes_cluster_automation/pods/myregistry$HOST_ID.yaml create pods/ && \
fi
