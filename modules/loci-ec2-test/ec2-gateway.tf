resource "aws_instance" "test_loci_ec2" {
  ami           = "ami-075caa3491def750b"
  instance_type = "t2.micro"
  subnet_id = "${var.loci-subnet-public.id}"
  key_name = "${aws_key_pair.ec2key.key_name}"
  vpc_security_group_ids = ["${aws_security_group.loci-ec2.id}"]
  tags = {
    Name    = "loci test gateway"
    Project = "Loci"
    O2D     = "TBA"
    }
}
resource "aws_key_pair" "ec2key" {
  key_name = "publicKey"
  public_key = "${file(var.public_key_path)}"
}

resource "aws_security_group" "loci-ec2" {
  name        = "loci_ec2"
  description = "loci_ec2 security group"
  vpc_id = "${var.loci-vpc.id}"

  ingress {
    # TLS (change to whatever ports you need)
    from_port   = 22 
    to_port     = 22 
    protocol    = "tcp"
    cidr_blocks = "${var.cidr}"
  }
  ingress {
    # TLS (change to whatever ports you need)
    from_port   = 22 
    to_port     = 22 
    protocol    = "tcp"
    ipv6_cidr_blocks = "${var.ipv6_cidr}"
  }

  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]
  }
  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    ipv6_cidr_blocks     = ["::/0"]
  }
}

