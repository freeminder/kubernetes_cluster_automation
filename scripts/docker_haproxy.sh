#!/bin/bash
KUB_IP=$1
HOST_ID=$2
DRUPAL_PODS_IP_ARRAY=( `echo $3|sed s/\'//g|sed s/\,//g|sed s/\\\[//g|sed s/\\\]//g` )

cd ~
rm -fr lb_haproxy
git clone https://github.com/freeminder/lb_haproxy
# patch haproxy settings
x=1
while [ $x -le ${#DRUPAL_PODS_IP_ARRAY[*]} ]; do
	DRUPAL_LINES_ARRAY=("${DRUPAL_LINES_ARRAY[@]}" "server drupal${x} ${DRUPAL_PODS_IP_ARRAY[$x-1]}\\:80 weight 100 maxconn 84 check inter 10s\n ")
	x=$((x+1))
done
sed -i s/\\#change\\_me/"${DRUPAL_LINES_ARRAY[*]}"/ lb_haproxy/haproxy.cfg
# build, tag and push haproxy image
docker build -t haproxy lb_haproxy && docker tag haproxy localhost:5000/haproxy && docker push localhost:5000/haproxy
# create haproxy pod
cd ~
mv kubernetes_cluster_automation/pods/haproxy1.yaml kubernetes_cluster_automation/pods/haproxy$HOST_ID.yaml
pwd
sed -i s/haproxy1/haproxy${HOST_ID}/ kubernetes_cluster_automation/pods/haproxy$HOST_ID.yaml
kubernetes_cluster_automation/bin/kubecfg -h http://$KUB_IP:8080 -c kubernetes_cluster_automation/pods/haproxy$HOST_ID.yaml create pods/
