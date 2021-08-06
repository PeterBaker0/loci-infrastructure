import os

"""
=====================
DEPLOYMENT PARAMETERS
=====================
"""
# Please ensure AWS creds are present which can deploy with full IAM permissions 
# to the below account.

# What AWS region should be targeted
DEPLOYMENT_REGION = os.environ.get("DEPLOYMENT_REGION", 'ap-southeast-2')

# What AWS account should be targeted? LOCI account by default
DEPLOYMENT_ACCOUNT_ID = os.environ.get("DEPLOYMENT_ACCOUNT_ID", "077917336704")

"""
=====================
ADJUSTABLE PARAMETERS
=====================
"""

# The name of the hosted zone e.g. "lab.loci.cat"
HOSTED_ZONE_NAME = os.environ.get(
    "HOSTED_ZONE_NAME",
    "lab.loci.cat"
)

# The unique ID of the existing hosted zone for 
# DNS mapping -> the default is the "lab.loci.cat"
# hosted zone id.
HOSTED_ZONE_ID = os.environ.get(
    "HOSTED_ZONE_ID",
    "Z0038958343ZBGUYG08EO"
)

# This is the name of the prefix on the zone name 
# for the static website. For example, currently, 
# URL of the website will be timedemo.lab.loci.cat
TIME_DEMO_BUCKET_SHORT_NAME = os.environ.get(
    "TIME_DEMO_BUCKET_SHORT_NAME",
    "timedemo"
)

"""
================
FIXED PARAMETERS
================
Currently these are fixed as the variables 
are hardcoded in the scripts. It would be possible
to setup variable injection into the ec2 setup 
scripts in the user_data_tools function if required.
"""
# The desired base IP address of the deployment
BASE_ADDRESS = "10.0.0.0"

# The VPC and subnet CIDR masks
# currently fixed at the most restrictive.
VPC_MASK = 24
SUBNET_MASK = 24

