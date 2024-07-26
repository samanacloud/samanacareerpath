#!/bin/bash
set -e

echo "Starting MySQL server..."
/usr/local/bin/docker-entrypoint.sh mysqld &

echo "Waiting for MySQL server to start..."
while ! mysqladmin ping -h "localhost" --silent; do
    sleep 1
done

echo "MySQL server started. Importing database..."
mysql -u root -p"${MYSQL_ROOT_PASSWORD}" "${MYSQL_DATABASE}" < /docker-entrypoint-initdb.d/jobs_samana_db.sql 2>&1 | tee /docker-entrypoint-initdb.d/mysql_import.log

echo "Database import finished."
wait