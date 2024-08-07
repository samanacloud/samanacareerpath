<?php
require_once '../vendor/autoload.php';

// Test database connection
$mysqli = new mysqli(getenv('MYSQL_HOSTNAME'), getenv('MYSQL_USER'), getenv('MYSQL_PASSWORD'), getenv('MYSQL_DATABASE'));

if ($mysqli->connect_error) {
    die("Database connection failed: " . $mysqli->connect_error);
}

echo "Database connection successful<br>";

// Query to show tables
$result = $mysqli->query("SHOW TABLES");

if ($result) {
    echo "Tables in the database:<br>";
    while ($row = $result->fetch_array()) {
        echo $row[0] . "<br>";
    }
} else {
    echo "Error showing tables: " . $mysqli->error;
}

$mysqli->close();
?>