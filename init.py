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
# os.system("sed -i s/512mb/4gb/ create_droplet.sh")
call(["sed", "-i", "s/603313/" + SSH_KEY_ID + "/", "create_droplet.sh"])
os.system("PATH=$PATH:~/bin ./bootstrap.sh")



x = 1
z = 0 - CLUSTER_SIZE
kub_ip = client.droplets.list()[-1]["droplets"][z]["networks"]["v4"][0]["ip_address"]
while x <= CLUSTER_SIZE:
	# get host's public IP
	host_pub_ip = client.droplets.list()[-1]["droplets"][z]["networks"]["v4"][1]["ip_address"]
	# get host's private IP
	host_int_ip = client.droplets.list()[-1]["droplets"][z]["networks"]["v4"][0]["ip_address"]
	# remove old ssh public key fingerprints
	call(["ssh-keygen", "-R", host_pub_ip])
	# create local registry; build, tag and push drupal image; create pods
	call(["/usr/bin/scp", "-o StrictHostKeyChecking=no", "-o PasswordAuthentication=no", HOME + "/kubernetes_cluster_automation/host.sh", "core@" + host_pub_ip + ":~/"])
	call(["/usr/bin/ssh", "-o StrictHostKeyChecking=no", "-o PasswordAuthentication=no", "core@" + host_pub_ip, "bash host.sh", str(kub_ip), str(x)])
	# get pod's IP
	pods_ip_list = list()
	pods_ip_list.append(call(["/usr/bin/ssh", "-o StrictHostKeyChecking=no", "-o PasswordAuthentication=no", "core@" + host_pub_ip, "PATH=$PATH:/opt/bin kubecfg -h http://" + kub_ip + ":8080 -json=true get pods/drupal" + str(x) + "|PATH=$PATH:/opt/bin jq '.currentState.podIP'|sed 's/\"//g'"]))

	x += 1
	z += 1

print(pods_ip_list)
