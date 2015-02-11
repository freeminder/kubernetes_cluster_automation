# Usage

Run the following scripts/full_init.py script will create 3 nodes cluster by default on
DigitalOcean and setup local registry, drupal and nginx pods.

You will need to create your own myconfig.py in the root dir.
This file should contain the following values:

    API_KEY = 'xxx'
    SSH_KEY_ID = '123456'
    CLUSTER_SIZE = 3
