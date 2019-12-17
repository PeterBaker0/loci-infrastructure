output "ebs_volume" {
  description = "ebs volume"
  value = "${module.loci-ebs-volume.id}"
}
