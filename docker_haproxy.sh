#!/bin/bash
KUB_IP=$1
HOST_ID=$2
ARRAY_OF_DRUPALS=$3

cd ~
rm -fr lb_haproxy
git clone https://github.com/freeminder/lb_haproxy
sed -i s/gcomm\\:\\/\\//gcomm\\:\\/\\/${ARRAY_OF_DRUPALS}/ lb_haproxy/haproxy.cfg
docker build -t haproxy lb_haproxy && docker tag haproxy localhost:5000/haproxy && docker push localhost:5000/haproxy
# create haproxy pod
cd ~
mv kubernetes_cluster_automation/pods/haproxy1.yaml kubernetes_cluster_automation/pods/haproxy$HOST_ID.yaml
pwd
sed -i s/haproxy1/haproxy${HOST_ID}/ kubernetes_cluster_automation/pods/haproxy$HOST_ID.yaml
kubernetes_cluster_automation/kubecfg -h http://$KUB_IP:8080 -c kubernetes_cluster_automation/pods/haproxy$HOST_ID.yaml create pods/
# patch haproxy settings
# sleep 120
# HAPROXY_ID=`docker ps|grep haproxy:latest|awk '{print $1}'`
# sudo docker exec -i -t $HAPROXY_ID cp -f /var/www/sites/default/settings.orig /var/www/sites/default/settings.php
