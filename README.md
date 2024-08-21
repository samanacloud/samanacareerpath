# Samana CareerPath

Samana CareerPath is an ATS platform designed to help you track your employees, candidates, career progress, and performance details of your team. It offers a comprehensive solution for managing talent and optimizing career development within your organization.

## Features

- **Secure API**: Ensures secure communication between the frontend and backend.
- **Skillsets Evaluations**: Evaluate and track the skillsets of your employees and candidates.
- **Certificate Tracking**: Keep track of certifications acquired by employees.
- **Candidates and Employee Tracking**: Manage and monitor the details of candidates and employees.
- **Career Development Recommendations**: AI-driven recommendations for career development based on employee skillsets and certifications.
- **Performance Monitoring**: Track and evaluate employee performance.


## Samana Careerpath v0.8 Pre-Release

### Recent Updates

- Modified the authentication process to be processed in the backend and provide enhanced security.
- Removed exposed environmental variables identified during troubleshooting.
- Updated the Candidates module to edit candidate information.
- Added the Candidates Admin module to delete and disable candidates.
- Optimized backend functions to provide enhanced control.


### New in Version 0.7 Beta
- **Slack Notifications**: Notifications sent to Slack channels for candidate registrations, job submissions, and employee onboarding events.
- **AWS S3 Integration**: Secure file uploads to AWS S3, with flexible policies for different file types.
- **API Enhancements**: Backend API improvements for Slack integration and AWS S3 file handling.
- **UI Improvements**: Minor fixes to the Employee Profile, Employee Onboarding, and Dashboard pages.


## Version 0.56 Beta

### What's New
- **Feedback System:** Integrated feedback submission with screenshot upload in the top bar.
- **UI Improvements:** Adjusted layout and design elements for better user experience.
- **Bug Fixes:** Fixed issues related to session expiration and feedback submission.


## Technologies Used

### Frontend
- Node.js
- Vue.js
- OpenAI

### Backend
- PHP
- MySQL
- REST API
- NginX

## Installation

Follow these steps to set up the project locally:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/samanacloud/samanacareerpath.git
    cd samanacareerpath
    ```

2. **Set up environment variables**:
    Create a `.env` file in the root directory of the project and add the following environment variables:

    ```plaintext
    # Environment variables for scp.samana.cloud (SCP - Samana CareerPath)

    # API keys
    GOOGLE_CLIENT_ID=your-google-client-id
    GOOGLE_CLIENT_SECRET=your-google-client-secret
    GOOGLE_API_KEY=your-google-api-key

    # Database configuration
    MYSQL_ROOT_PASSWORD=your-mysql-root-password
    MYSQL_DATABASE=your-database-name
    MYSQL_USER=your-database-user
    MYSQL_PASSWORD=your-database-password
    MYSQL_HOSTNAME=db #do not change this value
    MYSQL_PORT=3306

    # Backend Configuration
    SITE_URL=scp.samana.cloud  #Define here the URL that will use the application
    PUBLIC_IP=your-public-ip  #UPDATE this IP once you have the real public IP
    BACKEND_PORT=8080
    BACKEND_PROTOCOL=http
    BACKEND_HOSTNAME=backend_php #not required for now
    FRONTEND_PORT=3000
    FRONTEND_PROTOCOL=http
    FRONTEND_HOSTNAME=frontend_node #not required for now

    # Node environment
    NODE_ENV=development
    NODE_PORT=3000
    NEXT_PUBLIC_BACKEND_URL=http://backend

    # Variables for AI 
    VITE_OPENAI_API_KEY=your-openai-api-key
    ```

3. **Run the project in Docker**:
    Ensure you have Docker installed on your system. Use the following command to build and run the Docker containers:

    ```sh
    docker-compose up --build
    ```

4. **Access the application**:
    Open your web browser and go to `http://localhost:3000` to access the frontend and `http://localhost:8080` for the backend.

## Usage

Once the project is set up and running, you can:

- **Manage Employees and Candidates**: Add, edit, and delete employee and candidate details.
- **Track Skillsets and Certifications**: Keep an up-to-date record of employee skillsets and certifications.
- **Evaluate Performance**: Use the platform to evaluate and monitor employee performance.
- **AI Recommendations**: Get AI-driven recommendations for career development based on skillsets and certifications.

## Environment Variables

The following environment variables are required for the project:

- `GOOGLE_CLIENT_ID`: Your Google client ID.
- `GOOGLE_CLIENT_SECRET`: Your Google client secret.
- `GOOGLE_API_KEY`: Your Google API key.
- `MYSQL_ROOT_PASSWORD`: The root password for MySQL.
- `MYSQL_DATABASE`: The name of the MySQL database.
- `MYSQL_USER`: The MySQL user.
- `MYSQL_PASSWORD`: The password for the MySQL user.
- `MYSQL_HOSTNAME`: The hostname for the MySQL database (should be set to `db`).
- `MYSQL_PORT`: The port for MySQL (default is 3306).
- `SITE_URL`: The URL that will be used for the application.
- `PUBLIC_IP`: The public IP address of the server.
- `BACKEND_PORT`: The port for the backend (default is 8080).
- `BACKEND_PROTOCOL`: The protocol for the backend (http or https).
- `FRONTEND_PORT`: The port for the frontend (default is 3000).
- `FRONTEND_PROTOCOL`: The protocol for the frontend (http or https).
- `NODE_ENV`: The environment for Node.js (development, production).
- `NODE_PORT`: The port for the Node.js server (default is 3000).
- `NEXT_PUBLIC_BACKEND_URL`: The backend URL for the frontend to communicate with.
- `VITE_OPENAI_API_KEY`: Your OpenAI API key.

## Contributing

We welcome contributions from the community. If you'd like to contribute, please follow these guidelines:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the MIT License.

## Authors

- **Juan Pablo Otalvaro** - *Architecture - Design and Build* - [juandiab](https://github.com/juandiab)

## Acknowledgments

- Thanks to all the contributors and maintainers of the open-source libraries and tools used in this project.

