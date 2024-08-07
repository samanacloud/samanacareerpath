<?php
session_start();
require_once  '../config/config.php';
require_once __DIR__ . '/../../vendor/autoload.php';

$config = include('../config/config.php');

$client = new Google_Client();
$client->setClientId($config['google']['client_id']);
$client->setClientSecret($config['google']['client_secret']);
$client->setRedirectUri($config['google']['redirect_uri']);

if (isset($_GET['code'])) {
    $token = $client->fetchAccessTokenWithAuthCode($_GET['code']);
    if (!isset($token['error'])) {
        $client->setAccessToken($token['access_token']);

        $google_oauth = new Google_Service_Oauth2($client);
        $google_account_info = $google_oauth->userinfo->get();
        $google_id = $google_account_info->id;
        $email = $google_account_info->email;
        $name = $google_account_info->name;
        $profile_image = $google_account_info->picture;

        $mysqli = new mysqli("db", $config['database']['user'], $config['database']['pass'], $config['database']['db']); // Use "db" as host

        if ($mysqli->connect_error) {
            http_response_code(500);
            echo json_encode(['error' => 'Database connection failed']);
            exit();
        }

        $result = $mysqli->query("SELECT * FROM users WHERE email = '$email'");
        if ($result->num_rows > 0) {
            $user = $result->fetch_assoc();
            $_SESSION['user_id'] = $user['id'];
            $_SESSION['name'] = $user['name'];
            $_SESSION['email'] = $user['email'];
            $_SESSION['profile_image'] = $user['profile_image'];
        } else {
            $stmt = $mysqli->prepare("INSERT INTO users (google_id, name, email, profile_image) VALUES (?, ?, ?, ?)");
            $stmt->bind_param('ssss', $google_id, $name, $email, $profile_image);
            $stmt->execute();
            $_SESSION['user_id'] = $stmt->insert_id;
            $_SESSION['name'] = $name;
            $_SESSION['email'] = $email;
            $_SESSION['profile_image'] = $profile_image;
            $stmt->close();
        }

        $mysqli->close();

        // Ensure no output before this point
        header('Location: /api/');
        ob_end_flush(); // Flush the buffer and send the output
        exit();
    }
}

// Redirect to a default page on invalid login attempt
header('Location: /api/');
ob_end_flush(); // Flush the buffer and send the output
exit();
?>