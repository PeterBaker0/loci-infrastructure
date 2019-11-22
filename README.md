# loci-infrastructure
aws infrastructure for loci

Go to environments dir for terraform.

Go to packer dir for packer.

Build packer then build using terraform.

## Quickstart

need app.terraform.io token in ~/.terraformrc

cidr ranges to restrict access need to be defined. One way of doing this is to create a file like secrets.tf. secrets_template is provided as a template it can be copied and modified with real ip ranges.

need keys for SSH in a home dir called ~/loci-keys

Valid AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY and AWS_SESSION_TOKEN need to be defined as environment variables (or via other terraform acceptable means)

To run combinations of:
```
terraform init 
terraform plan
terraform apply
terraform destroy
as per the terraform documentation
```
