#!/usr/bin/env python
from subprocess import call
import random
import string
import urllib2
import fileinput
import shutil
import os
import sys
import time
from myconfig import *


# set variables
os.environ['DO_TOKEN'] = API_KEY
os.environ['DISCOVERY_URL'] = urllib2.urlopen("https://discovery.etcd.io/new").read()

# get kubernetes' binaries
os.system("mkdir ~/bin && pushd ~/bin && wget https://github.com/freeminder/deis_cluster_automation/raw/master/kubernetes-binaries.tar.gz && \
	tar zxf kubernetes-binaries.tar.gz && rm -f kubernetes-binaries.tar.gz && popd")

# create cluster
os.system("git clone https://github.com/unicell/coreos-k8s-demo")
os.chdir("coreos-k8s-demo")
os.system("sed -i 's/603313/534374/' create_droplet.sh")
os.system("PATH=$PATH:~/bin ./bootstrap.sh")

# get hosts' IPs
host1_ip = 
host2_ip = 

# create pods
os.system("git clone https://github.com/freeminder/drupal_allin2")
os.chdir("drupal_allin2")
os.system("kubecfg -c drupal.yaml create pods")
