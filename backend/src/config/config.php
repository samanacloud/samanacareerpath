<?php
require_once __DIR__ . '/../../vendor/autoload.php';



$redirect_uri =  'https://' . $_ENV['SITE_URL'];
#$redirect_uri = $_ENV['BACKEND_PROTOCOL'] . '://' . $_ENV['SITE_URL'];
#if ($_ENV['BACKEND_PORT'] != 80 && $_ENV['BACKEND_PORT'] != 443) {
#    $redirect_uri .= ':' . $_ENV['BACKEND_PORT'];
#}
$redirect_uri .= '/api/google-login/callback.php';

$redirect_uri_api =  'https://' . $_ENV['SITE_URL'];
#$redirect_uri_api = $_ENV['BACKEND_PROTOCOL'] . '://' . $_ENV['SITE_URL'];
#if ($_ENV['BACKEND_PORT'] != 80 && $_ENV['BACKEND_PORT'] != 443) {
#    $redirect_uri_api .= ':' . $_ENV['BACKEND_PORT'];
#}
$redirect_uri_api .= '/api/google-login/apicallback.php';

$config = [
    'google' => [
        'client_id' => $_ENV['GOOGLE_CLIENT_ID'],
        'client_secret' => $_ENV['GOOGLE_CLIENT_SECRET'],
        'redirect_uri' => $redirect_uri,
        'redirect_uri_api' => $redirect_uri_api,
    ],
    'database' => [
        'host' => $_ENV['MYSQL_HOSTNAME'],
        'port' => $_ENV['MYSQL_PORT'],
        'db' => $_ENV['MYSQL_DATABASE'],
        'user' => $_ENV['MYSQL_USER'],
        'pass' => $_ENV['MYSQL_PASSWORD'],
    ],
];
return $config;
