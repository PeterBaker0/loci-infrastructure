variable "public_key_suffix" {
  description = "private subnet"
}
variable "loci-subnet-private" {
  description = "private subnet"
}
variable "loci-subnet-public" {
  description = "public subnet"
}
variable "loci-vpc" {
  description = "loci-vpc"
}
variable "private_key_path" {
  description = "ec2 public key path"
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
variable eip_allocation_id {
  description = "eip allocation id"
}
variable "public_ip" {
  description = "public ip of api" 
}
variable triplestore_cache_url {
  description = "triple store cache url"
}
output "ec2_address" {
  value = aws_instance.test_loci_ec2.public_ip
}
variable api_image_tag_suffix {
  description = "suffix on the api image tag"
}