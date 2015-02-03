#!/usr/bin/env python
import dosa
from subprocess import call
import random
import string
import urllib
import urllib2
import fileinput
import shutil
import os
import sys
import time
from myconfig import *


# set variables
# dosa.set_debug()  # enables debug logs
client = dosa.Client(api_key=API_KEY)
HOME = os.environ['HOME']
os.environ['DO_TOKEN'] = API_KEY
os.environ['DISCOVERY_URL'] = urllib2.urlopen("https://discovery.etcd.io/new").read()

# get kubernetes' binaries
if not os.path.exists(HOME + "/bin"): os.mkdir(HOME + "/bin", 0755)
os.chdir(HOME + "/bin")
urllib.urlretrieve ("https://github.com/freeminder/deis_cluster_automation/raw/master/kubernetes-binaries.tar.gz", "kubernetes-binaries.tar.gz")
os.system("tar zxf kubernetes-binaries.tar.gz")
os.remove("kubernetes-binaries.tar.gz")

# create cluster
os.chdir(HOME)
os.system("git clone https://github.com/unicell/coreos-k8s-demo")
os.chdir("coreos-k8s-demo")
call(["sed", "-i", "s/603313/" + SSH_KEY_ID + "/", "create_droplet.sh"])
os.system("PATH=$PATH:~/bin ./bootstrap.sh")



x = 1
z = 0 - CLUSTER_SIZE
while x <= CLUSTER_SIZE:
	# get host's public IP
	host_pub_ip = client.droplets.list()[-1]["droplets"][z]["networks"]["v4"][1]["ip_address"]
	# get host's private IP
	host_int_ip = client.droplets.list()[-1]["droplets"][z]["networks"]["v4"][0]["ip_address"]
	# remove old ssh public key fingerprints
	call(["ssh-keygen", "-R", host_pub_ip])
	# create local registry
	call(["/usr/bin/ssh", "-o StrictHostKeyChecking=no", "-o PasswordAuthentication=no", "core@" + host_pub_ip, "git clone https://github.com/freeminder/kubernetes_cluster_automation"])
	call(["/usr/bin/ssh", "-o StrictHostKeyChecking=no", "-o PasswordAuthentication=no", "core@" + host_pub_ip, "kubecfg -c kubernetes_cluster_automation/pods/myregistry.yaml create pods/"])
	# build, tag and push drupal image
	call(["/usr/bin/ssh", "-o StrictHostKeyChecking=no", "-o PasswordAuthentication=no", "core@" + host_pub_ip, "git clone https://github.com/freeminder/drupal_allin2"])
	call(["/usr/bin/ssh", "-o StrictHostKeyChecking=no", "-o PasswordAuthentication=no", "core@" + host_pub_ip, "docker build -t drupal drupal_allin2 && docker tag drupal localhost:5000/drupal && docker push localhost:5000/drupal"])
	# create pods
	call(["/usr/bin/ssh", "-o StrictHostKeyChecking=no", "-o PasswordAuthentication=no", "core@" + host_pub_ip, "mv kubernetes_cluster_automation/pods/drupal1.yaml kubernetes_cluster_automation/pods/drupal" + str(x) + ".yaml"])
	call(["/usr/bin/ssh", "-o StrictHostKeyChecking=no", "-o PasswordAuthentication=no", "core@" + host_pub_ip, "sed -i s/drupal1/drupal" + str(x) + "/ kubernetes_cluster_automation/pods/drupal" + str(x) + ".yaml"])
	call(["/usr/bin/ssh", "-o StrictHostKeyChecking=no", "-o PasswordAuthentication=no", "core@" + host_pub_ip, "kubecfg -c kubernetes_cluster_automation/pods/drupal" + str(x) + ".yaml create pods/"])
	# get pod's IP
	# code to be written
	# ...
	x += 1
	z += 1


