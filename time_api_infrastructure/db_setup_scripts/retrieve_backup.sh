# Restore from backup 
backup_bucket_name="loci-change-over-time-db-backup"
file_name="backup.dump"
backup_name="backup.dump"

# Wait for access to apt-get 
# https://askubuntu.com/questions/132059/how-to-make-a-package-manager-wait-if-another-instance-of-apt-is-running
while sudo fuser /var/{lib/{dpkg,apt/lists},cache/apt/archives}/lock >/dev/null 2>&1; do 
	sleep 1;
done

# Update apt-get 
sudo apt-get update -y

# Get unzip 
sudo apt-get install unzip -y

# Get the aws-cli v2
# From https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html

# Download the latest 
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"

# Unzip and install
unzip awscliv2.zip
sudo ./aws/install

# No credentials file required (role environment variables)
aws s3 cp s3://"${backup_bucket_name}"/"${file_name}" "${backup_name}"

