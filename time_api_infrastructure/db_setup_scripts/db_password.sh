# Assumption: aws cli v2 is already installed (in retrieve_backup)
# Retrieve db password from secrets manager 

# AWS secret name
database_secret_name="loci-time-demo-db-password"

# Pull secret and parse for SecretString -> db_password
 db_password=$(aws secretsmanager get-secret-value --secret-id ${database_secret_name} | jq -r ".SecretString")