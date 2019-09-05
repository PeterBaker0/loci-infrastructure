resource "aws_vpc" "loci-vpc" {
  cidr_block       = "10.0.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true

  tags = {
    Name    = "loci test vpc"
    Project = "Loci"
    O2D     = "TBA"
  }
}
resource "aws_internet_gateway" "loci-igw" {
  vpc_id = "${aws_vpc.loci-vpc.id}"
  tags = {
    Name    = "loci test igw"
    Project = "Loci"
    O2D     = "TBA"
  }
}

resource "aws_subnet" "loci-subnet-public" {
  vpc_id = "${aws_vpc.loci-vpc.id}"
  cidr_block = "10.0.0.0/24"
  map_public_ip_on_launch = "true"
  availability_zone = "${var.availability_zone}"
  tags = {
    Name    = "loci test subnet"
    Project = "Loci"
    O2D     = "TBA"
  }
}
resource "aws_route_table" "loci-rtb-public" {
  vpc_id = "${aws_vpc.loci-vpc.id}"
  route {
      cidr_block = "0.0.0.0/0"
      gateway_id = "${aws_internet_gateway.loci-igw.id}"
  }
  tags = {
    Name    = "loci test route table"
    Project = "Loci"
    O2D     = "TBA"
  }
}

resource "aws_route_table_association" "loci-rta-subnet-public" {
  subnet_id      = "${aws_subnet.loci-subnet-public.id}"
  route_table_id = "${aws_route_table.loci-rtb-public.id}"
}

resource "aws_main_route_table_association" "loci-main-table" {
  vpc_id         = "${aws_vpc.loci-vpc.id}"
  route_table_id = "${aws_route_table.loci-rtb-public.id}"
}
