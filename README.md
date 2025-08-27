📝 Flask Quiz Application

A full-featured Quiz Management System built with Flask and MySQL.
It provides separate dashboards for Students and Teachers, allowing teachers to create quizzes and students to attempt them in a secure environment.

✨ Features
👩‍🏫 Teacher Dashboard

Create new quizzes with unique quiz codes

Add multiple-choice questions with correct answers and marks

Manage quizzes (title, description, max questions)

Share quiz codes with students using quiz code

👨‍🎓 Student Dashboard

Register & Login securely

Enter quiz code to attempt a quiz

View available quizzes

Attempt quizzes with live marking

📊 Results & Analytics

Automatic calculation of scores

Store results in database (result_info)

Display quiz results with student performance

🛠️ Tech Stack

Backend: Flask (Python)

Database: MySQL

Frontend: HTML, CSS (dark & vintage themed UI)

⚙️ Installation

Clone the repository:

git clone https://github.com/yourusername/Flask-Quiz-App.git
cd Flask-Quiz-App


Create a virtual environment and install dependencies:

pip install -r requirements.txt


Setup MySQL database:

Create a database named quiz_database

Run the SQL scripts to create required tables (user_info, quiz_info, result_info, etc.)

Run the app:

python app.py


Open in browser:

http://127.0.0.1:5000/

📂 Project Structure
Flask-Quiz-App/
│── app.py                # Main Flask app
│── templates/            # HTML Templates (welcome, login, register, dashboards, quiz, etc.)
│── static/               # CSS, JS, and images
│── requirements.txt      # Dependencies
│── README.md             # Project description

🚀 Future Enhancements

Add quiz scheduling & timer

Export results to CSV/PDF

Graphical analytics for teachers

Enhanced security with password hashing

📌 Author: RAVINDRA VIDYASAGAR PANDEY
📌 License: MIT
