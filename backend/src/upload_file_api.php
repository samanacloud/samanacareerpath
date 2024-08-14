<?php
require '../vendor/autoload.php';

use Aws\S3\S3Client;
use Aws\Exception\AwsException;

// Function to send a JSON response
function sendJsonResponse($data, $statusCode = 200) {
    header('Content-Type: application/json');
    http_response_code($statusCode);
    echo json_encode($data);
    exit();
}

// Get the raw POST data
$request = json_decode(file_get_contents('php://input'), true);

// Validate the incoming JSON data
if (!isset($request['file']) || !isset($request['folder']) || !isset($request['email']) || !isset($request['fileName'])) {
    sendJsonResponse(['error' => 'Invalid request. Please provide file, folder, email, and fileName.'], 400);
}

// Extract the data
$fileBase64 = $request['file']; // Assuming the file is sent as a base64 string
$folder = $request['folder'];
$email = $request['email'];

// Determine the file name and folder based on the type
$extension = pathinfo($request['fileName'], PATHINFO_EXTENSION);

switch ($folder) {
    case 'CVs':
        $fileName = $email . '_CV.' . $extension;
        break;
    case 'feedback':
        $fileName = $email . '_feedback.' . $extension;
        break;
    case 'images':
        $fileName = $email . '_image.' . $extension;
        break;
    default:
        sendJsonResponse(['error' => 'Invalid folder specified.'], 400);
}

// Decode the base64 file data
$fileData = base64_decode($fileBase64);
if ($fileData === false) {
    sendJsonResponse(['error' => 'Failed to decode file.'], 400);
}

// Temporarily save the file on the server
$filePath = '/tmp/' . $fileName;

if (file_put_contents($filePath, $fileData) === false) {
    sendJsonResponse(['error' => 'Failed to save file.'], 500);
}

// Create an S3 client
$s3Client = new S3Client([
    'region' => 'us-east-1',
    'version' => 'latest',
]);

$bucketName = 'scp-samana-cloud';

try {
    // Upload the file to S3
    $key = $folder . '/' . $fileName;
    $result = $s3Client->putObject([
        'Bucket' => $bucketName,
        'Key' => $key,
        'SourceFile' => $filePath,
    ]);

    // Get the URL of the uploaded file
    $fileUrl = $s3Client->getObjectUrl($bucketName, $key);

    // Clean up the temporary file
    unlink($filePath);

    // Return the URL in a JSON response
    sendJsonResponse(['url' => $fileUrl]);
} catch (AwsException $e) {
    // Output error message if the upload fails
    sendJsonResponse(['error' => 'Error uploading file: ' . $e->getMessage()], 500);
}
?>