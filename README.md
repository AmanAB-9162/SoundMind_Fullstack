# SoundMind – Music-Based Mood Coach

A full-stack app that analyzes the mood of a Spotify track using the Spotify API and OpenAI.

---

## Features

- Paste a Spotify track link and get a mood analysis.
- Uses FastAPI for the backend and React for the frontend.
- Integrates with Spotify and OpenAI APIs.

---

## Setup

### 1. Clone the repository

```sh
git clone <your-repo-url>
cd soundmind_fullstack
```

### 2. Backend Setup

```sh
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

#### Create a `.env` file in the `backend` folder:

```
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
OPENAI_API_KEY=your_openai_api_key
```

#### Run the backend server

```sh
uvicorn main:app --reload
```

The backend will be available at [http://localhost:8000](http://localhost:8000).

---

### 3. Frontend Setup

```sh
cd ../frontend
npm install
npm run dev
```

The frontend will be available at [http://localhost:5173](http://localhost:5173).

---

## Usage

1. Start both backend and frontend servers.
2. Open the frontend in your browser.
3. Paste a Spotify track link and click "Analyze Mood".
4. View the mood analysis and track features.

---

## Troubleshooting

- **403 Forbidden from Spotify:**  
  - Check your Spotify credentials in `.env`.
  - Make sure the track is available in your region.
  - Try a different track.
  - Ensure your Spotify app is set to use the "Client Credentials" flow (no redirect URI needed).

- **400 Bad Request:**  
  - Make sure you are submitting a valid Spotify track URL.
  - The request body should be JSON: `{"track_url": "<spotify-track-url>"}`.

- **OpenAI errors:**  
  - Check your OpenAI API key in `.env`.
  - Ensure you have enough quota.
  - Make sure your OpenAI account is active and not rate-limited.

- **CORS errors:**  
  - Make sure both servers are running and CORS is enabled in the backend.
  - The frontend should use the correct backend URL (`http://localhost:8000/mood`).

- **Environment variables not loading:**  
  - Ensure your `.env` file is in the correct directory (`backend/`).
  - Restart the backend server after editing `.env`.

- **Frontend not connecting to backend:**  
  - Check that the backend is running on `http://localhost:8000`.
  - Make sure the fetch URL in your frontend matches the backend endpoint.

- **General debugging tips:**  
  - Check your browser console and backend terminal for error messages.
  - Use tools like Postman or curl to test your backend endpoints directly.
  - If you change dependencies, re-install with `pip install -r requirements.txt` or `npm install`.

---

## License

MIT
