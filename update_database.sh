#!/bin/bash

 mysqldump -P 3306 jobs_samana_db > db/scp.samana.cloud.sql
 scp -i /Users/juampa/Desktop/Samana/juano-scp.pem db/scp.samana.cloud.sql ubuntu@52.86.129.247:/home/ubuntu/scp.samana.cloud/db/.
 ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "mv scp.samana.cloud/db/scp.samana.cloud.sql scp.samana.cloud/db/jobs_samana_db1.sql"
 ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "cd /home/ubuntu/scp.samana.cloud && docker compose up -d --build"

