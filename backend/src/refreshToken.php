<?php
session_start();
require '../vendor/autoload.php';
require_once 'config/config.php';

// Define response function
function sendJsonResponse($data, $statusCode = 200) {
    header('Content-Type: application/json');
    http_response_code($statusCode);
    echo json_encode($data);
    exit();
}

// Get the refresh token from the session
$refreshToken = $_SESSION['refreshToken'] ?? null;

if (!$refreshToken) {
    sendJsonResponse(['error' => 'Refresh token not found'], 400);
}

$clientId = getenv('GOOGLE_CLIENT_ID');
$clientSecret = getenv('GOOGLE_CLIENT_SECRET');
$redirectUri = 'https://scp.samana.cloud/api/oauthcallback.php';

$client = new Google_Client();
$client->setClientId($clientId);
$client->setClientSecret($clientSecret);
$client->setRedirectUri($redirectUri);
$client->setAccessType('offline'); // Required to get a refresh token
$client->setApprovalPrompt('force');

try {
    // Refresh the access token using the refresh token
    $client->refreshToken($refreshToken);
    $newToken = $client->getAccessToken();

    // Check if the token refresh was successful
    if ($newToken) {
        // Update session tokens
        $_SESSION['authToken'] = $newToken['access_token'];
        $_SESSION['refreshToken'] = $newToken['refresh_token'] ?? $refreshToken; // Keep the old refresh token if a new one is not provided

        // Send the new access token back to the frontend
        sendJsonResponse([
            'access_token' => $newToken['access_token'],
            'expires_in' => $newToken['expires_in']
        ]);
    } else {
        sendJsonResponse(['error' => 'Failed to refresh token'], 500);
    }
} catch (Exception $e) {
    sendJsonResponse(['error' => 'Error refreshing token: ' . $e->getMessage()], 500);
}