# Get jq from yum
sudo yum install jq -y

# Install aws cli v2 to have creds 
# From https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html

# Download the latest 
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"

# Unzip and install
unzip awscliv2.zip
sudo ./aws/install --update

# Retrieve db password from secrets manager 
# Establish secret name
database_secret_name="loci-time-demo-db-password"
database_vpc_ip="10.0.0.28"

# Set application docker env variables
export TEMPORAL_PG_PASSWORD=$(aws secretsmanager get-secret-value --secret-id ${database_secret_name} | jq -r ".SecretString")
export TEMPORAL_PG_HOST="${database_vpc_ip}"
export TEMPORAL_PG_PORT="5432"
export TEMPORAL_PG_DB_NAME="loci"
export TEMPORAL_PG_USER="postgres"