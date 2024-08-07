<?php
session_start();
require_once __DIR__ . '/config/config.php';

$loggedIn = isset($_SESSION['name']);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login with Google</title>
</head>
<body>
    <?php if ($loggedIn): ?>
        <p>Hello, <?php echo htmlspecialchars($_SESSION['name']); ?>!</p>
        <a href="google-login/logout.php"><button>Logout</button></a>
    <?php else: ?>
        <a href="google-login/login.php"><button>Login with Google</button></a>
    <?php endif; ?>
</body>
</html>