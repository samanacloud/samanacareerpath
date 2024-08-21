<?php session_start();
require '../vendor/autoload.php';
require_once 'config/config.php';

$clientId = getenv('GOOGLE_CLIENT_ID');
$clientSecret = getenv('GOOGLE_CLIENT_SECRET');
$redirectUri = 'https://scp.samana.cloud/api/oauthcallback.php';

$client = new Google_Client();
$client->setClientId($clientId);
$client->setClientSecret($clientSecret);
$client->setRedirectUri($redirectUri);

if (isset($_GET['code'])) {
    $token = $client->fetchAccessTokenWithAuthCode($_GET['code']);
    if (!isset($token['error'])) {
        $google_oauth = new Google_Service_Oauth2($client);
        $google_account_info = $google_oauth->userinfo->get();

        // Encode the user information as a JSON object
        $userData = [
            'accessToken' => $token['access_token'],
            'idToken' => $token['id_token'],
            'email' => rawurldecode($google_account_info->email),
            'name' => $google_account_info->name,
            'picture' => $google_account_info->picture
        ];

        $encodedUserData = urlencode(json_encode($userData));

        // Redirect to the login page with the user data as a query parameter
        header("Location: /auth/login?userData={$encodedUserData}&status=success&message=Authentication%20Succeeded");
        exit();
    } else {
        header("Location: /auth/login?status=error&message=" . urlencode($token['error_description']));
        exit();
    }
} else {
    header("Location: /auth/login?status=error&message=Authorization%20code%20not%20provided");
    exit();
}