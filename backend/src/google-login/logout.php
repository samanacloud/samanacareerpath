<?php
session_start();
session_unset();
session_destroy();

// Check if HTTP_REFERER is set and redirect, otherwise redirect to a default page
$redirect_url = isset($_SERVER['HTTP_REFERER']) ? $_SERVER['HTTP_REFERER'] : 'api/';
header('Location: ' . $redirect_url);
exit();
?>