<?php
// Allow CORS requests from any origin
require_once 'cors.php';  // Include the CORS settings
require_once 'apiauth.php'; //Authentication function for the API, uses the authentication key generated in the frontend session to use it in the backend session.
ob_start();

if (!function_exists('sendJsonResponse')) {
    function sendJsonResponse($data, $statusCode = 200) {
        ob_end_clean(); // Clean the buffer and turn off output buffering
        header('Content-Type: application/json');
        http_response_code($statusCode);
        echo json_encode($data);
        exit();
    }
}





header('Content-Type: application/json');

// Include configuration
require_once __DIR__ . '/../vendor/autoload.php';

// Load the configuration
$config = include('config/config.php');

// Helper function to send JSON response
function sendJsonResponse($data, $statusCode = 200) {
    http_response_code($statusCode);
    echo json_encode($data);
    exit();
}

// Read incoming JSON request
$request = json_decode(file_get_contents('php://input'), true);

error_log("Received request: " . json_encode($request)); // Log the incoming request

// Check if the action parameter is set
if (!isset($request['action'])) {
    sendJsonResponse(['error' => 'No action specified'], 400);
}


// Route the request based on the action parameter
switch ($request['action']) {
    case 'getUser':
        if (isset($request['userId'])) {
            getUser($request['userId']);
        } else {
            sendJsonResponse(['error' => 'No userId specified'], 400);
        }
        break;

    case 'getUserDetails':
        if (isset($request['email'])) {
            getUserDetails($request['email']);
        } else {
            sendJsonResponse(['error' => 'No Email specified'], 400);
        }
        break;
    case 'listUsers':
        listUsers();
        break;
    
    case 'getOverallInfo':
            getOverallInfo();
            break;
    // Test database connection
    case 'testDbConnection':
        testDbConnection();
        break;
    
    case 'listCandidateProfiles':
            listCandidateProfiles();
            break;

    case 'listCandidateSkillsets':
            if (isset($request['email'])) {
                listCandidateSkillsets($request['email']);
            } else {
                sendJsonResponse(['error' => 'No email specified'], 400);
            }
            break;
   case 'listCandidateReviews':
            if (isset($request['email'])) {
                listCandidateReviews($request['email']);
           } else {
                 sendJsonResponse(['error' => 'No email specified'], 400);
            }
            break;
    case 'listCandidateRegistrations':
        if (isset($request['email'])) {
            listCandidateRegistrations($request['email']);
        } else {
                sendJsonResponse(['error' => 'No email specified'], 400);
        }
        break;
    case 'listJobPostings':
                listJobPostings();
                break;
    case 'listAvailableJobs':
                listAvailableJobs();
                break;


    case 'getCandidate':
            if (isset($request['email'])) {
             getCandidate($request['email']);
            } else {
             sendJsonResponse(['error' => 'No email specified'], 400);
                    }
                    break;
    case 'addCandidate':
        if (isset($request['name'], $request['email'], $request['phone_number'], $request['location'], $request['english_level'], $request['profile_photo'], $request['candidate_cv'], $request['created_at'], $request['enabled'])) {
            addCandidate(
                $request['name'],
                $request['email'],
                $request['phone_number'],
                $request['location'],
                $request['english_level'],
                $request['profile_photo'],
                $request['candidate_cv'],
                $request['created_at'],
                $request['enabled']
            );
        } else {
            sendJsonResponse(['error' => 'Missing parameters'], 400);
        }
        break;

        case 'updateCandidate':
            if (isset($request['id'], $request['name'], $request['email'], $request['phone_number'], $request['location'], $request['english_level'], $request['profile_photo'], $request['candidate_cv'], $request['enabled'])) {
                updateCandidate(
                    $request['id'],
                    $request['name'],
                    $request['email'],
                    $request['phone_number'],
                    $request['location'],
                    $request['english_level'],
                    $request['profile_photo'],
                    $request['candidate_cv'],
                    $request['enabled']
                );
            } else {
                sendJsonResponse(['error' => 'Missing parameters'], 400);
            }
            break;
        
        case 'deleteCandidate':
            if (isset($request['id'])) {
                deleteCandidate($request['id']);
            } else {
                sendJsonResponse(['error' => 'Missing parameters'], 400);
            }
            break;
                
                
                    


    case 'listCandidateCertifications':
            if (isset($request['email'])) {
                            listCandidateCertifications($request['email']);
                        } else {
                            sendJsonResponse(['error' => 'No email specified'], 400);
                        }
            break;
    
    case 'jobDetails':
                if (isset($request['id'])) {
                    jobDetails($request['id']);
                } else {
                    sendJsonResponse(['error' => 'No id specified'], 400);
                }
                break;

    case 'getCandidatesByProcess':
                    if (isset($request['processId'])) {
                        getCandidatesByProcess($request['processId']);
                    } else {
                        sendJsonResponse(['error' => 'No processId specified'], 400);
                    }
                    break;
    case 'getCandidateReviews':
                        if (isset($request['email']) && isset($request['processId'])) {
                            getCandidateReviews($request['email'], $request['processId']);
                        } else {
                            sendJsonResponse(['error' => 'No email or processId specified'], 400);
                        }
                        break;
    case 'listJobCategories':
                            listJobCategories();
                            break;
                        
    case 'addJobCategory':
                                if (isset($request['category_name'])) {
                                    addJobCategory($request['category_name']);
                                } else {
                                    sendJsonResponse(['error' => 'No category name specified'], 400);
                                }
                                break;
    
    case 'updateJobCategory':
                                    if (isset($request['id']) && isset($request['category_name'])) {
                                        updateJobCategory($request['id'], $request['category_name']);
                                    } else {
                                        sendJsonResponse(['error' => 'No id or category name specified'], 400);
                                    }
                                    break;                       
    case 'deleteJobCategory':
                                        if (isset($request['id'])) {
                                            deleteJobCategory($request['id']);
                                        } else {
                                            sendJsonResponse(['error' => 'No id specified'], 400);
                                        }
                                        break;

    case 'listJobSkillsets':
        listJobSkillsets();
        break;
    
    case 'addJobSkillset':
            if (isset($request['category_id']) && isset($request['skillset_name'])) {
                addJobSkillset($request['category_id'], $request['skillset_name']);
            } else {
                sendJsonResponse(['error' => 'No category ID or skillset name specified'], 400);
            }
            break;
case 'updateJobSkillset':
        if (isset($request['id']) && isset($request['category_id']) && isset($request['skillset_name'])) {
            updateJobSkillset($request['id'], $request['category_id'], $request['skillset_name']);
        } else {
            sendJsonResponse(['error' => 'No id, category ID, or skillset name specified'], 400);
        }
        break;                                           

    case 'deleteJobSkillset':
        if (isset($request['id'])) {
            deleteJobSkillset($request['id']);
        } else {
            sendJsonResponse(['error' => 'No id specified'], 400);
        }
        break;
                                                    
    case 'listJobCategoriesAndSkillsets': // New case for combined data
        listJobCategoriesAndSkillsets(); // Call the new function
     break;

    case 'listCertifications':
        listCertifications();
        break;
    
    case 'addCertification':
        if (isset($request['certification'])) {
            addCertification($request['certification']);
        } else {
            sendJsonResponse(['error' => 'No certification specified'], 400);
        }
        break;
    
    case 'updateCertification':
        if (isset($request['id']) && isset($request['certification'])) {
            updateCertification($request['id'], $request['certification']);
        } else {
            sendJsonResponse(['error' => 'No id or certification specified'], 400);
        }
        break;
    
    case 'deleteCertification':
        if (isset($request['id'])) {
            deleteCertification($request['id']);
        } else {
            sendJsonResponse(['error' => 'No id specified'], 400);
        }
        break;
                
        case 'getReviewerName':
            if (isset($request['email'])) {
                getReviewerName($request['email']);
            } else {
                sendJsonResponse(['error' => 'No email specified'], 400);
            }
            break;
        

            case 'setCandidateSkillSet':
                if (isset($request['candidate_id']) && isset($request['email']) && isset($request['category']) && isset($request['skillset']) && isset($request['rating']) && isset($request['reviewer_id']) && isset($request['reviewer_email']) && isset($request['timestamp'])) {
                    setCandidateSkillSet($request['candidate_id'], $request['email'], $request['category'], $request['skillset'], $request['rating'], $request['reviewer_id'], $request['reviewer_email'], $request['comment'] ?? '', $request['timestamp']);
                } else {
                    sendJsonResponse(['error' => 'Missing parameters'], 400);
                }
                break;


        case 'getCandidateSkillset':
                if (isset($request['reviewer_email']) && isset($request['candidate_email'])) {
                    getCandidateSkillset($request['reviewer_email'], $request['candidate_email']);
                } else {
                    sendJsonResponse(['error' => 'No reviewer_email or candidate_email specified'], 400);
                }
                break;

    case 'deleteCandidateSkillset':
        if (isset($request['id'])) {
            deleteCandidateSkillset($request['id']);
        } else {
            sendJsonResponse(['error' => 'No ID specified'], 400);
        }
        break;

        case 'getSkillsetCategory':
            if (isset($request['id'])) {
                getSkillsetCategory($request['id']);
            } else {
                sendJsonResponse(['error' => 'No category ID specified'], 400);
            }
            break;
            case 'createInterview':
                if (isset($request['email']) && isset($request['process']) && isset($request['salary_expectation']) && isset($request['availability']) && isset($request['interview']) && isset($request['interviewer_name']) && isset($request['interviewer_email']) && isset($request['evaluation_field']) && isset($request['rating']) && isset($request['observations']) && isset($request['approved']) && isset($request['review_date'])) {
                    createInterview($request['email'], $request['process'], $request['salary_expectation'], $request['availability'], $request['interview'], $request['interviewer_name'], $request['interviewer_email'], $request['evaluation_field'], $request['rating'], $request['observations'], $request['approved'], $request['review_date']);
                } else {
                    sendJsonResponse(['error' => 'Missing parameters'], 400);
                }
                break;
        
                case 'getInterviews':
                    if (isset($request['interviewer_email']) && isset($request['candidate_email'])) {
                        getInterviews($request['interviewer_email'], $request['candidate_email']);
                    } else {
                        sendJsonResponse(['error' => 'Missing parameters'], 400);
                    }
                    break;
        
            case 'updateInterview':
                if (isset($request['id']) && isset($request['email']) && isset($request['process']) && isset($request['salary_expectation']) && isset($request['availability']) && isset($request['interview']) && isset($request['interviewer_name']) && isset($request['interviewer_email']) && isset($request['evaluation_field']) && isset($request['rating']) && isset($request['observations']) && isset($request['approved']) && isset($request['review_date'])) {
                    updateInterview($request['id'], $request['email'], $request['process'], $request['salary_expectation'], $request['availability'], $request['interview'], $request['interviewer_name'], $request['interviewer_email'], $request['evaluation_field'], $request['rating'], $request['observations'], $request['approved'], $request['review_date']);
                } else {
                    sendJsonResponse(['error' => 'Missing parameters'], 400);
                }
                break;
        
        case 'deleteInterview':
            if (isset($request['id'])) {
                deleteInterview($request['id']);
            } else {
                sendJsonResponse(['error' => 'Missing parameters'], 400);
            }
            break;

    case 'addSystemUser':
        if (isset($request['google_id'], $request['name'], $request['email'], $request['profile_image'], $request['admin'])) {
            addSystemUser($request['google_id'], $request['name'], $request['email'], $request['profile_image'], $request['admin']);
        } else {
            sendJsonResponse(['error' => 'Missing parameters'], 400);
        }
        break;
    
    case 'updateSystemUser':
        if (isset($request['id'], $request['google_id'], $request['name'], $request['email'], $request['profile_image'], $request['admin'])) {
            updateSystemUser($request['id'], $request['google_id'], $request['name'], $request['email'], $request['profile_image'], $request['admin']);
        } else {
            sendJsonResponse(['error' => 'Missing parameters'], 400);
        }
        break;
    
    case 'deleteSystemUser':
        if (isset($request['id'])) {
            deleteSystemUser($request['id']);
        } else {
            sendJsonResponse(['error' => 'Missing parameters'], 400);
        }
        break;
    
    case 'listSystemUsers':
        listSystemUsers();
        break;
        case 'listEmployees':
            listEmployees();
            break;
    
        case 'addEmployee':
            if (isset($request['primaryEmail'], $request['fullName'], $request['companyRole'], $request['contractType'], $request['suspended'], $request['creationDate'])) {
                addEmployee(
                    $request['primaryEmail'],
                    $request['recoveryEmail'] ?? null,
                    $request['fullName'],
                    $request['phone_mobile'] ?? null,
                    $request['thumbnailPhotoURL'] ?? null,
                    $request['companyRole'],
                    $request['contractType'],
                    $request['suspended'],
                    $request['creationDate']
                );
            } else {
                sendJsonResponse(['error' => 'Missing parameters'], 400);
            }
            break;
    

            case 'getEmployee':
                if (isset($request['email'])) {
                    getEmployee($request['email']);
                } else {
                    sendJsonResponse(['error' => 'No email specified'], 400);
                }
                break;
        
                case 'updateEmployee':
                    if (isset($request['ID'], $request['primaryEmail'], $request['fullName'], $request['companyRole'], $request['contractType'], $request['suspended'], $request['creationDate'])) {
                        updateEmployee(
                            $request['ID'],
                            $request['primaryEmail'],
                            $request['recoveryEmail'] ?? null,
                            $request['fullName'],
                            $request['phone_mobile'] ?? null,
                            $request['thumbnailPhotoURL'] ?? null,
                            $request['companyRole'],
                            $request['contractType'],
                            $request['suspended'],
                            $request['creationDate']
                        );
                    } else {
                        sendJsonResponse(['error' => 'Missing parameters'], 400);
                    }
                    break;

        case 'deleteEmployee':
            if (isset($request['id'])) {
                deleteEmployee($request['id']);
            } else {
                sendJsonResponse(['error' => 'No ID specified'], 400);
            }
            break;
    
            case 'listEmployeeCertifications':
                if (isset($request['email'])) {
                    listEmployeeCertifications($request['email']);
                } else {
                    sendJsonResponse(['error' => 'No email specified'], 400);
                }
                break;
        
            case 'addEmployeeCertification':
                if (isset($request['email'], $request['certification'], $request['date'])) {
                    addEmployeeCertification($request['email'], $request['certification'], $request['date']);
                } else {
                    sendJsonResponse(['error' => 'Missing parameters'], 400);
                }
                break;
        
            case 'deleteEmployeeCertification':
                if (isset($request['id'])) {
                    deleteEmployeeCertification($request['id']);
                } else {
                    sendJsonResponse(['error' => 'No ID specified'], 400);
                }
                break;
    case 'listEmployeeSkillsets':
        if (isset($request['email'])) {
            listEmployeeSkillsets($request['email']);
        } else {
            sendJsonResponse(['error' => 'No email specified'], 400);
        }
        break;

    case 'addEmployeeSkillset':
        if (isset($request['employee_id'], $request['email'], $request['category'], $request['skillset'], $request['rating'], $request['reviewer_email'], $request['date'])) {
            addEmployeeSkillset($request['employee_id'], $request['email'], $request['category'], $request['skillset'], $request['rating'], $request['reviewer_email'], $request['date']);
        } else {
            sendJsonResponse(['error' => 'Missing parameters'], 400);
        }
        break;

    case 'deleteEmployeeSkillset':
        if (isset($request['id'])) {
            deleteEmployeeSkillset($request['id']);
        } else {
            sendJsonResponse(['error' => 'No ID specified'], 400);
        }
        break;
    case 'listEmployeeReviews':
        if (isset($request['email'])) {
            listEmployeeReviews($request['email']);
        } else {
            sendJsonResponse(['error' => 'No email specified'], 400);
        }
        break;
    case 'listPublicEmployeeReviews':
        if (isset($request['email'])) {
            listPublicEmployeeReviews($request['email']);
        } else {
            sendJsonResponse(['error' => 'No email specified'], 400);
        }
        break;

case 'listAllReviews':
            listAllReviews();
            break;
        
    case 'addEmployeeReview':
        if (isset($request['employee_id'], $request['email'], $request['evaluation_field'], $request['rating'], $request['reviewer_email'], $request['observations'], $request['date'], $request['public'])) {
            addEmployeeReview($request['employee_id'], $request['email'], $request['evaluation_field'], $request['rating'], $request['reviewer_email'], $request['observations'], $request['date'], $request['public']);
        } else {
            sendJsonResponse(['error' => 'Missing parameters'], 400);
        }
        break;

    case 'deleteEmployeeReview':
        if (isset($request['id'])) {
            deleteEmployeeReview($request['id']);
        } else {
            sendJsonResponse(['error' => 'No ID specified'], 400);
        }
        break;

        case 'updateEmployeeReview':
            if (isset($request['id'], $request['employee_id'], $request['email'], $request['evaluation_field'], $request['rating'], $request['reviewer_email'], $request['observations'], $request['date'], $request['public'])) {
                updateEmployeeReview($request['id'], $request['employee_id'], $request['email'], $request['evaluation_field'], $request['rating'], $request['reviewer_email'], $request['observations'], $request['date'], $request['public']);
            } else {
                sendJsonResponse(['error' => 'Missing parameters'], 400);
            }
            break;
        
        

        
        
            // Add this in the switch statement of apitest.php
        case 'addCandidateCertification':
            if (isset($request['email'], $request['certification'])) {
                addCandidateCertification($request['email'], $request['certification']);
            } else {
                sendJsonResponse(['error' => 'Missing parameters'], 400);
            }
            break;

        case 'deleteCandidateCertification':
            if (isset($request['email'], $request['certification'])) {
                deleteCandidateCertification($request['email'], $request['certification']);
            } else {
                sendJsonResponse(['error' => 'Missing parameters'], 400);
            }
            break;
        case 'addCandidateReview':
            if (isset($request['email'], $request['process'], $request['salary_expectation'], $request['availability'], $request['interview'], $request['interviewer_name'], $request['interviewer_email'], $request['evaluation_field'], $request['rating'], $request['observations'], $request['approved'], $request['review_date'])) {
                addCandidateReview($request['email'], $request['process'], $request['salary_expectation'], $request['availability'], $request['interview'], $request['interviewer_name'], $request['interviewer_email'], $request['evaluation_field'], $request['rating'], $request['observations'], $request['approved'], $request['review_date']);
            } else {
                sendJsonResponse(['error' => 'Missing parameters'], 400);
            }
            break;
    
        case 'removeCandidateReview':
            if (isset($request['id'], $request['interviewer_email'])) {
                removeCandidateReview($request['id'], $request['interviewer_email']);
            } else {
                sendJsonResponse(['error' => 'Missing parameters'], 400);
            }
            break;
   
    case 'getJobProcess':
        getJobProcess();
        break;   

        case 'getCandidateSalaryExpectation':
            if (isset($request['email'])) {
                getCandidateSalaryExpectation($request['email']);
            } else {
                sendJsonResponse(['error' => 'Email not provided'], 400);
            }
            break;

            // Add these case statements in the switch statement of apitest.php

case 'listAdminRoles':
    listAdminRoles();
    break;

case 'addAdminRole':
    if (isset($request['functionName']) && isset($request['authrole'])) {
        addAdminRole($request['functionName'], $request['authrole']);
    } else {
        sendJsonResponse(['error' => 'Missing parameters'], 400);
    }
    break;

case 'updateAdminRole':
    if (isset($request['id']) && isset($request['functionName']) && isset($request['authrole'])) {
        updateAdminRole($request['id'], $request['functionName'], $request['authrole']);
    } else {
        sendJsonResponse(['error' => 'Missing parameters'], 400);
    }
    break;

case 'deleteAdminRole':
    if (isset($request['id'])) {
        deleteAdminRole($request['id']);
    } else {
        sendJsonResponse(['error' => 'Missing parameters'], 400);
    }
    break;

// Add this case statement in the switch statement of apitest.php

case 'getAdminRole':
    if (isset($request['functionName'])) {
        getAdminRole($request['functionName']);
    } else {
        sendJsonResponse(['error' => 'No functionName specified'], 400);
    }
    break;
    // Add these cases in the switch statement of apitest.php

case 'listAllEmployeeCertifications':
    listAllEmployeeCertifications();
    break;

case 'listAllCandidateCertifications':
    listAllCandidateCertifications();
    break;

case 'listAllEmployeeSkillsets':
    listAllEmployeeSkillsets();
    break;

case 'listAllCandidateSkillsets':
    listAllCandidateSkillsets();
    break;
case 'addFeedback':
    if (isset($request['type']) && isset($request['description'])) {
        $email = isset($request['email']) ? (is_array($request['email']) ? implode(', ', $request['email']) : $request['email']) : null;
        $screenshotUrl = isset($request['screenshotUrl']) ? (is_array($request['screenshotUrl']) ? implode(', ', $request['screenshotUrl']) : $request['screenshotUrl']) : null;
        addFeedback($request['type'], $request['description'], $email, $screenshotUrl);
    } else {
        sendJsonResponse(['error' => 'Type and description are required'], 400);
    }
    break;

    case 'updateFeedback':
        if (isset($request['id'])) {
            $type = isset($request['type']) ? $request['type'] : null;
            $description = isset($request['description']) ? $request['description'] : null;
            $email = isset($request['email']) ? $request['email'] : null;
            $screenshotUrl = isset($request['screenshotUrl']) ? $request['screenshotUrl'] : null;
            $status = isset($request['status']) ? $request['status'] : null;
            $date_closed = isset($request['date_closed']) ? $request['date_closed'] : null;
            updateFeedback($request['id'], $type, $description, $email, $screenshotUrl, $status, $date_closed);
        } else {
            sendJsonResponse(['error' => 'No feedback ID specified'], 400);
        }
        break;

    case 'listFeedback':
        listFeedback();
        break;

    case 'deleteFeedback':
        if (isset($request['id'])) {
            deleteFeedback($request['id']);
        } else {
            sendJsonResponse(['error' => 'No feedback ID specified'], 400);
        }
        break;
    // New case for handling employee enrollment actions
    case 'addEmployeeEnrollment':
        if (isset($request['email']) && isset($request['step']) && isset($request['value'])) {
            addEmployeeEnrollment($request['email'], $request['step'], $request['value']);
        } else {
            sendJsonResponse(['error' => 'Missing required parameters'], 400);
        }
        break;

    case 'listEmployeeEnrollment':
        if (isset($request['email'])) {
            listEmployeeEnrollment($request['email']);
        } else {
            sendJsonResponse(['error' => 'No email specified'], 400);
        }
        break;

    case 'deleteEmployeeEnrollment':
        if (isset($request['id'])) {
            deleteEmployeeEnrollment($request['id']);
        } else {
            sendJsonResponse(['error' => 'No ID specified'], 400);
        }
        break;
    default:
        sendJsonResponse(['error' => 'Invalid action specified'], 400);
        break;

    case 'getEnrollmentStatus':
        if (isset($request['email'])) {
            getEnrollmentStatus($request['email']);
        } else {
            sendJsonResponse(['error' => 'No email specified'], 400);
        }
        break;
    
}

//  handler function for getting user information
function getUser($userId) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("SELECT * FROM users WHERE id = ?");
    $stmt->bind_param('i', $userId);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $user = $result->fetch_assoc();
        sendJsonResponse($user);
    } else {
        sendJsonResponse(['error' => 'User not found'], 404);
    }

    $stmt->close();
    $mysqli->close();
}

function getUserDetails($email) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("SELECT * FROM users WHERE email = ?");
    $stmt->bind_param('s', $email);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $user = $result->fetch_assoc();
        sendJsonResponse($user);
    } else {
        sendJsonResponse(['error' => 'User not found'], 404);
    }

    $stmt->close();
    $mysqli->close();
}
// Handler function for listing all users
function listUsers() {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $result = $mysqli->query("SELECT * FROM users");

    if ($result->num_rows > 0) {
        $users = [];
        while ($row = $result->fetch_assoc()) {
            $users[] = $row;
        }
        sendJsonResponse($users);
    } else {
        sendJsonResponse(['error' => 'No users found'], 404);
    }

    $mysqli->close();
}

// Handler function for testing the database connection
function testDbConnection() {
    global $config;
    error_log("Testing database connection..."); // Log the testDbConnection call
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        error_log("Database connection failed: " . $mysqli->connect_error); // Log connection error
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    } else {
        error_log("Database connection successful."); // Log successful connection
        sendJsonResponse(['success' => true]);
    }

    $mysqli->close();
}

// Handler function for listing all candidate profiles
function listCandidateProfiles() {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $result = $mysqli->query("SELECT * FROM candidate_profiles ORDER BY name ASC");

    if ($result->num_rows > 0) {
        $candidateProfiles = [];
        while ($row = $result->fetch_assoc()) {
            $candidateProfiles[] = $row;
        }
        sendJsonResponse($candidateProfiles);
    } else {
        sendJsonResponse(['error' => 'No candidate profiles found'], 404);
    }

    $mysqli->close();
}

// Handler function for listing candidate skillsets based on email
function listCandidateSkillsets($email) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("SELECT * FROM candidate_skillsets WHERE email = ? ORDER BY category, skillset ASC");
    $stmt->bind_param('s', $email);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $skillsets = [];
        while ($row = $result->fetch_assoc()) {
            $skillsets[] = $row;
        }
        sendJsonResponse($skillsets);
    } else {
        sendJsonResponse(['error' => 'No skillsets found for the specified email'], 404);
    }

    $stmt->close();
    $mysqli->close();
}

// Handler function for listing candidate reviews based on email
function listCandidateReviews($email) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("SELECT * FROM candidate_review WHERE email = ?");
    $stmt->bind_param('s', $email);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $reviews = [];
        while ($row = $result->fetch_assoc()) {
            $reviews[] = $row;
        }
        sendJsonResponse($reviews);
    } else {
        sendJsonResponse(['error' => 'No reviews found for the specified email'], 404);
    }

    $stmt->close();
    $mysqli->close();
}


// Handler function for listing candidate registrations
function listCandidateRegistrations($email) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("SELECT process FROM candidate_review WHERE email = ? AND interview = 'Registration'");
    $stmt->bind_param('s', $email);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $reviews = [];
        while ($row = $result->fetch_assoc()) {
            $reviews[] = $row;
        }
        sendJsonResponse($reviews);
    } else {
        sendJsonResponse(['error' => 'No reviews found for the specified email'], 404);
    }

    $stmt->close();
    $mysqli->close();
}

// Handler function for getting all the job postings
function listJobPostings() {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $result = $mysqli->query("SELECT * FROM job_postings ORDER BY id");

    if ($result->num_rows > 0) {
        $jobPostings = [];
        while ($row = $result->fetch_assoc()) {
            $jobPostings[] = $row;
        }
        sendJsonResponse($jobPostings);
    } else {
        sendJsonResponse(['error' => 'No job postings found'], 404);
    }

    $mysqli->close();
}


// Handler function for getting all the job postings
function listAvailableJobs() {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $result = $mysqli->query("SELECT * FROM job_postings WHERE enabled=1 ORDER BY id");

    if ($result->num_rows > 0) {
        $jobPostings = [];
        while ($row = $result->fetch_assoc()) {
            $jobPostings[] = $row;
        }
        sendJsonResponse($jobPostings);
    } else {
        sendJsonResponse(['error' => 'No job postings found'], 404);
    }

    $mysqli->close();
}
// Handler function for getting job details by ID
function jobDetails($id) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("SELECT * FROM job_postings WHERE id = ?");
    $stmt->bind_param('i', $id);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $jobPosting = $result->fetch_assoc();
        sendJsonResponse($jobPosting);
    } else {
        sendJsonResponse(['error' => 'Job posting not found'], 404);
    }

    $stmt->close();
    $mysqli->close();
}


// Handler function for getting candidate information by email
function getCandidate($email) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("SELECT * FROM candidate_profiles WHERE email = ? ORDER BY name");
    $stmt->bind_param('s', $email);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $candidate = $result->fetch_assoc();
        sendJsonResponse($candidate);
    } else {
        sendJsonResponse(['error' => 'Candidate not found'], 404);
    }

    $stmt->close();
    $mysqli->close();
}

// Handler function for listing candidate certifications based on email
function listCandidateCertifications($email) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("SELECT * FROM candidate_certifications WHERE email = ? ORDER BY certification ASC ");
    $stmt->bind_param('s', $email);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $certifications = [];
        while ($row = $result->fetch_assoc()) {
            $certifications[] = $row;
        }
        sendJsonResponse($certifications);
    } else {
        sendJsonResponse(['error' => 'No certifications found for the specified email'], 404);
    }

    $stmt->close();
    $mysqli->close();
}


// Function to get candidate names and emails by process
function getCandidatesByProcess($processId) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("
        SELECT cp.name, cp.email
        FROM candidate_profiles cp
        JOIN candidate_review cr ON cp.email = cr.email
        WHERE cr.Process = ? AND cr.interview = 'First Interview'
    ");
    $stmt->bind_param('i', $processId);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $candidates = [];
        while ($row = $result->fetch_assoc()) {
            $candidates[] = $row;
        }
        sendJsonResponse($candidates);
    } else {
        sendJsonResponse(['error' => 'No candidates found for the specified process'], 404);
    }

    $stmt->close();
    $mysqli->close();
}

// Function to get candidate reviews by email and process ID
function getCandidateReviews($email, $processId) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("
        SELECT interview, interviewer_name, rating, approved
        FROM candidate_review
        WHERE email = ? AND Process = ?
    ");
    $stmt->bind_param('si', $email, $processId);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $reviews = [];
        while ($row = $result->fetch_assoc()) {
            $reviews[] = $row;
        }
        sendJsonResponse($reviews);
    } else {
        sendJsonResponse(['error' => 'No reviews found for the specified email and process ID'], 404);
    }

    $stmt->close();
    $mysqli->close();
}

function listJobCategories() {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $result = $mysqli->query("SELECT * FROM job_categories ORDER BY category_name ASC");

    if ($result->num_rows > 0) {
        $jobCategories = [];
        while ($row = $result->fetch_assoc()) {
            $jobCategories[] = $row;
        }
        sendJsonResponse($jobCategories);
    } else {
        sendJsonResponse(['error' => 'No job categories found'], 404);
    }

    $mysqli->close();
}

function addJobCategory($categoryName) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("INSERT INTO job_categories (category_name) VALUES (?)");
    $stmt->bind_param('s', $categoryName);
    if ($stmt->execute()) {
        sendJsonResponse(['success' => true, 'id' => $stmt->insert_id]);
    } else {
        sendJsonResponse(['error' => 'Failed to add job category'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

function updateJobCategory($id, $categoryName) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("UPDATE job_categories SET category_name = ? WHERE id = ?");
    $stmt->bind_param('si', $categoryName, $id);
    if ($stmt->execute()) {
        sendJsonResponse(['success' => true]);
    } else {
        sendJsonResponse(['error' => 'Failed to update job category'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

function deleteJobCategory($id) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("DELETE FROM job_categories WHERE id = ?");
    $stmt->bind_param('i', $id);
    if ($stmt->execute()) {
        sendJsonResponse(['success' => true]);
    } else {
        sendJsonResponse(['error' => 'Failed to delete job category'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

function listJobSkillsets() {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $result = $mysqli->query("SELECT js.*, jc.category_name 
                              FROM job_skillsets js 
                              JOIN job_categories jc ON js.category_id = jc.id 
                              ORDER BY js.skillset_name ASC");

    if ($result->num_rows > 0) {
        $jobSkillsets = [];
        while ($row = $result->fetch_assoc()) {
            $jobSkillsets[] = $row;
        }
        sendJsonResponse($jobSkillsets);
    } else {
        sendJsonResponse(['error' => 'No job skillsets found'], 404);
    }

    $mysqli->close();
}

function addJobSkillset($categoryId, $skillsetName) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("INSERT INTO job_skillsets (category_id, skillset_name) VALUES (?, ?)");
    $stmt->bind_param('is', $categoryId, $skillsetName);
    if ($stmt->execute()) {
        sendJsonResponse(['success' => true, 'id' => $stmt->insert_id]);
    } else {
        sendJsonResponse(['error' => 'Failed to add job skillset'], 500);
    }

    $stmt->close();
    $mysqli->close();
}


function updateJobSkillset($id, $categoryId, $skillsetName) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("UPDATE job_skillsets SET category_id = ?, skillset_name = ? WHERE id = ?");
    $stmt->bind_param('isi', $categoryId, $skillsetName, $id);
    if ($stmt->execute()) {
        sendJsonResponse(['success' => true]);
    } else {
        sendJsonResponse(['error' => 'Failed to update job skillset'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

function deleteJobSkillset($id) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("DELETE FROM job_skillsets WHERE id = ?");
    $stmt->bind_param('i', $id);
    if ($stmt->execute()) {
        sendJsonResponse(['success' => true]);
    } else {
        sendJsonResponse(['error' => 'Failed to delete job skillset'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

// New function to fetch and combine categories and skillsets
function listJobCategoriesAndSkillsets() {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    // Fetch categories
    $categoriesResult = $mysqli->query("SELECT * FROM job_categories ORDER BY category_name ASC");
    $jobCategories = [];
    while ($row = $categoriesResult->fetch_assoc()) {
        $jobCategories[] = $row;
    }

    // Fetch skillsets
    $skillsetsResult = $mysqli->query("SELECT js.*, jc.category_name 
                                      FROM job_skillsets js 
                                      JOIN job_categories jc ON js.category_id = jc.id 
                                      ORDER BY js.skillset_name ASC");
    $jobSkillsets = [];
    while ($row = $skillsetsResult->fetch_assoc()) {
        $jobSkillsets[] = $row;
    }

    // Combine the results
    $result = [
        'categories' => $jobCategories,
        'skillsets' => $jobSkillsets
    ];

    sendJsonResponse($result);
    $mysqli->close();
}

//Function to manage the certifications
function listCertifications() {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $result = $mysqli->query("SELECT * FROM job_certifications ORDER BY certification ASC");

    if ($result->num_rows > 0) {
        $certifications = [];
        while ($row = $result->fetch_assoc()) {
            $certifications[] = $row;
        }
        sendJsonResponse($certifications);
    } else {
        sendJsonResponse(['error' => 'No certifications found'], 404);
    }

    $mysqli->close();
}

function addCertification($certification) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("INSERT INTO job_certifications (certification) VALUES (?)");
    $stmt->bind_param('s', $certification);
    if ($stmt->execute()) {
        sendJsonResponse(['success' => true, 'id' => $stmt->insert_id]);
    } else {
        sendJsonResponse(['error' => 'Failed to add certification'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

function updateCertification($id, $certification) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("UPDATE job_certifications SET certification = ? WHERE id = ?");
    $stmt->bind_param('si', $certification, $id);
    if ($stmt->execute()) {
        sendJsonResponse(['success' => true]);
    } else {
        sendJsonResponse(['error' => 'Failed to update certification'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

function deleteCertification($id) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("DELETE FROM job_certifications WHERE id = ?");
    $stmt->bind_param('i', $id);
    if ($stmt->execute()) {
        sendJsonResponse(['success' => true]);
    } else {
        sendJsonResponse(['error' => 'Failed to delete certification'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

function getReviewerName($email) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("SELECT id, name FROM users WHERE email = ?");
    $stmt->bind_param('s', $email);
    $stmt->execute();
    $stmt->bind_result($id, $name); // Bind both id and name
    $stmt->fetch();

    if ($name) {
        sendJsonResponse(['id' => $id, 'name' => $name]); // Send both id and name
    } else {
        sendJsonResponse(['error' => 'Reviewer not found'], 404);
    }

    $stmt->close();
    $mysqli->close();
}

// Function to set candidate skillset
function setCandidateSkillSet($candidate_id, $email, $category, $skillset, $rating, $reviewer_id, $reviewer_email, $comment, $timestamp) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("INSERT INTO candidate_skillsets (candidate_id, email, category, skillset, rating, reviewer_id, reviewer_email, comment, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)");
    $stmt->bind_param('isssissss', $candidate_id, $email, $category, $skillset, $rating, $reviewer_id, $reviewer_email, $comment, $timestamp);
    
    if ($stmt->execute()) {
        sendJsonResponse(['success' => true]);
    } else {
        sendJsonResponse(['error' => 'Failed to set candidate skillset'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

// Function to get candidate skillset based on reviewer_email and candidate_email
function getCandidateSkillset($reviewer_email, $candidate_email) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("SELECT id, category, skillset, rating FROM candidate_skillsets WHERE reviewer_email = ? AND email = ? ORDER BY skillset");
    $stmt->bind_param('ss', $reviewer_email, $candidate_email);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $skillsets = [];
        while ($row = $result->fetch_assoc()) {
            $skillsets[] = $row;
        }
        sendJsonResponse($skillsets);
    } else {
        sendJsonResponse(['error' => 'No skillsets found for the specified reviewer and candidate'], 404);
    }

    $stmt->close();
    $mysqli->close();
}

// Function to delete a candidate skillset by ID
function deleteCandidateSkillset($id) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("DELETE FROM candidate_skillsets WHERE id = ?");
    $stmt->bind_param('i', $id);

    if ($stmt->execute()) {
        sendJsonResponse(['success' => true]);
    } else {
        sendJsonResponse(['error' => 'Failed to delete candidate skillset'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

// Function to get skillsets by category ID
function getSkillsetCategory($id) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("SELECT skillset_name FROM job_skillsets WHERE category_id = ?");
    $stmt->bind_param('i', $id);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $skillsets = [];
        while ($row = $result->fetch_assoc()) {
            $skillsets[] = $row;
        }
        sendJsonResponse($skillsets);
    } else {
        sendJsonResponse(['error' => 'No skillsets found for the specified category ID'], 404);
    }

    $stmt->close();
    $mysqli->close();
}
function createInterview($email, $process, $salary_expectation, $availability, $interview, $interviewer_name, $interviewer_email, $evaluation_field, $rating, $observations, $approved, $review_date) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);
    
    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("INSERT INTO candidate_review (email, process, salary_expectation, availability, interview, interviewer_name, interviewer_email, evaluation_field, rating, observations, approved, review_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)");
    $stmt->bind_param('sissssssisss', $email, $process, $salary_expectation, $availability, $interview, $interviewer_name, $interviewer_email, $evaluation_field, $rating, $observations, $approved, $review_date);
    
    if ($stmt->execute()) {
        sendJsonResponse(['success' => true]);
    } else {
        sendJsonResponse(['error' => 'Failed to create interview'], 500);
    }

    $stmt->close();
    $mysqli->close();
}
function getInterviews($interviewer_email, $candidate_email) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("SELECT * FROM candidate_review WHERE interviewer_email = ? AND email = ?");
    $stmt->bind_param('ss', $interviewer_email, $candidate_email);
    $stmt->execute();
    $result = $stmt->get_result();
    $interviews = [];

    while ($row = $result->fetch_assoc()) {
        $interviews[] = $row;
    }

    sendJsonResponse($interviews);
    
    $stmt->close();
    $mysqli->close();
}
function updateInterview($id, $email, $process, $salary_expectation, $availability, $interview, $interviewer_name, $interviewer_email, $evaluation_field, $rating, $observations, $approved, $review_date) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);
    
    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("UPDATE candidate_review SET email=?, process=?, salary_expectation=?, availability=?, interview=?, interviewer_name=?, interviewer_email=?, evaluation_field=?, rating=?, observations=?, approved=?, review_date=? WHERE id=?");
    $stmt->bind_param('sissssssisssi', $email, $process, $salary_expectation, $availability, $interview, $interviewer_name, $interviewer_email, $evaluation_field, $rating, $observations, $approved, $review_date, $id);
    
    if ($stmt->execute()) {
        sendJsonResponse(['success' => true]);
    } else {
        sendJsonResponse(['error' => 'Failed to update interview'], 500);
    }

    $stmt->close();
    $mysqli->close();
}
function deleteInterview($id) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);
    
    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("DELETE FROM candidate_review WHERE id = ?");
    $stmt->bind_param('i', $id);
    
    if ($stmt->execute()) {
        sendJsonResponse(['success' => true]);
    } else {
        sendJsonResponse(['error' => 'Failed to delete interview'], 500);
    }

    $stmt->close();
    $mysqli->close();
}


// Handler function to add a user
function addSystemUser($google_id, $name, $email, $profile_image, $admin) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("INSERT INTO users (google_id, name, email, profile_image, admin) VALUES (?, ?, ?, ?, ?)");
    $stmt->bind_param('ssssi', $google_id, $name, $email, $profile_image, $admin);

    if ($stmt->execute()) {
        sendJsonResponse(['success' => true, 'id' => $stmt->insert_id]);
    } else {
        sendJsonResponse(['error' => 'Failed to add user'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

// Handler function to update a user
function updateSystemUser($id, $google_id, $name, $email, $profile_image, $admin) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("UPDATE users SET google_id = ?, name = ?, email = ?, profile_image = ?, admin = ? WHERE id = ?");
    $stmt->bind_param('ssssii', $google_id, $name, $email, $profile_image, $admin, $id);

    if ($stmt->execute()) {
        sendJsonResponse(['success' => true]);
    } else {
        sendJsonResponse(['error' => 'Failed to update user'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

// Handler function to delete a user
function deleteSystemUser($id) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("DELETE FROM users WHERE id = ?");
    $stmt->bind_param('i', $id);

    if ($stmt->execute()) {
        sendJsonResponse(['success' => true]);
    } else {
        sendJsonResponse(['error' => 'Failed to delete user'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

// Handler function to list all users
function listSystemUsers() {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $result = $mysqli->query("SELECT * FROM users");

    if ($result->num_rows > 0) {
        $users = [];
        while ($row = $result->fetch_assoc()) {
            $users[] = $row;
        }
        sendJsonResponse($users);
    } else {
        sendJsonResponse(['error' => 'No users found'], 404);
    }

    $mysqli->close();
}

// Functions to handle the Employees Table
function listEmployees() {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $result = $mysqli->query("SELECT * FROM employee_profiles ORDER BY fullName ASC");

    if ($result->num_rows > 0) {
        $employees = [];
        while ($row = $result->fetch_assoc()) {
            $employees[] = $row;
        }
        sendJsonResponse($employees);
    } else {
        sendJsonResponse(['error' => 'No employees found'], 404);
    }

    $mysqli->close();
}

function addEmployee($primaryEmail, $recoveryEmail, $fullName, $phone_mobile, $thumbnailPhotoURL, $companyRole, $contractType, $suspended, $creationDate) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("INSERT INTO employee_profiles (primaryEmail, recoveryEmail, fullName, phone_mobile, thumbnailPhotoURL, companyRole, contractType, suspended, creationDate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)");
    $stmt->bind_param('sssssssss', $primaryEmail, $recoveryEmail, $fullName, $phone_mobile, $thumbnailPhotoURL, $companyRole, $contractType, $suspended, $creationDate);
    
    if ($stmt->execute()) {
        sendJsonResponse(['success' => true, 'id' => $stmt->insert_id]);
    } else {
        sendJsonResponse(['error' => 'Failed to add employee'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

// Function to get employee details by email
function getEmployee($email) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("SELECT * FROM employee_profiles WHERE primaryEmail = ?");
    $stmt->bind_param('s', $email);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $employee = $result->fetch_assoc();
        sendJsonResponse($employee);
    } else {
        sendJsonResponse(['error' => 'Employee not found'], 404);
    }

    $stmt->close();
    $mysqli->close();
}

// Function to update employee details
function updateEmployee($id, $primaryEmail, $recoveryEmail, $fullName, $phone_mobile, $thumbnailPhotoURL, $companyRole, $contractType, $suspended, $creationDate) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("UPDATE employee_profiles SET primaryEmail = ?, recoveryEmail = ?, fullName = ?, phone_mobile = ?, thumbnailPhotoURL = ?, companyRole = ?, contractType = ?, suspended = ?, creationDate = ? WHERE ID = ?");
    $stmt->bind_param('sssssssssi', $primaryEmail, $recoveryEmail, $fullName, $phone_mobile, $thumbnailPhotoURL, $companyRole, $contractType, $suspended, $creationDate, $id);
    
    if ($stmt->execute()) {
        sendJsonResponse(['success' => true]);
    } else {
        sendJsonResponse(['error' => 'Failed to update employee'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

function deleteEmployee($id) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("DELETE FROM employee_profiles WHERE ID = ?");
    $stmt->bind_param('i', $id);
    
    if ($stmt->execute()) {
        sendJsonResponse(['success' => true]);
    } else {
        sendJsonResponse(['error' => 'Failed to delete employee'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

// Function to list all certifications for an employee based on email
function listEmployeeCertifications($email) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("SELECT * FROM employee_certifications WHERE email = ? ORDER BY certification ASC");
    $stmt->bind_param('s', $email);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $certifications = [];
        while ($row = $result->fetch_assoc()) {
            $certifications[] = $row;
        }
        sendJsonResponse($certifications);
    } else {
        sendJsonResponse(['error' => 'No certifications found for the specified email'], 404);
    }

    $stmt->close();
    $mysqli->close();
}

// Function to add a new certification
function addEmployeeCertification($email, $certification, $date) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("INSERT INTO employee_certifications (email, certification, date) VALUES (?, ?, ?)");
    $stmt->bind_param('sss', $email, $certification, $date);
    if ($stmt->execute()) {
        sendJsonResponse(['success' => true, 'id' => $stmt->insert_id]);
    } else {
        sendJsonResponse(['error' => 'Failed to add certification'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

// Function to delete a certification by ID
function deleteEmployeeCertification($id) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("DELETE FROM employee_certifications WHERE id = ?");
    $stmt->bind_param('i', $id);

    if ($stmt->execute()) {
        sendJsonResponse(['success' => true]);
    } else {
        sendJsonResponse(['error' => 'Failed to delete certification'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

// Function to list all skillsets for an employee based on email
function listEmployeeSkillsets($email) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("SELECT * FROM employee_skillsets WHERE email = ? ORDER BY category, skillset ASC");
    $stmt->bind_param('s', $email);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $skillsets = [];
        while ($row = $result->fetch_assoc()) {
            $skillsets[] = $row;
        }
        sendJsonResponse($skillsets);
    } else {
        sendJsonResponse(['error' => 'No skillsets found for the specified email'], 404);
    }

    $stmt->close();
    $mysqli->close();
}

// Function to add a new skillset
function addEmployeeSkillset($employee_id, $email, $category, $skillset, $rating, $reviewer_email, $date) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("INSERT INTO employee_skillsets (employee_id, email, category, skillset, rating, reviewer_email, date) VALUES (?, ?, ?, ?, ?, ?, ?)");
    $stmt->bind_param('isssiss', $employee_id, $email, $category, $skillset, $rating, $reviewer_email, $date);
    if ($stmt->execute()) {
        sendJsonResponse(['success' => true, 'id' => $stmt->insert_id]);
    } else {
        sendJsonResponse(['error' => 'Failed to add skillset'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

// Function to delete a skillset by ID
function deleteEmployeeSkillset($id) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("DELETE FROM employee_skillsets WHERE id = ?");
    $stmt->bind_param('i', $id);

    if ($stmt->execute()) {
        sendJsonResponse(['success' => true]);
    } else {
        sendJsonResponse(['error' => 'Failed to delete skillset'], 500);
    }

    $stmt->close();
    $mysqli->close();
}
// Function to list all reviews for an employee based on email
function listEmployeeReviews($email) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("SELECT * FROM employee_reviews WHERE email = ? ORDER BY evaluation_field ASC");
    $stmt->bind_param('s', $email);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $reviews = [];
        while ($row = $result->fetch_assoc()) {
            $reviews[] = $row;
        }
        sendJsonResponse($reviews);
    } else {
        sendJsonResponse(['error' => 'No reviews found for the specified email'], 404);
    }

    $stmt->close();
    $mysqli->close();
}

// Function to list all public reviews for an employee based on email
function listPublicEmployeeReviews($email) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("SELECT * FROM employee_reviews WHERE email = ? AND public = 'YES' ORDER BY evaluation_field ASC");
    $stmt->bind_param('s', $email);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $reviews = [];
        while ($row = $result->fetch_assoc()) {
            $reviews[] = $row;
        }
        sendJsonResponse($reviews);
    } else {
        sendJsonResponse(['error' => 'No public reviews found for the specified email'], 404);
    }

    $stmt->close();
    $mysqli->close();
}

// Function to list all reviews
function listAllReviews() {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $result = $mysqli->query("SELECT * FROM employee_reviews ORDER BY evaluation_field ASC");

    if ($result->num_rows > 0) {
        $reviews = [];
        while ($row = $result->fetch_assoc()) {
            $reviews[] = $row;
        }
        sendJsonResponse($reviews);
    } else {
        sendJsonResponse(['error' => 'No reviews found'], 404);
    }

    $mysqli->close();
}
// Function to add a new review
function addEmployeeReview($employee_id, $email, $evaluation_field, $rating, $reviewer_email, $observations, $date, $public) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("INSERT INTO employee_reviews (employee_id, email, evaluation_field, rating, reviewer_email, observations, date, public) VALUES (?, ?, ?, ?, ?, ?, ?, ?)");
    $stmt->bind_param('ississss', $employee_id, $email, $evaluation_field, $rating, $reviewer_email, $observations, $date, $public);
    if ($stmt->execute()) {
        sendJsonResponse(['success' => true, 'id' => $stmt->insert_id]);
    } else {
        sendJsonResponse(['error' => 'Failed to add review'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

// Function to delete a review by ID
function deleteEmployeeReview($id) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("DELETE FROM employee_reviews WHERE id = ?");
    $stmt->bind_param('i', $id);

    if ($stmt->execute()) {
        sendJsonResponse(['success' => true]);
    } else {
        sendJsonResponse(['error' => 'Failed to delete review'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

// Function to update a review by ID
function updateEmployeeReview($id, $employee_id, $email, $evaluation_field, $rating, $reviewer_email, $observations, $date, $public) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("UPDATE employee_reviews SET employee_id = ?, email = ?, evaluation_field = ?, rating = ?, reviewer_email = ?, observations = ?, date = ?, public = ? WHERE id = ?");
    $stmt->bind_param('ississssi', $employee_id, $email, $evaluation_field, $rating, $reviewer_email, $observations, $date, $public, $id);
    if ($stmt->execute()) {
        sendJsonResponse(['success' => true]);
    } else {
        sendJsonResponse(['error' => 'Failed to update review'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

// Function to add a new candidate certification
function addCandidateCertification($email, $certification) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("INSERT INTO candidate_certifications (email, certification) VALUES (?, ?)");
    $stmt->bind_param('ss', $email, $certification);
    if ($stmt->execute()) {
        sendJsonResponse(['success' => true]);
    } else {
        sendJsonResponse(['error' => 'Failed to add certification'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

// Function to delete a candidate certification
function deleteCandidateCertification($email, $certification) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("DELETE FROM candidate_certifications WHERE email = ? AND certification = ?");
    $stmt->bind_param('ss', $email, $certification);

    if ($stmt->execute()) {
        sendJsonResponse(['success' => true]);
    } else {
        sendJsonResponse(['error' => 'Failed to delete certification'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

// Function to add a new candidate review
function addCandidateReview($email, $process, $salary_expectation, $availability, $interview, $interviewer_name, $interviewer_email, $evaluation_field, $rating, $observations, $approved, $review_date) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("INSERT INTO candidate_review (email, process, salary_expectation, availability, interview, interviewer_name, interviewer_email, evaluation_field, rating, observations, approved, review_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)");
    $stmt->bind_param('ssisssssisss', $email, $process, $salary_expectation, $availability, $interview, $interviewer_name, $interviewer_email, $evaluation_field, $rating, $observations, $approved, $review_date);
    
    if ($stmt->execute()) {
        sendJsonResponse(['success' => true, 'id' => $stmt->insert_id]);
    } else {
        sendJsonResponse(['error' => 'Failed to add candidate review'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

// Function to remove a candidate review by ID and interviewer_email
function removeCandidateReview($id, $interviewer_email) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("DELETE FROM candidate_review WHERE id = ? AND interviewer_email = ?");
    $stmt->bind_param('is', $id, $interviewer_email);

    if ($stmt->execute()) {
        sendJsonResponse(['success' => true]);
    } else {
        sendJsonResponse(['error' => 'Failed to remove candidate review'], 500);
    }

    $stmt->close();
    $mysqli->close();
}


function getJobProcess() {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $result = $mysqli->query("SELECT id, job_title, enabled FROM job_postings");

    if ($result->num_rows > 0) {
        $jobPostings = [];
        while ($row = $result->fetch_assoc()) {
            $jobPostings[] = $row;
        }
        sendJsonResponse($jobPostings);
    } else {
        sendJsonResponse(['error' => 'No job postings found'], 404);
    }

    $mysqli->close();
}

function getCandidateSalaryExpectation($email) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("SELECT salary_expectation, availability FROM candidate_review WHERE email = ? AND interview = 'First Interview'");
    $stmt->bind_param('s', $email);

    if ($stmt->execute()) {
        $result = $stmt->get_result();
        if ($result->num_rows > 0) {
            $data = $result->fetch_assoc();
            sendJsonResponse($data);
        } else {
            sendJsonResponse(['error' => 'No data found'], 404);
        }
    } else {
        sendJsonResponse(['error' => 'Failed to retrieve data'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

// Function to list all admin roles
function listAdminRoles() {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $result = $mysqli->query("SELECT * FROM admin_roles ORDER BY functionName ASC");

    if ($result->num_rows > 0) {
        $adminRoles = [];
        while ($row = $result->fetch_assoc()) {
            $adminRoles[] = $row;
        }
        sendJsonResponse($adminRoles);
    } else {
        sendJsonResponse(['error' => 'No admin roles found'], 404);
    }

    $mysqli->close();
}

// Function to add a new admin role
function addAdminRole($functionName, $authrole) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("INSERT INTO admin_roles (functionName, authrole) VALUES (?, ?)");
    $stmt->bind_param('si', $functionName, $authrole);

    if ($stmt->execute()) {
        sendJsonResponse(['success' => true, 'id' => $stmt->insert_id]);
    } else {
        sendJsonResponse(['error' => 'Failed to add admin role'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

// Function to update an existing admin role
function updateAdminRole($id, $functionName, $authrole) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("UPDATE admin_roles SET functionName = ?, authrole = ? WHERE id = ?");
    $stmt->bind_param('sii', $functionName, $authrole, $id);

    if ($stmt->execute()) {
        sendJsonResponse(['success' => true]);
    } else {
        sendJsonResponse(['error' => 'Failed to update admin role'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

// Function to delete an admin role
function deleteAdminRole($id) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("DELETE FROM admin_roles WHERE id = ?");
    $stmt->bind_param('i', $id);

    if ($stmt->execute()) {
        sendJsonResponse(['success' => true]);
    } else {
        sendJsonResponse(['error' => 'Failed to delete admin role'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

// Function to get the authrole of a specific function by functionName
function getAdminRole($functionName) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("SELECT authrole FROM admin_roles WHERE functionName = ?");
    $stmt->bind_param('s', $functionName);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        sendJsonResponse(['authrole' => $row['authrole']]);
    } else {
        sendJsonResponse(['error' => 'Function not found'], 404);
    }

    $stmt->close();
    $mysqli->close();
}

function getOverallInfo() {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $result = [];
    $query = "SHOW TABLES";
    $tables = $mysqli->query($query);

    if ($tables->num_rows > 0) {
        while ($row = $tables->fetch_array()) {
            $tableName = $row[0];
            $countQuery = "SELECT COUNT(*) as row_count FROM $tableName";
            $countResult = $mysqli->query($countQuery);
            $countRow = $countResult->fetch_assoc();
            $result[] = [
                "table_name" => $tableName,
                "count" => $countRow['row_count']
            ];
        }
        sendJsonResponse($result);
    } else {
        sendJsonResponse(['error' => 'No tables found'], 404);
    }

    $mysqli->close();
}

// Function to list all employee certifications
function listAllEmployeeCertifications() {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $result = $mysqli->query("SELECT * FROM employee_certifications");

    if ($result->num_rows > 0) {
        $certifications = [];
        while ($row = $result->fetch_assoc()) {
            $certifications[] = $row;
        }
        sendJsonResponse($certifications);
    } else {
        sendJsonResponse(['error' => 'No employee certifications found'], 404);
    }

    $mysqli->close();
}

// Function to list all candidate certifications
function listAllCandidateCertifications() {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $result = $mysqli->query("SELECT * FROM candidate_certifications");

    if ($result->num_rows > 0) {
        $certifications = [];
        while ($row = $result->fetch_assoc()) {
            $certifications[] = $row;
        }
        sendJsonResponse($certifications);
    } else {
        sendJsonResponse(['error' => 'No candidate certifications found'], 404);
    }

    $mysqli->close();
}

// Function to list all employee skillsets
function listAllEmployeeSkillsets() {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $result = $mysqli->query("SELECT * FROM employee_skillsets");

    if ($result->num_rows > 0) {
        $skillsets = [];
        while ($row = $result->fetch_assoc()) {
            $skillsets[] = $row;
        }
        sendJsonResponse($skillsets);
    } else {
        sendJsonResponse(['error' => 'No employee skillsets found'], 404);
    }

    $mysqli->close();
}

// Function to list all candidate skillsets
function listAllCandidateSkillsets() {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $result = $mysqli->query("SELECT * FROM candidate_skillsets");

    if ($result->num_rows > 0) {
        $skillsets = [];
        while ($row = $result->fetch_assoc()) {
            $skillsets[] = $row;
        }
        sendJsonResponse($skillsets);
    } else {
        sendJsonResponse(['error' => 'No candidate skillsets found'], 404);
    }

    $mysqli->close();
}

function addFeedback($type, $description, $email, $screenshotUrl = null) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
        return;
    }

    // Ensure that all parameters are strings
    $type = is_array($type) ? implode(', ', $type) : (string)$type;
    $description = is_array($description) ? implode(', ', $description) : (string)$description;
    $email = is_array($email) ? implode(', ', $email) : (string)$email;
    $screenshotUrl = is_array($screenshotUrl) ? implode(', ', $screenshotUrl) : (string)$screenshotUrl;

    $stmt = $mysqli->prepare("INSERT INTO site_feedback (type, description, email, screenshotUrl, status, date_open) VALUES (?, ?, ?, ?, 'Open', NOW())");
    $stmt->bind_param('ssss', $type, $description, $email, $screenshotUrl);
    if ($stmt->execute()) {
        sendJsonResponse(['success' => true, 'id' => $stmt->insert_id]);
    } else {
        sendJsonResponse(['error' => 'Failed to add feedback'], 500);
    }

    $stmt->close();
    $mysqli->close();
}


function listFeedback() {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
        return;
    }

    $result = $mysqli->query("SELECT * FROM site_feedback ORDER BY date_open DESC");

    if ($result) {
        $feedbackList = $result->fetch_all(MYSQLI_ASSOC);
        sendJsonResponse(['success' => true, 'data' => $feedbackList]);
    } else {
        sendJsonResponse(['error' => 'Failed to retrieve feedback list'], 500);
    }

    $mysqli->close();
}
function deleteFeedback($id) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
        return;
    }

    $stmt = $mysqli->prepare("DELETE FROM site_feedback WHERE id = ?");
    $stmt->bind_param('i', $id);
    if ($stmt->execute()) {
        sendJsonResponse(['success' => true]);
    } else {
        sendJsonResponse(['error' => 'Failed to delete feedback'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

function updateFeedback($id, $type = null, $description = null, $email = null, $screenshotUrl = null, $status = null, $observations = null, $date_closed = null) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
        return;
    }

    $fields = [];
    $params = [];
    $types = '';

    if ($type !== null) {
        $fields[] = 'type = ?';
        $params[] = $type;
        $types .= 's';
    }
    if ($description !== null) {
        $fields[] = 'description = ?';
        $params[] = $description;
        $types .= 's';
    }
    if ($email !== null) {
        $fields[] = 'email = ?';
        $params[] = $email;
        $types .= 's';
    }
    if ($screenshotUrl !== null) {
        $fields[] = 'screenshotUrl = ?';
        $params[] = $screenshotUrl;
        $types .= 's';
    }
    if ($status !== null) {
        $fields[] = 'status = ?';
        $params[] = $status;
        $types .= 's';
    }
    if ($observations !== null) {
        $fields[] = 'observations = ?';
        $params[] = $observations;
        $types .= 's';
    }
    if ($date_closed !== null) {
        $fields[] = 'date_closed = ?';
        $params[] = $date_closed;
        $types .= 's';
    }

    if (empty($fields)) {
        sendJsonResponse(['error' => 'No fields to update'], 400);
        return;
    }

    $params[] = $id;
    $types .= 'i';

    $stmt = $mysqli->prepare("UPDATE site_feedback SET " . implode(', ', $fields) . " WHERE id = ?");
    $stmt->bind_param($types, ...$params);

    if ($stmt->execute()) {
        sendJsonResponse(['success' => true]);
    } else {
        sendJsonResponse(['error' => 'Failed to update feedback'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

// Function to add a new employee enrollment record
function addEmployeeEnrollment($email, $step, $value) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
        return;
    }

    $stmt = $mysqli->prepare("
        INSERT INTO employee_enrollment (email, step, value)
        VALUES (?, ?, ?)
    ");
    $stmt->bind_param('sii', $email, $step, $value);

    try {
        if ($stmt->execute()) {
            sendJsonResponse(['success' => 'Enrollment added successfully']);
        }
    } catch (mysqli_sql_exception $e) {
        if ($stmt->errno === 1062) { // Duplicate entry error code
            sendJsonResponse(['error' => 'Duplicate'], 409);
        } else {
            sendJsonResponse(['error' => 'Failed to add enrollment: ' . $stmt->error], 500);
        }
    }

    $stmt->close();
    $mysqli->close();
}

// Function to list employee enrollment records by email
function listEmployeeEnrollment($email) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("
        SELECT id, email, step, value, date
        FROM employee_enrollment
        WHERE email = ?
    ");
    $stmt->bind_param('s', $email);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $enrollments = [];
        while ($row = $result->fetch_assoc()) {
            $enrollments[] = $row;
        }
        sendJsonResponse($enrollments);
    } else {
        sendJsonResponse(['error' => 'No enrollments found for the specified email'], 404);
    }

    $stmt->close();
    $mysqli->close();
}

// Function to delete an employee enrollment record by ID
function deleteEmployeeEnrollment($id) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("
        DELETE FROM employee_enrollment
        WHERE id = ?
    ");
    $stmt->bind_param('i', $id);

    if ($stmt->execute()) {
        sendJsonResponse(['success' => 'Enrollment deleted successfully']);
    } else {
        sendJsonResponse(['error' => 'Failed to delete enrollment: ' . $stmt->error], 500);
    }

    $stmt->close();
    $mysqli->close();
}

// Function to get enrollment status as a percentage
function getEnrollmentStatus($email) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("
        SELECT SUM(value) as total_value
        FROM employee_enrollment
        WHERE email = ?
    ");
    $stmt->bind_param('s', $email);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($row = $result->fetch_assoc()) {
        $totalValue = $row['total_value'];
        $percentage = ($totalValue / 13) * 100;
        $percentage = round($percentage, 2); // Round to two decimal places
        sendJsonResponse(['percentage' => $percentage . '%']);
    } else {
        sendJsonResponse(['error' => 'No enrollments found for the specified email'], 404);
    }

    $stmt->close();
    $mysqli->close();
}

function addCandidate($name, $email, $phone_number, $location, $english_level, $profile_photo, $candidate_cv, $created_at, $enabled) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("INSERT INTO candidate_profiles (name, email, phone_number, location, english_level, profile_photo, candidate_cv, created_at, enabled) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)");
    $stmt->bind_param('ssssssssi', $name, $email, $phone_number, $location, $english_level, $profile_photo, $candidate_cv, $created_at, $enabled);
    
    if ($stmt->execute()) {
        sendJsonResponse(['success' => true, 'id' => $stmt->insert_id]);
    } else {
        sendJsonResponse(['error' => 'Failed to add candidate'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

function updateCandidate($id, $name, $email, $phone_number, $location, $english_level, $profile_photo, $candidate_cv, $enabled) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("UPDATE candidate_profiles SET name = ?, email = ?, phone_number = ?, location = ?, english_level = ?, profile_photo = ?, candidate_cv = ?, enabled = ? WHERE id = ?");
    $stmt->bind_param('sssssssii', $name, $email, $phone_number, $location, $english_level, $profile_photo, $candidate_cv, $enabled, $id);

    if ($stmt->execute()) {
        sendJsonResponse(['success' => true]);
    } else {
        sendJsonResponse(['error' => 'Failed to update candidate'], 500);
    }

    $stmt->close();
    $mysqli->close();
}

function deleteCandidate($id) {
    global $config;
    $mysqli = new mysqli($config['database']['host'], $config['database']['user'], $config['database']['pass'], $config['database']['db']);

    if ($mysqli->connect_error) {
        sendJsonResponse(['error' => 'Database connection failed: ' . $mysqli->connect_error], 500);
    }

    $stmt = $mysqli->prepare("DELETE FROM candidate_profiles WHERE id = ?");
    $stmt->bind_param('i', $id);

    if ($stmt->execute()) {
        sendJsonResponse(['success' => true]);
    } else {
        sendJsonResponse(['error' => 'Failed to delete candidate'], 500);
    }

    $stmt->close();
    $mysqli->close();
}
