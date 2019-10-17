variable "availability_zone" {
  description = "availability zone to create subnet"
  default = "ap-southeast-2c"
}

output "loci-subnet-public" {
    value = aws_subnet.loci-subnet-public
}

output "loci-subnet-private" {
    value = aws_subnet.loci-subnet-private
}

output "loci-vpc" {
    value = aws_vpc.loci-vpc
}
