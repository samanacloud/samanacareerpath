# Samana CareerPath (SCP)

**Version: 0.7 Beta**

Samana CareerPath (SCP) is a hybrid Applicant Tracking System (ATS) designed to streamline the hiring process and career development within an organization. It tracks skillsets, certifications, and reviews of both applicants and employees, helping to identify career roadmaps and simplify analysis for HR teams.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Roadmap](#roadmap)
- [Changelog](#changelog)
- [License](#license)

## Features

### General Features
- **Job Posting & Application Management**: Create job postings, manage applications, and track candidates through the recruitment process.
- **Employee Profile Management**: Maintain and update employee profiles, including skillsets, certifications, and performance reviews.
- **Skillset & Certification Tracking**: Track and manage skillsets and certifications for both employees and candidates.
- **Career Development**: Provide AI-driven recommendations for employee career development, including course suggestions and progress tracking.
- **File Uploads**: Support for uploading resumes (CVs) and profile photos directly to an AWS S3 bucket.

### New in Version 0.7 Beta
- **Slack Notifications**: Notifications sent to Slack channels for candidate registrations, job submissions, and employee onboarding events.
- **AWS S3 Integration**: Secure file uploads to AWS S3, with flexible policies for different file types.
- **API Enhancements**: Backend API improvements for Slack integration and AWS S3 file handling.
- **UI Improvements**: Minor fixes to the Employee Profile, Employee Onboarding, and Dashboard pages.

## Architecture

The project is built using a modern stack with Docker containers hosted on AWS EC2. Below is an overview of the architecture:

### Frontend
- **Framework**: Vue.js with PrimeVue and Sakai Vue template.
- **Authentication**: Google OAuth 2.0.
- **Styling**: Custom SCSS based on Sakai Vue theme.

### Backend
- **Language**: PHP.
- **API**: RESTful API using PHP for handling JSON requests.
- **Database**: MySQL for storing candidate and employee data.

### Infrastructure
- **Containers**: Docker containers for frontend, backend, and database services.
- **Hosting**: AWS EC2.
- **Reverse Proxy & SSL**: NginX as the reverse proxy with SSL offload.
- **File Storage**: AWS S3 for storing uploaded files (CVs, profile photos).

## Installation

### Prerequisites
- Docker installed on your machine.
- AWS account for S3 and EC2 services.
- Google account for OAuth 2.0.

### Installation Steps
1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-repo/samana-careerpath.git
   cd samana-careerpath

2.	**Set Up Environment Variables**
•	Create a .env file in the root directory with the following:
GOOGLE_CLIENT_ID=<your-google-client-id>
GOOGLE_CLIENT_SECRET=<your-google-client-secret>
GOOGLE_API_KEY=<your-google-api-key>
VITE_SITE_URL=<your-site-url>
AWS_ACCESS_KEY_ID=<your-aws-access-key-id>
AWS_SECRET_ACCESS_KEY=<your-aws-secret-access-key>
AWS_REGION=us-east-1

3.	**Build and Run Docker Containers**
docker-compose up --build -d


4.	**Access the Application**
- **Visit http://localhost:8080 or your deployed site URL.

## Roadmap

- **Deeper Integration with OpenAI**: Utilize AI for advanced career development recommendations and analysis.
- **Google Drive Integration**: Allow employees to store and manage documents directly from Google Drive.
- **Slack Integration**: Enhance messaging and notifications features.
- **Smart Reports**: Generate detailed reports on candidate and employee performance and career progression.

### Changelog

### Version 0.7 Beta

- **Slack Notifications**: Implemented notifications for key events.
- **AWS S3 Integration**: Integrated file storage and retrieval using AWS S3.
- **API Enhancements**: Improved backend API for Slack and AWS interactions.
- **UI Improvements**: Refined the UI for a better user experience.
- **Minor Fixes**: Corrected issues in Employee Profile, Employee Onboarding, and Dashboard.

## License

Samana CareerPath is licensed under the MIT License. See LICENSE for more information.