#!/usr/bin/env python
import dosa
from subprocess import call, check_output
import random, string, urllib, urllib2, fileinput, shutil, os, sys, time, re
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from myconfig import *

# set variables
# dosa.set_debug()  # enables debug logs
client = dosa.Client(api_key=API_KEY)
HOME = os.environ['HOME']
os.environ['DO_TOKEN'] = API_KEY
os.environ['DISCOVERY_URL'] = urllib2.urlopen("https://discovery.etcd.io/new").read()
os.environ['NUM_OF_DROPLETS'] = str(CLUSTER_SIZE)

z = 0 - CLUSTER_SIZE
kub_ip = client.droplets.list()[-1]["droplets"][z]["networks"]["v4"][0]["ip_address"]
drupal_ip_list = list()


# copy and run deployment script of local docker registry on each node
z = 0 - CLUSTER_SIZE
x = 1
while x <= CLUSTER_SIZE:
	# get host's public IP
	host_pub_ip = client.droplets.list()[-1]["droplets"][z]["networks"]["v4"][1]["ip_address"]
	# remove old ssh public key fingerprints
	call(["ssh-keygen", "-R", host_pub_ip])

	call(["/usr/bin/scp", "-o StrictHostKeyChecking=no", "-o PasswordAuthentication=no", HOME + "/kubernetes_cluster_automation/scripts/docker_registry.sh", "core@" + host_pub_ip + ":~/"])
	call(["/usr/bin/ssh", "-o StrictHostKeyChecking=no", "-o PasswordAuthentication=no", "core@" + host_pub_ip, "bash docker_registry.sh", str(kub_ip), str(x)])

	x += 1
	z += 1


# copy and run script, which will build, tag and push drupal image and also create pods
z = 0 - CLUSTER_SIZE
x = 1
while x <= CLUSTER_SIZE:
	# get host's public IP
	host_pub_ip = client.droplets.list()[-1]["droplets"][z]["networks"]["v4"][1]["ip_address"]
	call(["/usr/bin/scp", "-o StrictHostKeyChecking=no", "-o PasswordAuthentication=no", HOME + "/kubernetes_cluster_automation/scripts/docker_drupal.sh", "core@" + host_pub_ip + ":~/"])
	if len(drupal_ip_list) == 0:
		call(["/usr/bin/ssh", "-o StrictHostKeyChecking=no", "-o PasswordAuthentication=no", "core@" + host_pub_ip, "bash docker_drupal.sh", str(kub_ip), str(x)])
		# get drupal's pod IP
		drupal_ip_list.append("")
		while not re.match('10', str(drupal_ip_list[0])):
			out = check_output(["/usr/bin/ssh", "-o StrictHostKeyChecking=no", "-o PasswordAuthentication=no", "core@" + host_pub_ip, "/opt/bin/kubecfg -json=true get pods/drupal1 | /opt/bin/jq '.currentState.podIP'|sed 's/\"//g'"])
			drupal_ip_list[0] = out.strip()
	else:
		call(["/usr/bin/ssh", "-o StrictHostKeyChecking=no", "-o PasswordAuthentication=no", "core@" + host_pub_ip, "bash docker_drupal.sh", str(kub_ip), str(x), str(drupal_ip_list[0])])
		# get drupal's pod IP
		drupal_ip_list.append("")
		while not re.match('10', str(drupal_ip_list[x-1])):
			out = check_output(["/usr/bin/ssh", "-o StrictHostKeyChecking=no", "-o PasswordAuthentication=no", "core@" + host_pub_ip, "/opt/bin/kubecfg -h http://" + kub_ip + ":8080 -json=true get pods/drupal" + str(x) + "|/opt/bin/jq '.currentState.podIP'|sed 's/\"//g'"])
			drupal_ip_list[x-1] = out.strip()

	x += 1
	z += 1

# patch drupal settings
z = 0 - CLUSTER_SIZE
x = 1
while x <= CLUSTER_SIZE:
	# get host's public IP
	host_pub_ip = client.droplets.list()[-1]["droplets"][z]["networks"]["v4"][1]["ip_address"]

	call(["/usr/bin/scp", "-o StrictHostKeyChecking=no", "-o PasswordAuthentication=no", HOME + "/kubernetes_cluster_automation/scripts/patch_drupal_settings.sh", "core@" + host_pub_ip + ":~/"])
	call(["/usr/bin/ssh", "-o StrictHostKeyChecking=no", "-o PasswordAuthentication=no", "core@" + host_pub_ip, "bash patch_drupal_settings.sh"])

	x += 1
	z += 1


# copy and run deployment script of haproxy load balancer on each node
z = 0 - CLUSTER_SIZE
x = 1
while x <= CLUSTER_SIZE:
	# get host's public IP
	host_pub_ip = client.droplets.list()[-1]["droplets"][z]["networks"]["v4"][1]["ip_address"]

	call(["/usr/bin/scp", "-o StrictHostKeyChecking=no", "-o PasswordAuthentication=no", HOME + "/kubernetes_cluster_automation/scripts/docker_haproxy.sh", "core@" + host_pub_ip + ":~/"])
	call(["/usr/bin/ssh", "-o StrictHostKeyChecking=no", "-o PasswordAuthentication=no", "core@" + host_pub_ip, "bash docker_haproxy.sh", str(kub_ip), str(x), str(drupal_ip_list)])

	x += 1
	z += 1


print(drupal_ip_list)
