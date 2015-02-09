#!/usr/bin/env python
import dosa
from subprocess import call, check_output
import random
import string
import urllib
import urllib2
import fileinput
import shutil
import os
import sys
import time
import re
from myconfig import *


# set variables
# dosa.set_debug()  # enables debug logs
client = dosa.Client(api_key=API_KEY)
HOME = os.environ['HOME']
os.environ['DO_TOKEN'] = API_KEY
os.environ['DISCOVERY_URL'] = urllib2.urlopen("https://discovery.etcd.io/new").read()
os.environ['NUM_OF_DROPLETS'] = str(CLUSTER_SIZE)

# get kubernetes' binaries
if not os.path.exists(HOME + "/bin"): os.mkdir(HOME + "/bin", 0755)
os.chdir(HOME + "/bin")
urllib.urlretrieve ("https://github.com/freeminder/deis_cluster_automation/raw/master/kubernetes-binaries.tar.gz", "kubernetes-binaries.tar.gz")
os.system("tar zxf kubernetes-binaries.tar.gz")
os.remove("kubernetes-binaries.tar.gz")

# create dirs and files
if not os.path.exists(HOME + "/.fleetctl"):
	os.mkdir(HOME + "/.fleetctl", 0755)
	open(HOME + '/.fleetctl/known_hosts', 'a').close()
if not os.path.exists(HOME + "/.ssh"):
	os.mkdir(HOME + "/.ssh", 0755)
	open(HOME + '/.ssh/known_hosts', 'a').close()
# create cluster
os.chdir(HOME)
os.system("git clone https://github.com/unicell/coreos-k8s-demo")
os.chdir("coreos-k8s-demo")
# patch original sources
os.system("sed -i s/512mb/4gb/ create_droplet.sh")
call(["sed", "-i", "s/603313/" + SSH_KEY_ID + "/", "create_droplet.sh"])
os.system("sed -i 's/i;/i \&\& sleep 15;/' bootstrap.sh")
# copy kubernetes binaries
if not os.path.exists("bin"): os.mkdir("bin", 0755)
os.system("cp ../bin/* bin/")
# bootstrap cluster
os.system("PATH=$PATH:~/bin ./bootstrap.sh")



# x = 1
# z = 0 - CLUSTER_SIZE
# kub_ip = client.droplets.list()[-1]["droplets"][z]["networks"]["v4"][0]["ip_address"]
# drupal_ip_list = list()
# while x <= CLUSTER_SIZE:
# 	# get host's public IP
# 	host_pub_ip = client.droplets.list()[-1]["droplets"][z]["networks"]["v4"][1]["ip_address"]
# 	# get host's private IP
# 	host_int_ip = client.droplets.list()[-1]["droplets"][z]["networks"]["v4"][0]["ip_address"]
# 	# remove old ssh public key fingerprints
# 	call(["ssh-keygen", "-R", host_pub_ip])
# 	# copy and run script, which will create local registry; build, tag and push drupal image; create pods
# 	call(["/usr/bin/scp", "-o StrictHostKeyChecking=no", "-o PasswordAuthentication=no", HOME + "/kubernetes_cluster_automation/host.sh", "core@" + host_pub_ip + ":~/"])
# 	if len(drupal_ip_list) == 0:
# 		call(["/usr/bin/ssh", "-o StrictHostKeyChecking=no", "-o PasswordAuthentication=no", "core@" + host_pub_ip, "bash host.sh", str(kub_ip), str(x)])
# 		# get drupal's pod IP
# 		drupal_ip_list.append("")
# 		while not re.match('10', str(drupal_ip_list[0])):
# 			out = check_output(["/usr/bin/ssh", "-o StrictHostKeyChecking=no", "-o PasswordAuthentication=no", "core@" + host_pub_ip, "/opt/bin/kubecfg -h http://" + kub_ip + ":8080 -json=true get pods/drupal" + str(x) + "|/opt/bin/jq '.currentState.podIP'|sed 's/\"//g'"])
# 			drupal_ip_list[0] = out.strip()
# 	else:
# 		call(["/usr/bin/ssh", "-o StrictHostKeyChecking=no", "-o PasswordAuthentication=no", "core@" + host_pub_ip, "bash host.sh", str(kub_ip), str(x), str(drupal_ip_list[0])])
# 		# get drupal's pod IP
# 		drupal_ip_list.append("")
# 		while not re.match('10', str(drupal_ip_list[x-1])):
# 			out = check_output(["/usr/bin/ssh", "-o StrictHostKeyChecking=no", "-o PasswordAuthentication=no", "core@" + host_pub_ip, "/opt/bin/kubecfg -h http://" + kub_ip + ":8080 -json=true get pods/drupal" + str(x) + "|/opt/bin/jq '.currentState.podIP'|sed 's/\"//g'"])
# 			drupal_ip_list[x-1] = out.strip()

# 	x += 1
# 	z += 1

