# LOCI Time-Demo API + DB + Static Website Infrastructure
Documented below is a deployment system for the LOCI Time-Demo API, the associated Postgis database serving data, as well as a website front end.

## Deployment components
- VPC to host EC2 instances
- Public subnet inside VPC
- EC2 medium instance for hosting the API which is a containerised Python Sanic API which communicates with the PG database - application starts hosting automatically
- Postgresql/Postgis DB hosted on EC2 medium instance - restores itself automatically from s3 bucket stored backup
- S3 bucket to host the website which has the name "timedemo.lab.loci.cat". This is PUBLIC READ bucket so please ensure no sensitive information is available there (it should just be making curls to a public endpoint)
- Elastic IP allocations for the EC2 instances
- Route53 mappings for the endpoints (documented below)

## Deployment Endpoints 
- EC2 API [http://api.lab.loci.cat:8080]
- EC2 DB (only receives comms from CSIRO VPNs and VPC traffic) [db.lab.loci.cat:5432]
  - You can connect with psql -U postgres -p 5432 -h db.lab.loci.cat 
  - You will be prompted for the password which changes every deployment - retrieve it from AWS Secrets Manager
- S3 Time Demo Integration APP [https://timedemo.lab.loci.cat]

## Quick deployment
Assuming you have the dependencies installed (see below), to **deploy**:
```
python3 -m venv .venv 
source .venv/bin/activate 
pip install -r requirements.txt 
cdk deploy 
```
To **destroy**:
```
python3 -m venv .venv 
source .venv/bin/activate 
pip install -r requirements.txt 
cdk destroy
```
or just 
```
cdk destroy
``` 
if you already have a virtual environment setup and have sourced it.


## Detailed setup steps

Firstly, it is not intended that most users will deploy this system locally. A local deployment will deploy resources to the cloud environment targeted in the app.py file. There is (WIP) a CI/CD pipeline tied to this repo which will keep the build up to date. 

### Local deployment (to AWS) requirements:
- AWS CLI tool installed, see [this](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- AWS CDK installed, you can install it using the following commands:
  Install the AWS CDK Toolkit globally using the following Node Package Manager command.
  ```
  npm install -g aws-cdk
  ```
  Run the following command to verify correct installation and print the version number of the AWS CDK.
  ```
  cdk --version
  ```
- AWS configured to provide access credentials. You can use SSO to provide temporary keys and export them as environment variables, or you can use SSO with the aws-cli. There are a few extra steps to get CDK to recognise your SSO, first, install aws2-wrap from pip
  ```
  pip install aws2-wrap
  ```
  Then configure your normal iam-poweruser role using sso like: 
  ```
  aws configure sso
  ```
  and following the prompts. Once you have your profile configured (make sure to save it as a profile), you can modify your `~/.aws/config` file like so - creating a default and auto profile which use the aws2-wrap to grab credentials from the sso role you have established.
  ```
  [profile default]
  credential_process = aws2-wrap --process --profile poweruser
  region = ...
  
  
  [profile poweruser]
  sso_start_url = ...
  sso_region = ...
  sso_account_id = ...
  sso_role_name = IAMPowerUserAccess
  region = ...
  output = json
  
  [profile auto]
  credential_process = aws2-wrap --process --profile poweruser
  region = ...
  ```
  Once setup, you can use sso as you would expect, e.g. cdk deploy --profile auto. Make sure you login first with aws sso login --profile poweruser. 
- You need Python3.8 or greater, also install the virtual environment extension:
  ```
  sudo apt-get install python3-venv
  ```

### Deployment steps
- Create a virtual environment
  ```
  $ python3 -m venv .venv
  ```
- Activate the venv
  ```
  $ source .venv/bin/activate
  ```
- Install requirements into venv
  ```
  $ pip install -r requirements.txt
  ```
- Use the CDK tool to perform actions, e.g. 
  - To deploy:
  ```
  cdk deploy
  ```
  - To destroy the infrastructure (be careful):
  ```
  cdk destroy
  ```
  - To run a diff over existing (on AWS) vs current:
  ```
  cdk diff
  ``` 
 
	  
