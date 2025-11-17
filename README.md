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

Usage

Open the frontend in your browser (usually at http://localhost:3000).

Navigate to a page with text content.

Click the Read Text button to start converting the text into speech.

The application will read the text page by page.

Optionally, click Start from Here at any part of the text to begin reading from that section.

Project Structure
├── backend/          # Django backend
│   ├── tts_app/      # Django app for Text-to-Speech
│   ├── manage.py
│   └── requirements.txt
├── frontend/         # React frontend
│   ├── src/
│   └── package.json
└── README.md

How It Works

The frontend sends text or selected text to the Django backend.

The backend uses gTTS to generate a speech file (MP3).

The frontend receives the audio file and plays it using a browser audio player.

Users can navigate pages, and the system continues reading the next page automatically or from a chosen point.

Dependencies

Django


gTTS

React

Node.js / npm

Future Improvements

Add support for multiple languages.

Pause, resume, and skip functionalities for audio playback.

Highlight text as it is being read.

Save audio files for offline playback.
