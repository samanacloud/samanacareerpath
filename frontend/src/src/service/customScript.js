import axios from 'axios';


export async function uploadToAWSS3(file, type, email) {
    // Check the file type based on the provided 'type'
    const allowedFileTypes = {
        CVs: ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
        feedback: ['image/jpeg', 'image/png', 'image/gif'],
        images: ['image/jpeg', 'image/png', 'image/gif'],
    };

    // Set maximum file size based on the type
    const maxFileSize = type === 'CVs' ? 10000000 : 5000000;

    if (!allowedFileTypes[type].includes(file.type)) {
        return { success: false, message: "Invalid file type. Please upload a valid file." };
    }

    if (file.size > maxFileSize) {
        return { success: false, message: `File size exceeds the limit. Maximum allowed size is ${maxFileSize / 1000000} MB.` };
    }

    const reader = new FileReader();

    return new Promise((resolve, reject) => {
        reader.onload = async () => {
            const fileBase64 = reader.result.split(',')[1]; // Get base64 without the prefix

            try {
                const response = await axios.post('/api/upload_file_api', {
                    file: fileBase64,
                    folder: type,
                    email: email,
                    fileName: file.name,
                });

                if (response.data && response.data.url) {
                    resolve({ success: true, url: response.data.url }); // Return success and the uploaded file URL
                } else {
                    resolve({ success: false, message: 'Upload failed.' }); // Return failure message
                }
            } catch (error) {
                console.error('Upload error:', error);
                resolve({ success: false, message: 'An error occurred during file upload.' }); // Return failure message
            }
        };

        reader.onerror = (error) => {
            console.error('File reading error:', error);
            reject({ success: false, message: 'Failed to read the file' }); // Return failure message
        };

        reader.readAsDataURL(file);
    });
}



export async function sendSlackNotification(message, channel) {
    try {
        const response = await axios.post('/api/slackProxy', {
            message: message,
            channel: channel
        });

        if (response.data && response.data.ok) {
            return { success: true };
        } else {
            return { success: false, message: response.data.error || 'Failed to send message to Slack' };
        }
    } catch (error) {
        console.error('Slack notification error:', error);
        return { success: false, message: 'An error occurred while sending the Slack notification.' };
    }
}