from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests, base64, os
from dotenv import load_dotenv
import openai

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:5173",  # Frontend Vite dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TrackInput(BaseModel):
    track_url: str

def get_access_token():
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
   

    if not client_id or not client_secret:
        raise HTTPException(status_code=500, detail="Missing Spotify credentials")

    auth = f"{client_id}:{client_secret}"
    b64_auth = base64.b64encode(auth.encode()).decode()
    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    res = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    if res.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Spotify token error: {res.text}")

    token = res.json().get("access_token")
    if not token:
        raise HTTPException(status_code=500, detail="Failed to retrieve Spotify access token")

    return token

@app.post("/mood")
def analyze_mood(data: TrackInput):
    token = get_access_token()
    print("🔐 SPOTIFY TOKEN:", token)
    try:
        track_id = data.track_url.split("/")[-1].split("?")[0]
        if not track_id:
            raise ValueError
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Spotify track URL.")

    headers = {"Authorization": f"Bearer {token}"}
    track_res = requests.get(f"https://api.spotify.com/v1/tracks/{track_id}", headers=headers)
    features_res = requests.get(f"https://api.spotify.com/v1/audio-features/{track_id}", headers=headers)

    if track_res.status_code != 200 or features_res.status_code != 200:
       
        track_error = track_res.text if track_res.status_code != 200 else None
        features_error = features_res.text if features_res.status_code != 200 else None
        user_message = None
        try:
            if features_error:
                import json
                err_obj = json.loads(features_error)
                if isinstance(err_obj, dict) and "error" in err_obj and "status" in err_obj["error"]:
                    if err_obj["error"]["status"] == 403:
                        user_message = "Spotify API access forbidden (403). Check if the track is available in your region or if your credentials are correct."
        except Exception:
            pass

        raise HTTPException(
            status_code=403,
            detail={
                "track_error": track_error,
                "features_error": features_error,
                "user_message": user_message
            }
        )

    info = track_res.json()
    features = features_res.json()

    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = (
        f"The song '{info['name']}' by {info['artists'][0]['name']} has valence={features['valence']}, "
        f"energy={features['energy']}, danceability={features['danceability']}. "
        "Describe the listener's mood in 1 sentence."
    )

    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=60
        )
        mood_text = response.choices[0].text.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

    return {
        "name": info["name"],
        "artist": info["artists"][0]["name"],
        "valence": features["valence"],
        "energy": features["energy"],
        "tempo": features["tempo"],
        "danceability": features["danceability"],
        "mood": mood_text
    }


