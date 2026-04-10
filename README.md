## About the Project

PrepLP is a placement preparation platform designed to help students access structured study materials and resources in one place.

The platform aims to simplify preparation by organizing content, making it easy to find relevant materials, and improving learning efficiency.

It helps students save time, stay consistent, and prepare effectively for technical interviews and placements.


## Features
-  Access organized study materials
-  Easy navigation and search
-  Structured content for better learning
-  Simple and user-friendly interface

## Tech Stack
- Frontend: HTML, CSS, JavaScript  
- Backend: Django  
- Database: SQLite  
- Cloud: S3-compatible storage (Backblaze B2)

##  Future Improvements
- User authentication system
- AI-based recommendations
- Personalized dashboard
- File upload & sharing system
- Required RAG updations

## My Contributions
- Converted a static file upload script into a reusable function-based module
- Implemented dynamic file naming using UUID to prevent overwriting
- Replaced hardcoded content with flexible input-based upload functionality
- Added error handling to improve reliability of file uploads

## Improvements Made
Enhanced a basic S3 file upload script by implementing dynamic file handling, unique naming using UUID, and error handling for improved scalability and reliability.
- Before: Uploaded a static file (`boto3-test.txt`) with fixed content ("hello")
- After: Implemented dynamic file uploads with unique filenames using UUID

- Before: Hardcoded script with no reusability
- After: Created a reusable function (`upload_text_file`) for flexible usage

- Before: No error handling
- After: Added try-except for better reliability
