Text-to-Speech Web Application

A web application that converts text into speech, allowing users to listen to content page by page. Users can start the speech journey from any point in the text, making it interactive and easy to follow.

This project uses gTTS for text-to-speech conversion, Django as the backend framework, and React for the frontend interface.

Features

Converts text from pages into audio using gTTS.

Reads content page by page, automatically or on user selection.

Users can click a button to start speech from a specific part of the text.

Interactive and user-friendly interface with React.

Seamless backend integration with Django.

Tech Stack

Backend: Django

Frontend: React

Text-to-Speech: gTTS (Google Text-to-Speech)

Audio Playback: Browser-based audio player

Installation

Clone the repository

git clone <your-repo-url>
cd <your-repo-folder>


Backend Setup (Django)

cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver


Frontend Setup (React)

cd frontend
npm install
npm start
