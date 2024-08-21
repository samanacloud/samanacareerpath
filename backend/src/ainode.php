<?php
/// Load environment variables
$slackToken = getenv('SLACK_BOT_TOKEN');
$openAiKey = getenv('OPENAI_API_KEY');

// Ensure the logs directory exists
if (!file_exists('logs')) {
    mkdir('logs', 0777, true);
}

// Simulated in-memory storage for conversation states 
$conversationStates = [];
$thinkingStates = []; // Track if the bot is "Thinking"
$processingStates = []; // Track if the bot is processing an OpenAI request

// Function to get the conversation state for a user
function getConversationState($user) {
    global $conversationStates;
    return isset($conversationStates[$user]) ? $conversationStates[$user] : 'WAITING_FOR_GREETING';
}

// Function to set the conversation state for a user
function setConversationState($user, $state) {
    global $conversationStates;
    $conversationStates[$user] = $state;
}

// Function to check if the bot is "Thinking"
function isThinking($user) {
    global $thinkingStates;
    return isset($thinkingStates[$user]) ? $thinkingStates[$user] : false;
}

// Function to set the "Thinking" state
function setThinking($user, $state) {
    global $thinkingStates;
    $thinkingStates[$user] = $state;
}

// Function to check if the bot is already processing an OpenAI request
function isProcessing($eventId) {
    global $processingStates;
    return isset($processingStates[$eventId]) ? $processingStates[$eventId] : false;
}

// Function to set the processing state
function setProcessing($eventId, $state) {
    global $processingStates;
    $processingStates[$eventId] = $state;
}

// Function to send a message to Slack
function sendSlackMessage($channel, $message) {
    global $slackToken;
    $payload = json_encode([
        'channel' => $channel,
        'text' => $message
    ]);

    $ch = curl_init('https://slack.com/api/chat.postMessage');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json',
        'Authorization: Bearer ' . $slackToken
    ]);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);

    $response = curl_exec($ch);
    curl_close($ch);

    if ($httpCode != 200) {
        error_log("Error sending Slack message: " . $response); // Log the error for debugging
        // Handle the error if necessary
    }
}

// Function to send a question to OpenAI and get the response
function askOpenAI($question) {
    global $openAiKey;

    // Simplified prompt
    $prompt = "You are an expert in cloud computing and IT support. Assist the L1 Support Desk Engineers by answering the following question concisely and within the max of slack messages accepted. Provide up to 3 relevant links to official documentation or approved blogs. Focus only on relevant information. The question is: \"$question\"";

    $payload = json_encode([
        'model' => 'gpt-4o-mini',
        'messages' => [['role' => 'user', 'content' => $prompt]],
        'temperature' => 0.7,
        'max_tokens' => 200
    ]);

    $ch = curl_init('https://api.openai.com/v1/chat/completions');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json',
        'Authorization: Bearer ' . $openAiKey
    ]);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);

    $response = curl_exec($ch);
    curl_close($ch);

    $decodedResponse = json_decode($response, true);
    return $decodedResponse['choices'][0]['message']['content'] ?? 'I encountered an error.';
}

// Function to check if an event has been processed
function isEventProcessed($eventId) {
    return file_exists("processed_events/{$eventId}.txt"); 
}

// Function to mark an event as processed
function markEventProcessed($eventId) {
    if (!file_exists('processed_events')) {
        mkdir('processed_events', 0777, true);
    }

    touch("processed_events/{$eventId}.txt"); 
}

// Main function to process incoming Slack events
function handleSlackEvent($data) {
    $user = $data['event']['user'];
    $channel = $data['event']['channel'];
    $text = $data['event']['text'];
    $botUserId = $data['authorizations'][0]['user_id'];
    $eventId = $data['event_id'];
    $isDirectMessage = $data['event']['channel_type'] === 'im';

    // Process only if it's a direct message, not from the bot itself, and hasn't been processed before
    if ($isDirectMessage && $user !== $botUserId && !isEventProcessed($eventId)) {
        // Immediately send a 200 OK response to Slack to prevent retries
        http_response_code(200); 

        // Check if the bot is already processing this specific event
        if (!isProcessing($eventId)) {
            // Set the bot to "Processing" state for this event
            setProcessing($eventId, true);

            // Check if the bot is already "Thinking"
            if (!isThinking($user)) {
                // Send "Thinking..." message only once
                sendSlackMessage($channel, "Thinking...");
                setThinking($user, true);
            }

            // Send the question to OpenAI and get the response
            $response = askOpenAI($text);

            // Send the OpenAI response to the user
            sendSlackMessage($channel, $response);

            // Mark the event as processed
            markEventProcessed($eventId);

            // Reset the thinking state
            setThinking($user, false);

            // Reset the processing state
            setProcessing($eventId, false);
        }
    }
}

// Function to get recommended training from OpenAI
function showRecommendedTraining($certifications) {
    global $openAiKey;

    $prompt = $certifications
        ? "Search in the pluralsight website and Provide only 3 recent training courses with descriptions and links that help the student improve their skillsets in complementary technologies using as base that they already have knowledge on the following certifications: {$certifications}. Format the response as JSON with the following structure: title, description, and link. Do not provide anything else."
        : "Search in the pluralsight website and Provide only 3 recent training courses with descriptions and links for career development. Format the response as JSON with the following structure: title, description, and link. Do not provide anything else.";

    $payload = json_encode([
        'model' => 'gpt-4o-mini',
        'messages' => [
            ['role' => 'system', 'content' => 'You are a trainer specialized in IT, that gives training recommendations for a team of engineers that works in a IT managed services company. Every request, you search to identify on internet and provide only updated content.'],
            ['role' => 'user', 'content' => $prompt]
        ],
        'max_tokens' => 500,
        'n' => 1,
        'temperature' => 0.7,
    ]);

    $ch = curl_init('https://api.openai.com/v1/chat/completions');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json',
        'Authorization: Bearer ' . $openAiKey,
    ]);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);

    $response = curl_exec($ch);
    curl_close($ch);

    $decodedResponse = json_decode($response, true);

    if (isset($decodedResponse['choices'][0]['message']['content'])) {
        $messageContent = trim($decodedResponse['choices'][0]['message']['content']);

        // Remove Markdown code block delimiters
        $messageContent = str_replace(["```json", "```"], '', $messageContent);

        // Try to decode the JSON content
        $trainingData = json_decode($messageContent, true);

        // Check if the JSON decoding was successful
        if (json_last_error() === JSON_ERROR_NONE) {
            return $trainingData; // Return the valid training data
        } else {
            // Log the raw content for debugging
            error_log("Invalid JSON format received from OpenAI: " . $messageContent);
            return ['error' => 'Invalid JSON format received from OpenAI', 'raw' => $messageContent];
        }
    } else {
        return ['error' => 'No valid content received from OpenAI'];
    }
}


// Process the incoming request
$data = json_decode(file_get_contents('php://input'), true);
if (isset($data['event']) && $data['event']['type'] === 'message' && !isset($data['event']['subtype'])) {
    handleSlackEvent($data);
}

if (isset($data['certifications'])) {
    $certifications = $data['certifications'];
    $recommendedTraining = showRecommendedTraining($certifications);

    header('Content-Type: application/json');
    echo json_encode(['recommendedTraining' => $recommendedTraining]);
} else {
    echo json_encode(['error' => 'Invalid request']);
}