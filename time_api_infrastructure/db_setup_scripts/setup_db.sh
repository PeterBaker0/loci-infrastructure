# Some variables 
database_name="loci"

# Update package repo
until sudo apt-get update -y
do
	echo "Waiting for apt-get lock.";
	sleep 2;
done

# Install postgres requirements 
until sudo apt-get install postgresql-12-postgis-3 postgresql-12-postgis-3-scripts -y
do
	echo "Waiting for apt-get lock.";
	sleep 2;
done

# Update security 
# Enable authentication to all dbs with password
echo "host  all  all 0.0.0.0/0 md5" >> /etc/postgresql/12/main/pg_hba.conf

# Listen on all IP addresses
echo "listen_addresses = '*'" >> /etc/postgresql/12/main/postgresql.conf

# Use password md5 encryption
echo "password_encryption = md5" >> /etc/postgresql/12/main/postgresql.conf

# Start service temporarily 
sudo systemctl start postgresql 

# Create some commands to update password 
# Password was retrieved from AWS SM in db_password
# Create some commands to launch inside the psql context of the 
# postgres user
 printf "\password\n${db_password}\n${db_password}" > update_password.temp

# Perform password update sequence 
sudo su -c "psql" - postgres < update_password.temp 

# Clean up 
rm update_password.temp 
unset db_password

# Restore from backup file which was downloaded 

# Backup file is called ${backup_name}
sudo su -c "createdb ${database_name}" - postgres

# Restore the database to loci (this will take a while)
sudo su -c "pg_restore -d ${database_name} /home/${user_name}/${backup_name}" - postgres

# Stop the service for now - we are due for a restart
sudo systemctl stop postgresql