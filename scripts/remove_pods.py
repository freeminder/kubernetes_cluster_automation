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
from ../myconfig import *


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


x = 1
while x <= CLUSTER_SIZE:
	# get host's public IP
	host_pub_ip = client.droplets.list()[-1]["droplets"][z]["networks"]["v4"][1]["ip_address"]
	call(["/usr/bin/scp", "-o StrictHostKeyChecking=no", "-o PasswordAuthentication=no", HOME + "/kubernetes_cluster_automation/scripts/destroy_script.sh", "core@" + host_pub_ip + ":~/"])
	call(["/usr/bin/ssh", "-o StrictHostKeyChecking=no", "-o PasswordAuthentication=no", "core@" + host_pub_ip, "bash destroy_script.sh", str(kub_ip), str(x)])

	x += 1
	z += 1

print(drupal_ip_list)