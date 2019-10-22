data "terraform_remote_state" "id" {
  backend = "remote"

  config = {
    organization = "loci"
    workspaces = {
      name = "dev"
    }
  }
}
data "aws_ami" "ec2-ami" {
  owners           = ["self"]
  filter {
    name   = "state"
    values = ["available"]
  }  
  filter {
    name   = "name"
    values = ["loci-integration-api-image*"]
  }  
  most_recent = true
}
data "aws_ami" "ec2-db-ami" {
  owners           = ["self"]
  filter {
    name   = "state"
    values = ["available"]
  }  
  filter {
    name   = "name"
    values = ["loci-integration-db-image*"]
  }  
  most_recent = true
}
resource "aws_instance" "test_loci_ec2" {
  ami           = "${data.aws_ami.ec2-ami.id}" 
  instance_type = "m5.large"
  availability_zone = "ap-southeast-2a"
  subnet_id = "${var.loci-subnet-public.id}"
  key_name = "${aws_key_pair.ec2key.key_name}"
  vpc_security_group_ids = ["${aws_security_group.loci-ec2.id}"]
  tags = {
    Name    = "loci test api"
    Project = "Loci"
    O2D     = "TBA"
    }
}

resource "aws_volume_attachment" "loci_api_ebs_att" {
  device_name = "/dev/sdh"
  volume_id   = "${data.terraform_remote_state.id}"
  instance_id = "${aws_instance.test_loci_ec2.id}"
  provisioner "remote-exec" {
    connection {
      host     = "${aws_instance.test_loci_ec2.public_ip}"
      type     = "ssh"
      user     = "ec2-user"
    }
    inline = [
      "mkfs -t ext4 /dev/sdh",
      "mkdir /certs",
      "mount /dev/sdh /certs"
    ]
  }
}

resource "aws_instance" "test_loci_ec2-2" {
  ami           = "${data.aws_ami.ec2-db-ami.id}" 
  availability_zone = "ap-southeast-2a"
  instance_type = "t2.large"
  subnet_id = "${var.loci-subnet-private.id}"
  private_ip = "10.0.1.200"
  key_name = "${aws_key_pair.ec2key.key_name}"
  vpc_security_group_ids = ["${aws_security_group.loci-ec2-private-db.id}"]
  tags = {
    Name    = "loci test db"
    Project = "Loci"
    O2D     = "TBA"
    }
}
resource "aws_eip_association" "eip_assoc" {
  instance_id   = "${aws_instance.test_loci_ec2.id}"
  allocation_id = "${var.eip_allocation_id}"
}

resource "aws_key_pair" "ec2key" {
  key_name = "publicKey"
  public_key = "${file(var.public_key_path)}"
}

resource "aws_security_group" "loci-ec2-private-db" {
  name        = "loci_ec2-private-2"
  description = "loci_ec2 security group"
  vpc_id = "${var.loci-vpc.id}"

  ingress {
    # TLS (change to whatever ports you need)
    from_port   = 22 
    to_port     = 22 
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }
  
  egress {
    # TLS (change to whatever ports you need)
    from_port   = 22 
    to_port     = 22 
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }
  
  ingress {
    # TLS (change to whatever ports you need)
    from_port   = 5432 
    to_port     = 5432 
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }
  egress {
    # TLS (change to whatever ports you need)
    from_port   = 5432 
    to_port     = 5432 
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }
  
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
  
  ingress {
    # TLS (change to whatever ports you need)
    from_port   = 80 
    to_port     = 80 
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    # TLS (change to whatever ports you need)
    from_port   = 80 
    to_port     = 80 
    protocol    = "tcp"
    ipv6_cidr_blocks =["::/0"]
  }
  
  ingress {
    # TLS (change to whatever ports you need)
    from_port   = 443 
    to_port     = 443 
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    # TLS (change to whatever ports you need)
    from_port   = 443 
    to_port     = 443 
    protocol    = "tcp"
    ipv6_cidr_blocks =["::/0"]
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

