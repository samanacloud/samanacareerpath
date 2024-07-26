<?php
header('Content-Type: application/json');

session_start();

// Check if the user is authenticated
if (!isset($_SESSION['user_id'])) {
    http_response_code(401);
    echo json_encode(['error' => 'Unauthorized']);
    exit();
}
// Include configuration
require_once __DIR__ . '/../vendor/autoload.php';

// Load the configuration
$config = include('config/config.php');

// Helper function to send JSON response
function sendJsonResponse($data, $statusCode = 200) {
    http_response_code($statusCode);
    echo json_encode($data);
    exit();
}

// Read incoming JSON request
$request = json_decode(file_get_contents('php://input'), true);

error_log("Received request: " . json_encode($request)); // Log the incoming request

// Check if the action parameter is set
if (!isset($request['action'])) {
    sendJsonResponse(['error' => 'No action specified'], 400);
}

// Route the request based on the action parameter
switch ($request['action']) {
    case 'getUser':
        if (isset($request['userId'])) {
            getUser($request['userId']);
        } else {
            sendJsonResponse(['error' => 'No userId specified'], 400);
        }
        break;
    case 'listUsers':
        listUsers();
        break;

    // Test database connection
    case 'testDbConnection':
        testDbConnection();
        break;

    default:
        sendJsonResponse(['error' => 'Invalid action specified'], 400);
        break;
}

// Example handler function for getting user information
function getUser($userId) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("SELECT * FROM users WHERE id = ?");
    $stmt->bind_param('i', $userId);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $user = $result->fetch_assoc();
        sendJsonResponse($user);
    } else {
        sendJsonResponse(['error' => 'User not found'], 404);
    }

    $stmt->close();
    $mysqli->close();
}

// Handler function for listing all users
function listUsers() {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $result = $mysqli->query("SELECT * FROM users");

    if ($result->num_rows > 0) {
        $users = [];
        while ($row = $result->fetch_assoc()) {
            $users[] = $row;
        }
        sendJsonResponse($users);
    } else {
        sendJsonResponse(['error' => 'No users found'], 404);
    }

    $mysqli->close();
}

// Handler function for testing the database connection
function testDbConnection() {
    global $config;
    error_log("Testing database connection..."); // Log the testDbConnection call
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        error_log("Database connection failed: " . $mysqli->connect_error); // Log connection error
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    } else {
        error_log("Database connection successful."); // Log successful connection
        sendJsonResponse(['success' => true]);
    }

    $mysqli->close();
}
?>