<?php
$clientId = getenv('GOOGLE_CLIENT_ID');
$redirectUri = 'https://scp.samana.cloud/api/oauthcallback.php';
$scope = urlencode('https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/drive.file');
$authUrl = "https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=$clientId&redirect_uri=$redirectUri&scope=$scope&access_type=online";

header("Location: $authUrl");
exit();