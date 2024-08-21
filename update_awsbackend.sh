# Temporarily change permissions recursively
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "sudo chmod -R 777 /opt/scp.samana.cloud/backend/src/"

# Wait a moment to ensure permissions are set
sleep 2

# Copy the archive to the remote server
scp -i /Users/juampa/Desktop/Samana/juano-scp.pem backend/src/*.* ubuntu@52.86.129.247:/opt/scp.samana.cloud/backend/src/

# Wait a moment to ensure the files have been copied
sleep 2

# Copy the files to the docker (Uncomment if needed)
#ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "docker cp /opt/scp.samana.cloud/backend/src/. backend_php:/app/src/router/"

# Restore permissions recursively
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "sudo chmod -R 755 /opt/scp.samana.cloud/backend/src/"