#!/bin/bash

# Get today's date
DATE=$(date +"%d-%m-%Y")
BACKUP_TMP_FOLDER="/tmp/mongodbbackuplatest"
BACKUP_OUTPUT_FOLDER="/opt/careerpath1.0/mongodb/backups"
BACKUP_FILENAME="backup-$DATE.tar.gz"

# Step 1: Create backup inside MongoDB container
docker exec -i scp_mongodb mongodump --username admin --password 'Samana!!CareerPath' --authenticationDatabase admin --db careerpath_db --out "$BACKUP_TMP_FOLDER"

# Step 2: Copy backup from container to server temp folder
docker cp scp_mongodb:$BACKUP_TMP_FOLDER "$BACKUP_OUTPUT_FOLDER/backup-$DATE"

# Step 3: Compress it into a single tar.gz
cd "$BACKUP_OUTPUT_FOLDER"
tar -czvf "$BACKUP_FILENAME" "backup-$DATE"

# Step 4: Remove the uncompressed folder
rm -rf "$BACKUP_OUTPUT_FOLDER/backup-$DATE"

# Step 5: Clean up inside container
docker exec -i scp_mongodb rm -rf "$BACKUP_TMP_FOLDER"

echo "Backup completed and compressed successfully: $BACKUP_OUTPUT_FOLDER/$BACKUP_FILENAME"
