<?php
require '../vendor/autoload.php';

use Aws\S3\S3Client;
use Aws\Exception\AwsException;

if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_FILES['file'])) {
    $file = $_FILES['file'];
    
    // Check for upload errors
    if ($file['error'] !== UPLOAD_ERR_OK) {
        die("Upload failed with error code " . $file['error']);
    }
    
    // Create an S3 client
    $s3Client = new S3Client([
        'region' => 'us-east-1',
        'version' => 'latest',
    ]);

    // Define the S3 bucket name and folder
    $bucketName = 'scp-samana-cloud';
    $folder = 'CVs';

    // Generate the full path in the bucket
    $key = $folder . '/' . basename($file['name']);

    try {
        // Upload the file to S3 without specifying ACL
        $result = $s3Client->putObject([
            'Bucket' => $bucketName,
            'Key' => $key,
            'SourceFile' => $file['tmp_name'],
        ]);

        // Generate a pre-signed URL for the uploaded file
        $cmd = $s3Client->getCommand('GetObject', [
            'Bucket' => $bucketName,
            'Key' => $key,
        ]);

        $request = $s3Client->createPresignedRequest($cmd, '+20 minutes'); // Valid for 20 minutes
        $fileUrl = (string) $request->getUri();

        echo "File uploaded successfully. <br>";
        echo "File URL (valid for 20 minutes): <a href='$fileUrl'>$fileUrl</a><br>";
        echo "<embed src='$fileUrl' width='600' height='500' alt='Uploaded file' />";
        } catch (AwsException $e) {
        // Output error message if the upload fails
        echo 'Error uploading file: ' . $e->getMessage();
    }
} else {
    echo "No file uploaded.";
}
?>