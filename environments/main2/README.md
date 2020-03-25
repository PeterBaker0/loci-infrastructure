# Loci AWS Infrastructure Automation

Terraform configuration for spinning up loci infrastructure on AWS

*Early Prototype* 

Spins up an ec2 instance using your local public ssh key with a VPC, public subnet, and internet gateway and security restricted to ssh at specified ip ranges

## Running

cidr ranges to restrict access need to be defined. One way of doing this is to create a file like secrets.tf.  secrets_template is provided as a template it can be copied and modified with real ip ranges and an existing static elastic ip associated with the api.loci.cat dns entry.

Valid AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY and AWS_SESSION_TOKEN need to be defined as environment variables (or via other terraform acceptable means)

Build Ami via Packer in packer/loci-integration-api:

```
packer build loci-integration-api-image.json 
```

To run combinations of: 

```
terraform init 
terraform plan
terraform apply
terraform destroy
```
as per the terraform documentation