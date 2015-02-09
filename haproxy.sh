#!/bin/sh
KUB_IP=$1
HOST_ID=$2
MYSQL_MASTER=$3

if [ $HOST_ID == 1 ]
then
	cd ~
	git clone https://github.com/freeminder/lb_haproxy && \
	# sed drupal hosts into haproxy.cfg
	docker build -t drupal drupal_allin2 && docker tag drupal localhost:5000/drupal && docker push localhost:5000/drupal
	lb_haproxy/kubecfg -h http://$KUB_IP:8080 -c lb_haproxy/pods/haproxy$HOST_ID.yaml create pods/
else
	cd ~
	git clone https://github.com/freeminder/lb_haproxy && \
	mv lb_haproxy/haproxy1.yaml lb_haproxy/haproxy$HOST_ID.yaml && \
	sed -i s/haproxy1/haproxy${HOST_ID}/ lb_haproxy/haproxy$HOST_ID.yaml && \

	docker build -t drupal drupal_allin2 && docker tag drupal localhost:5000/drupal && docker push localhost:5000/drupal
	lb_haproxy/kubecfg -h http://$KUB_IP:8080 -c lb_haproxy/pods/haproxy$HOST_ID.yaml create pods/
fi
