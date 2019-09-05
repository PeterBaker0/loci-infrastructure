resource "aws_network_acl" "sg_loci" {
  vpc_id = "${aws_vpc.loci-vpc.id}"
  subnet_ids = ["${aws_subnet.loci-subnet-public.id}"]
}
resource "aws_network_acl_rule" "loci-test-acl-ingress" {
  network_acl_id = "${aws_network_acl.sg_loci.id}"
  egress = false
    protocol   = "-1"
    rule_number    = "1"
    rule_action     = "allow"
    cidr_block = "0.0.0.0/0" 
}
resource "aws_network_acl_rule" "loci-test-acl-egress" {
  network_acl_id = "${aws_network_acl.sg_loci.id}"
  egress = true 
    protocol   = "-1"
    rule_number    = "1"
    rule_action     = "allow"
    cidr_block = "0.0.0.0/0" 
}
resource "aws_network_acl_rule" "loci-test-acl-ingress-6" {
  network_acl_id = "${aws_network_acl.sg_loci.id}"
  egress = false
    protocol   = "-1"
    rule_number    = "10"
    rule_action     = "allow"
    ipv6_cidr_block= "::/0"
}
resource "aws_network_acl_rule" "loci-test-acl-egress-6" {
  network_acl_id = "${aws_network_acl.sg_loci.id}"
  egress = true 
    protocol   = "-1"
    rule_number    = "10"
    rule_action     = "allow"
    ipv6_cidr_block= "::/0"
}


