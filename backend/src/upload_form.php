<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload File to S3</title>
</head>
<body>
    <h2>Upload File to S3</h2>
    <form action="upload_file.php" method="post" enctype="multipart/form-data">
        <label for="file">Select file to upload:</label>
        <input type="file" name="file" id="file" required>
        <br><br>
        <button type="submit">Upload File</button>
    </form>
</body>
</html>