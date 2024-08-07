<?php
session_start();
require_once  '../config/config.php';
require_once __DIR__ . '/../../vendor/autoload.php';

$config = include('../config/config.php');
// Check if session is not already started
if (session_status() == PHP_SESSION_NONE) {
    session_start();
}

$client = new Google_Client();
$client->setClientId($config['google']['client_id']);
$client->setClientSecret($config['google']['client_secret']);
$client->setRedirectUri($config['google']['redirect_uri']);
$client->addScope("email");
$client->addScope("profile");

$auth_url = $client->createAuthUrl();

// Redirect to Google login page
header('Location: ' . filter_var($auth_url, FILTER_SANITIZE_URL));
exit();
?>