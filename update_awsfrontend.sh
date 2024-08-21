# Temporarily change permissions
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "sudo chmod -R 777 /opt/scp.samana.cloud/frontend/src/src/router/"
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "sudo chmod -R 777 /opt/scp.samana.cloud/frontend/src/src/views/"
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "sudo chmod -R 777 /opt/scp.samana.cloud/frontend/src/src/service/"
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "sudo chmod -R 777 /opt/scp.samana.cloud/frontend/src/src/utils/"
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "sudo chmod -R 777 /opt/scp.samana.cloud/frontend/src/src/layout/"
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "sudo chmod -R 777 /opt/scp.samana.cloud/frontend/src/public/"
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "sudo chmod  777 /opt/scp.samana.cloud/frontend/src/src/App.vue"
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "sudo chmod  777 /opt/scp.samana.cloud/frontend/src/index.html"
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "sudo chmod  777 /opt/scp.samana.cloud/frontend/src/package.json"




# Copy the archive to the remote server
scp -i /Users/juampa/Desktop/Samana/juano-scp.pem -r frontend/src/src/router/ ubuntu@52.86.129.247:/opt/scp.samana.cloud/frontend/src/src/router/
scp -i /Users/juampa/Desktop/Samana/juano-scp.pem -r frontend/src/src/views/pages/ ubuntu@52.86.129.247:/opt/scp.samana.cloud/frontend/src/src/views/pages/
scp -i /Users/juampa/Desktop/Samana/juano-scp.pem -r frontend/src/src/service/ ubuntu@52.86.129.247:/opt/scp.samana.cloud/frontend/src/src/service/
scp -i /Users/juampa/Desktop/Samana/juano-scp.pem -r frontend/src/src/utils/ ubuntu@52.86.129.247:/opt/scp.samana.cloud/frontend/src/src/utils/
scp -i /Users/juampa/Desktop/Samana/juano-scp.pem -r frontend/src/src/layout/ ubuntu@52.86.129.247:/opt/scp.samana.cloud/frontend/src/src/layout/
scp -i /Users/juampa/Desktop/Samana/juano-scp.pem  frontend/src/public/*.* ubuntu@52.86.129.247:/opt/scp.samana.cloud/frontend/src/public/
scp -i /Users/juampa/Desktop/Samana/juano-scp.pem frontend/src/src/App.vue ubuntu@52.86.129.247:/opt/scp.samana.cloud/frontend/src/src/App.vue
scp -i /Users/juampa/Desktop/Samana/juano-scp.pem frontend/src/index.html ubuntu@52.86.129.247:/opt/scp.samana.cloud/frontend/src/index.html
scp -i /Users/juampa/Desktop/Samana/juano-scp.pem frontend/src/package.json ubuntu@52.86.129.247:/opt/scp.samana.cloud/frontend/src/package.json
scp -i /Users/juampa/Desktop/Samana/juano-scp.pem frontend/src/src/views/Dashboard.vue ubuntu@52.86.129.247:/opt/scp.samana.cloud/frontend/src/src/views/Dashboard.vue

#  Copy the files to the docker
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "docker cp /opt/scp.samana.cloud/frontend/src/src/router/. frontend_node:/app/src/router/"
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "docker cp /opt/scp.samana.cloud/frontend/src/src/views/. frontend_node:/app/src/views/"
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "docker cp /opt/scp.samana.cloud/frontend/src/src/service/. frontend_node:/app/src/service/"
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "docker cp /opt/scp.samana.cloud/frontend/src/src/utils/. frontend_node:/app/src/utils/"
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "docker cp /opt/scp.samana.cloud/frontend/src/src/layout/. frontend_node:/app/src/layout/"
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "docker cp /opt/scp.samana.cloud/frontend/src/public/. frontend_node:/app/public/"
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "docker cp /opt/scp.samana.cloud/frontend/src/src/App.vue frontend_node:/app/src/"
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "docker cp /opt/scp.samana.cloud/frontend/src/index.html frontend_node:/app/"
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "docker cp /opt/scp.samana.cloud/frontend/src/package.json frontend_node:/app/"

#  Restore permissions
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "sudo chmod -R 755 /opt/scp.samana.cloud/frontend/src/src/router/"
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "sudo chmod -R 755 /opt/scp.samana.cloud/frontend/src/src/views/"
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "sudo chmod -R 755 /opt/scp.samana.cloud/frontend/src/src/service/"
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "sudo chmod -R 755 /opt/scp.samana.cloud/frontend/src/src/utils/"
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "sudo chmod -R 755 /opt/scp.samana.cloud/frontend/src/src/layout/"
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "sudo chmod  755 /opt/scp.samana.cloud/frontend/src/src/App.vue"
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "sudo chmod  755 /opt/scp.samana.cloud/frontend/src/index.html"
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "sudo chmod  755 /opt/scp.samana.cloud/frontend/src/package.json"
ssh -i /Users/juampa/Desktop/Samana/juano-scp.pem ubuntu@52.86.129.247 "sudo chmod -R 755 /opt/scp.samana.cloud/frontend/src/public/"