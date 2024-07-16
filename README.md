Image Compressor Web Application

Developers
Leta Malimo - letaemiru@gmail.com
Feven Bayu - fevenbayu5@gmail.com

Overview
The Image Compressor Web Application is a user-friendly tool designed to compress images efficiently. It allows users to upload images, compress them to reduce file size, and download the compressed images in a ZIP file. The application features user authentication, including signup and login functionalities, and a profile page to manage user information.

Features
Image Compression: Upload images and compress them to reduce file size.
User Authentication: Secure signup, login, and logout functionalities.
User Profile: Manage user information and view profile details.
Responsive Design: User-friendly interface with responsive design for various devices.
Flash Messages: Informative alerts for user actions and errors.
Technologies Used
Backend: Flask
Frontend: HTML, CSS (Bootstrap), JavaScript
Authentication: Flask-Login
Image Processing: Pillow (PIL)
Database: In-memory user store for simplicity (can be extended to use a database)
Installation
Prerequisites
Python 3.x
Virtual environment (optional but recommended
)
Setup
Clone the repository:

sh
git clone https://github.com/your-username/image-compressor-webapp.git
cd image-compressor-webapp
Create and activate a virtual environment:

On Windows:

sh
python -m venv venv
venv\Scripts\activate
On macOS/Linux:

sh
python3 -m venv venv
source venv/bin/activate
Install dependencies:

sh
pip install -r requirements.txt
Running the Application
Navigate to the project directory (if not already there):

sh
cd path/to/your/project
Activate your virtual environment (if not already activated):

On Windows:

sh
Copy code
venv\Scripts\activate
On macOS/Linux:

sh
source venv/bin/activate
Run the Flask application:

sh
python app.py
Open your browser and go to http://127.0.0.1:5000 to access the application.

Deactivating the Virtual Environment
When you are done working, deactivate the virtual environment:

sh

deactivate

Project Structure

csharp
image-compressor-webapp/
│
├── app.py                  # Main application file
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
│
├── templates/              # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── profile.html
│   └── signup.html
│
└── static/                 # Static files (CSS, JS, images)
    ├── style.css
    └── script.js

Usage
Signup: Create a new account by navigating to the signup page and providing the required information.
Login: Access your account by logging in with your username and password.
Compress Images: Upload images, select the desired compression quality, and download the compressed images in a ZIP file.
View Profile: Navigate to the profile page to view and manage your user information.
