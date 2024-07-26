<?php
// Get all environment variables
$environmentVariables = getenv();

// Display all environment variables
foreach ($environmentVariables as $key => $value) {
    echo "$key: $value\n";
}
