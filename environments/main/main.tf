module "loci-vpc-subnets" {
    source = "../../modules/loci-vpc-subnets"
    availability_zone = var.availability_zone
}

module "loci-ec2-test" {
    source = "../../modules/loci-ec2-test"
    loci-subnet-public = module.loci-vpc-subnets.loci-subnet-public
    loci-subnet-private = module.loci-vpc-subnets.loci-subnet-private
    public_key_path = var.public_key_path
    private_key_path = var.private_key_path
    cidr = var.cidr
    ipv6_cidr = var.ipv6_cidr
    eip_allocation_id = var.eip_allocation_id
    loci-vpc = module.loci-vpc-subnets.loci-vpc
    public_ip = var.public_ip
}