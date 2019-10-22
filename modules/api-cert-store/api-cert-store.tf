resource "aws_ebs_volume" "cert_store" {
  availability_zone = "ap-southeast-2a"
  size              = 2 
  type              = "gp2"
  tags = {
    Name = "Loci API certificate storage"
    Purpose = "Loci API lets encrypt certificate storage"
  }
}