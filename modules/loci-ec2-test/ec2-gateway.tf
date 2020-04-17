data "terraform_remote_state" "certs" {
  backend = "remote"

  config = {
    organization = "loci"
    workspaces = {
      name = "dev-cert-store"
    }
  }
}

data "aws_ami" "ec2-ami" {
  owners = ["self"]
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

data "aws_ami" "ec2-gds-ami" {
  owners = ["self"]
  filter {
    name   = "state"
    values = ["available"]
  }
  filter {
    name   = "name"
    values = ["loci-geometry-data-service-image*"]
  }
  most_recent = true
}

data "aws_ami" "ec2-locicorsproxy-ami" {
  owners = ["self"]
  filter {
    name   = "state"
    values = ["available"]
  }
  filter {
    name   = "name"
    values = ["loci-cors-proxy-image*"]
  }
  most_recent = true
}



data "aws_ami" "ec2-gds-db-ami" {
  owners = ["self"]
  filter {
    name   = "state"
    values = ["available"]
  }
  filter {
    name   = "name"
    values = ["loci-geometry-data-service-db-image*"]
  }
  most_recent = true
}

resource "aws_instance" "test_loci_ec2" {
  ami                         = "${data.aws_ami.ec2-ami.id}"
  instance_type               = "m5.large"
  availability_zone           = "ap-southeast-2c"
  associate_public_ip_address = true
  subnet_id                   = "${var.loci-subnet-public.id}"
  key_name                    = "${aws_key_pair.ec2key.key_name}"
  vpc_security_group_ids      = ["${aws_security_group.loci-ec2.id}"]
  tags = {
    Name    = "loci test api"
    Project = "Loci"
    O2D     = "TBA"
  }
  user_data = <<-EOF
      #! /bin/bash 
      sed -i '1 aexport TRIPLESTORE_CACHE_URL=${var.triplestore_cache_url}' /instance.sh
      . /instance.sh
    EOF
}

resource "aws_instance" "test_loci_ec2-geometry-data-service" {
  ami                         = "${data.aws_ami.ec2-gds-ami.id}"
  instance_type               = "m5.large"
  availability_zone           = "ap-southeast-2c"
  associate_public_ip_address = true
  subnet_id                   = "${var.loci-subnet-public.id}"
  key_name                    = "${aws_key_pair.ec2key.key_name}"
  vpc_security_group_ids      = ["${aws_security_group.loci-ec2.id}"]
  tags = {
    Name    = "loci test geometry-data-service api"
    Project = "Loci"
    O2D     = "TBA"
  }
}

resource "aws_instance" "test_loci_ec2-cors-proxy" {
  ami                         = "${data.aws_ami.ec2-locicorsproxy-ami.id}"
  instance_type               = "t2.micro"
  availability_zone           = "ap-southeast-2c"
  associate_public_ip_address = true
  subnet_id                   = "${var.loci-subnet-public.id}"
  key_name                    = "${aws_key_pair.ec2key.key_name}"
  vpc_security_group_ids      = ["${aws_security_group.loci-ec2.id}"]
  tags = {
    Name    = "loci test cors proxy"
    Project = "Loci"
    O2D     = "TBA"
  }
}

/*resource "aws_volume_attachment" "loci_api_ebs_att" {
  device_name = "/dev/sdh"
  volume_id   = "${data.terraform_remote_state.certs.outputs.ebs_volume}"
  instance_id = "${aws_instance.test_loci_ec2.id}"
  provisioner "remote-exec" {
    connection {
      host        = "${var.public_ip}"
      type        = "ssh"
      user        = "ec2-user"
      private_key = "${file(var.private_key_path)}"
    }
    inline = [
      "sudo yum install xfsprogs",
      "if [ x`lsblk -ln -o FSTYPE /dev/sdh` != 'xext4' ] ; then sudo mkfs.ext4 /dev/sdh; fi",
      "sudo mkdir /certs",
      "sudo mount /dev/sdh /certs"
    ]
  }
}*/

resource "aws_instance" "test_loci_ec2-geometry-data-service-db" {
  ami                    = "${data.aws_ami.ec2-gds-db-ami.id}"
  availability_zone      = "ap-southeast-2c"
  instance_type          = "t2.large"
  subnet_id              = "${var.loci-subnet-private.id}"
  private_ip             = "10.0.1.201"
  key_name               = "${aws_key_pair.ec2key.key_name}"
  vpc_security_group_ids = ["${aws_security_group.loci-ec2-private-db.id}"]
  tags = {
    Name    = "loci test geometry-data-service db"
    Project = "Loci"
    O2D     = "TBA"
  }
}

resource "aws_eip_association" "eip_assoc" {
  instance_id   = "${aws_instance.test_loci_ec2.id}"
  allocation_id = "${var.eip_allocation_id}"
}

resource "aws_key_pair" "ec2key" {
  key_name   = "publicKey${var.public_key_suffix}"
  public_key = "${file(var.public_key_path)}"
}

resource "aws_security_group" "loci-ec2-private-db" {
  name        = "loci_ec2-private-2"
  description = "loci_ec2 security group"
  vpc_id      = "${var.loci-vpc.id}"

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
    from_port   = 5437
    to_port     = 5437
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }
  egress {
    # TLS (change to whatever ports you need)
    from_port   = 5437
    to_port     = 5437
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  ingress {
    # TLS (change to whatever ports you need)
    from_port   = 25432
    to_port     = 25432
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }
  egress {
    # TLS (change to whatever ports you need)
    from_port   = 25432
    to_port     = 25432
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

}


resource "aws_security_group" "loci-ec2" {
  name        = "loci_ec2"
  description = "loci_ec2 security group"
  vpc_id      = "${var.loci-vpc.id}"

  ingress {
    # TLS (change to whatever ports you need)
    from_port   = 5437
    to_port     = 5437
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  ingress {
    # TLS (change to whatever ports you need)
    from_port   = 25432
    to_port     = 25432
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  ingress {
    # TLS (change to whatever ports you need)
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = "${var.cidr}"
  }
  ingress {
    # TLS (change to whatever ports you need)
    from_port        = 22
    to_port          = 22
    protocol         = "tcp"
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
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    # TLS (change to whatever ports you need)
    from_port        = 80
    to_port          = 80
    protocol         = "tcp"
    ipv6_cidr_blocks = ["::/0"]
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
    from_port        = 443
    to_port          = 443
    protocol         = "tcp"
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    ipv6_cidr_blocks = ["::/0"]
  }
}

