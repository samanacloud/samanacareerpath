#!/bin/bash

# Remove existing tar.gz file
rm scp.samana.cloud.tar.gz 

# Backup the Database
 mysqldump -P 3306 jobs_samana_db > db/scp.samana.cloud.sql

# Updating the database locally
mv db/scp.samana.cloud.sql db/jobs_samana_db.sql

# Create a new tar.gz archive, excluding the 'api_keys' directory
tar -czvf scp.samana.cloud.tar.gz --exclude='./api_keys' .

# Temporarily change permissions
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "sudo chmod 777 /opt/scp.samana.cloud/"

# Shut down the Docker Container
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "cd /opt/scp.samana.cloud && docker compose down"

# Clean the entire folder before copy all again
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "cd /opt/scp.samana.cloud && sudo rm -rf * "

# Copy the archive to the remote server
scp -i /Users/juampa/Desktop/Samana/juano-scp.pem scp.samana.cloud.tar.gz ubuntu@52.86.129.247:/opt/scp.samana.cloud/.




# Extract the archive on the remote server
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "sudo tar -xzvf /opt/scp.samana.cloud/scp.samana.cloud.tar.gz -C /opt/scp.samana.cloud/"


# Start the Docker containers using docker-compose
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "cd /opt/scp.samana.cloud && docker compose up -d"

# Remove the archive from the remote server
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "sudo rm /opt/scp.samana.cloud/scp.samana.cloud.tar.gz"

# Remove the local archive
rm scp.samana.cloud.tar.gz
# Remove the database backup locally
rm db/scp.samana.cloud.sql 
# Free Space in the remote server
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "docker system prune -a -f"

# Remove the archive from the remote server
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "sudo rm /opt/scp.samana.cloud/scp.samana.cloud.tar.gz"
#  Restore permissions
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "sudo chmod 755 /opt/scp.samana.cloud/"