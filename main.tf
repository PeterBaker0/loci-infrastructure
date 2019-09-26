module "loci-vpc-subnets" {
    source = "./modules/loci-vpc-subnets"
    availability_zone = var.availability_zone
}

module "loci-ec2-test" {
    source = "./modules/loci-ec2-test"
    loci-subnet-public = module.loci-vpc-subnets.loci-subnet-public
    public_key_path = var.public_key_path
    cidr = var.cidr
    ipv6_cidr = var.ipv6_cidr
    loci-vpc = module.loci-vpc-subnets.loci-vpc
}