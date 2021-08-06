# Restore from backup 
backup_bucket_name="loci-change-over-time-db-backup"
file_name="backup.dump"
backup_name="backup.dump"
user_name="ubuntu"

# Update apt-get 
until sudo apt-get update -y
do
	echo "Waiting for apt-get lock.";
	sleep 2;
done

until sudo apt-get install unzip jq -y
do
	echo "Waiting for apt-get lock.";
	sleep 2;
done

# Get the aws-cli v2
# From https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html

# Download the latest 
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"

# Unzip and install
unzip awscliv2.zip
sudo ./aws/install --update

# No credentials file required (role environment variables)
aws s3 cp --no-progress s3://"${backup_bucket_name}"/"${file_name}" /home/"${user_name}"/"${backup_name}"

