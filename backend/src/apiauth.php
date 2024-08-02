<?php
require_once __DIR__ . '/../vendor/autoload.php';
// Load the configuration
$config = include('config/config.php');



use Google\Client;
use Firebase\JWT\JWT;
use Firebase\JWT\JWK;

if (!function_exists('getUserDetailsForAuth')) {
    function getUserDetailsForAuth($email) {
        global $config;
        $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

        if ($mysqli->connect_error) {
            throw new Exception('Database connection failed: ' . $mysqli->connect_error);
        }

        $stmt = $mysqli->prepare("SELECT * FROM users WHERE email = ?");
        $stmt->bind_param('s', $email);
        $stmt->execute();
        $result = $stmt->get_result();

        if ($result->num_rows > 0) {
            $user = $result->fetch_assoc();
            $stmt->close();
            $mysqli->close();
            return $user;
        } else {
            $stmt->close();
            $mysqli->close();
            return null;
        }
    }
}

if (!function_exists('authenticateUser')) {
    function authenticateUser() {
        // Check if session is already started
            if (session_status() !== PHP_SESSION_ACTIVE) {
                session_start();
            }


        // Initialize Google Client
        $client = new Client();
        $client->setClientId($_ENV['GOOGLE_CLIENT_ID']);

        // Check for idToken cookie
        if (isset($_COOKIE['idToken'])) {
            $idToken = $_COOKIE['idToken']; // Use idToken for verification

            // Get the Google signing keys from the public endpoint
            $jwks = json_decode(file_get_contents('https://www.googleapis.com/oauth2/v3/certs'), true);

            try {
                // Parse the JWK key set
                $keys = JWK::parseKeySet($jwks);

                // Manually verify the idToken using Firebase JWT library
                $payload = JWT::decode($idToken, $keys);

                // Token is valid, now check the user details
                $user = getUserDetailsForAuth($payload->email);
                if ($user && isset($user['admin']) && $user['admin'] > 3) {
                    $_SESSION['email'] = $payload->email;
                    return true;
                } else {
                    error_log('User admin field missing or not greater than 3 for email: ' . $payload->email);
                    return false;
                }
            } catch (Exception $e) {
                error_log('JWT verification error: ' . $e->getMessage());
                return false;
            }
        } else {
            // No idToken cookie found
            return false;
        }
    }
}
?>