<?php
require_once __DIR__ . '/../vendor/autoload.php';



function validateToken($token) {
    $client = new Google_Client(['client_id' => $_ENV['GOOGLE_CLIENT_ID']]);
    $payload = $client->verifyIdToken($token);
    return $payload ? $payload : null;
}

function authenticate() {
    if (!isset($_SERVER['HTTP_AUTHORIZATION'])) {
        http_response_code(401);
        echo json_encode(['error' => 'Unauthorized']);
        exit();
    }

    $authHeader = $_SERVER['HTTP_AUTHORIZATION'];
    list($token) = sscanf($authHeader, 'Bearer %s');
    
    $user = validateToken($token);
    if ($user) {
        session_start();
        $_SESSION['user'] = $user;
    } else {
        http_response_code(401);
        echo json_encode(['error' => 'Unauthorized']);
        exit();
    }
}

authenticate();