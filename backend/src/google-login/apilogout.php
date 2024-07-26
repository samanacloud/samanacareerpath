<?php
require_once '../cors.php'; // Include the CORS settings
session_start();
session_unset();
session_destroy();

// Send JSON response for logout
echo json_encode(['success' => true, 'message' => 'Logout successful']);
exit();
?>