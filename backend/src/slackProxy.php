<?php
// Load environment variables
$token = getenv('SLACK_BOT_TOKEN');

// Get the POST data from the frontend
$data = json_decode(file_get_contents('php://input'), true);

if (!isset($data['channel']) || !isset($data['message'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Channel and message are required.']);
    exit();
}

// Prepare the Slack API request
$payload = json_encode([
    'channel' => $data['channel'],
    'text' => $data['message']
]);

$ch = curl_init('https://slack.com/api/chat.postMessage');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Authorization: Bearer ' . $token
]);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);

$response = curl_exec($ch);
curl_close($ch);

echo $response;
?>