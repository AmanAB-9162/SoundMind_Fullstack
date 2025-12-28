# 🎧 SoundMind – Music-Based Mood Coach 

SoundMind is an AI-powered  mood analysis tool that uses **Spotify audio features** and **OpenAI** to predict your mood based on any track you paste. Built with **React (Vite)** frontend and **FastAPI** backend, it's fast, intuitive, and ready for extension.

---

## 🚀 Features

- 🔗 Paste any **Spotify track link**
- 🧠 Uses **OpenAI** to generate mood insights
- 📊 Reads Spotify's **valence**, **energy**, **tempo**, and **danceability**
- 🌐 CORS-enabled secure API communication
- 💡 Modern UI using **Tailwind CSS**

---

## 🛠️ Tech Stack

| Frontend | Backend |
|---------|---------|
| React (Vite) ⚛️ | FastAPI 🚀 |
| Tailwind CSS 🌈 | Python 🐍 |
| Fetch API 🔄 | Spotipy / Requests 🎵 |
|   –    | OpenAI API 🧠 |
|   –    | dotenv (.env) 🔐 |

---

## 📁 Project Structure

soundmind_fullstack/
├── backend/
│ ├── main.py
│ ├── .env
│ └── requirements.txt
├── frontend/
│ ├── index.html
│ ├── public/
│ │ └── soundmind-favicon.png
│ ├── src/
│ │ └── App.jsx
│ └── tailwind.config.js

---

## 🛠️ Setup Guide

### 1️⃣ Clone the Repo
git clone https://github.com/yourusername/soundmind_fullstack.git
cd soundmind_fullstack


###2️⃣ Backend (FastAPI)
cd backend
python -m venv venv
venv\Scripts\activate    # or source venv/bin/activate for Linux/Mac
pip install -r requirements.txt
Create .env file:

SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
OPENAI_API_KEY=your_openai_api_key


Run the backend:
uvicorn main:app --reload

This will start FastAPI at http://localhost:8000

###3️⃣ Frontend (React + Vite)
cd ../frontend
npm install
npm run dev
This will start the frontend at http://localhost:5173

📤 API Endpoint
POST /mood
Request Body:
Request Body:

json
{
  "track_url": "https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b"
}
Response Example:

json
{
  "name": "Blinding Lights",
  "artist": "The Weeknd",
  "valence": 0.95,
  "energy": 0.8,
  "tempo": 171.005,
  "danceability": 0.65,
  "mood": "The listener feels upbeat, energetic, and joyful."
}
🧪 Sample Spotify Track Links
https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b (Blinding Lights – The Weeknd)

https://open.spotify.com/track/4iJyoBOLtHqaGxP12qzhQI (Peaches – Justin Bieber)

https://open.spotify.com/track/75FEaRjZTKLhTrFGsfMUXR (Shivers – Ed Sheeran)

🌐 CORS Setup in FastAPI
python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
🎨 Add Favicon (Optional)
In frontend/index.html:
html
<link rel="icon" type="image/png" href="/soundmind-favicon.png" />
Put your favicon in frontend/public/

📦 Backend Dependencies (requirements.txt)
fastapi
uvicorn
python-dotenv
requests
openai


🛑 Common Errors
Error Message	Cause / Fix
403 Forbidden (Spotify)	Track not accessible / Invalid Client ID or Secret
400 Bad Request (Invalid URL)	Make sure Spotify track URL is complete and correct
CORS Policy Blocked	Ensure FastAPI allows http://localhost:5173 in allow_origins

🧠 Credits & Tools
Spotify Developer Portal


![image](https://github.com/user-attachments/assets/ee358500-79cc-41cb-aebf-a85b1b67a7ac)


FastAPI

React + Vite

Tailwind CSS

