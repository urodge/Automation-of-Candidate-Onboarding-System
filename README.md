# Automation-of-Candidate-Onboarding-System
This project automates the candidate onboarding process by extracting information from scanned forms (images or PDFs) and storing it in a database. It simplifies manual data entry, enhances efficiency, and provides a user-friendly interface to upload and manage candidate records.

# Features
Upload scanned forms (PDF or Image).
Extract text data using Optical Character Recognition (OCR).
Automatically map and store extracted data in a normalized database.
View and search candidate records by name or email.
User-friendly web interface.

# Technologies Used
Frontend: HTML, CSS, JavaScript
Backend: Flask (Python)
OCR: Tesseract OCR
Database: SQLite/MySQL
Others: OpenCV for image preprocessing

# System Architecture
Input: Scanned forms are uploaded via the web interface.
Processing:
OCR extracts text data.
AI model validates and preprocesses the data.
Storage: Data is stored in a normalized relational database.
Output: Records can be viewed and searched through the web interface.

# Setup Instructions
1. Prerequisites
Python 3.7 or higher
Pip package manager
2. Installation
Clone the repository:

git clone https://github.com/urodge/enzigma-onboarding-system.git
cd enzigma-onboarding-system
Install dependencies:

pip install -r requirements.txt
Set up the database:

Use the provided database.sql script to initialize the database.
Run the application:

python app.py
Access the application at:

arduino
Copy code
http://127.0.0.1:5000

# Usage
Upload Files:
Navigate to the homepage.
Upload scanned forms (supports multiple files).
View Records:
Search for candidates by name or email.
View extracted details from the database.

# Screenshots
Upload Interface: A screenshot of the file upload page.
Database View: A screenshot displaying stored candidate records.

# Testing
Tested with various formats (PDF, PNG, JPG).
Validated extracted data accuracy against original forms.




