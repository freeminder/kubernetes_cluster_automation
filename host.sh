#!/bin/bash
KUB_IP=$1
DRUPAL_ID=$2

# create local registry; build, tag and push drupal image
mkdir -p ~/bin && cd ~/bin && export PATH=$PATH:~/bin && \
wget -q https://github.com/freeminder/deis_cluster_automation/raw/master/kubernetes-binaries.tar.gz && \
tar zxf kubernetes-binaries.tar.gz && rm -f kubernetes-binaries.tar.gz && \
cd && git clone https://github.com/freeminder/kubernetes_cluster_automation && \
kubecfg -h http://$KUB_IP:8080 -c kubernetes_cluster_automation/pods/myregistry.yaml create pods/ && \
git clone https://github.com/freeminder/drupal_allin2 && \
docker build -t drupal drupal_allin2 && docker tag drupal localhost:5000/drupal && docker push localhost:5000/drupal

# create pods
mv kubernetes_cluster_automation/pods/drupal1.yaml kubernetes_cluster_automation/pods/drupal$DRUPAL_ID.yaml
sed -i s/drupal1/drupal${DRUPAL_ID}/ kubernetes_cluster_automation/pods/drupal$DRUPAL_ID.yaml
kubecfg -h http://$KUB_IP:8080 -c kubernetes_cluster_automation/pods/drupal$DRUPAL_ID.yaml create pods/
# # get pod's IP
# kubecfg -h http://$KUB_IP:8080 -json=true get pods/drupal$DRUPAL_ID
