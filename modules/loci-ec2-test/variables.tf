variable "loci-subnet-public" {
  description = "public subnet"
}
variable "loci-vpc" {
  description = "loci-vpc"
}
variable "public_key_path" {
  description = "ec2 public key path"
}
variable "cidr" {
  description = "ipv4 cidr blocks for security"
}
variable "ipv6_cidr" {
  description = "ipv6 cidr blocks for security"
}

output "ec2_address" {
  value = aws_instance.test_loci_ec2.public_ip
}