# # from fastapi import FastAPI, HTTPException
# # from fastapi.middleware.cors import CORSMiddleware
# # from pydantic import BaseModel
# # import requests, base64, os
# # from dotenv import load_dotenv
# # import openai

# # load_dotenv()

# # app = FastAPI()

# # origins = [
# #     "http://localhost:5173",  # Frontend Vite dev server
# # ]

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=origins,
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )


# # class TrackInput(BaseModel):
# #     track_url: str

# # def get_access_token():
# #     client_id = os.getenv("SPOTIPY_CLIENT_ID")
# #     client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
   

# #     if not client_id or not client_secret:
# #         raise HTTPException(status_code=500, detail="Missing Spotify credentials")

# #     auth = f"{client_id}:{client_secret}"
# #     b64_auth = base64.b64encode(auth.encode()).decode()
# #     headers = {
# #         "Authorization": f"Basic {b64_auth}",
# #         "Content-Type": "application/x-www-form-urlencoded"
# #     }
# #     data = {"grant_type": "client_credentials"}
# #     res = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
# #     if res.status_code != 200:
# #         raise HTTPException(status_code=500, detail=f"Spotify token error: {res.text}")

# #     token = res.json().get("access_token")
# #     if not token:
# #         raise HTTPException(status_code=500, detail="Failed to retrieve Spotify access token")

# #     return token

# # @app.post("/mood")
# # def analyze_mood(data: TrackInput):
# #     token = get_access_token()
# #     print("🔐 SPOTIFY TOKEN:", token)
# #     try:
# #         track_id = data.track_url.split("/")[-1].split("?")[0]
# #         if not track_id:
# #             raise ValueError
# #     except Exception:
# #         raise HTTPException(status_code=400, detail="Invalid Spotify track URL.")

# #     headers = {"Authorization": f"Bearer {token}"}
# #     track_res = requests.get(f"https://api.spotify.com/v1/tracks/{track_id}", headers=headers)
# #     features_res = requests.get(f"https://api.spotify.com/v1/audio-features/{track_id}", headers=headers)

# #     if track_res.status_code != 200 or features_res.status_code != 200:
       
# #         track_error = track_res.text if track_res.status_code != 200 else None
# #         features_error = features_res.text if features_res.status_code != 200 else None
# #         user_message = None
# #         try:
# #             if features_error:
# #                 import json
# #                 err_obj = json.loads(features_error)
# #                 if isinstance(err_obj, dict) and "error" in err_obj and "status" in err_obj["error"]:
# #                     if err_obj["error"]["status"] == 403:
# #                         user_message = "Spotify API access forbidden (403). Check if the track is available in your region or if your credentials are correct."
# #         except Exception:
# #             pass

# #         raise HTTPException(
# #             status_code=403,
# #             detail={
# #                 "track_error": track_error,
# #                 "features_error": features_error,
# #                 "user_message": user_message
# #             }
# #         )

# #     info = track_res.json()
# #     features = features_res.json()

# #     openai.api_key = os.getenv("OPENAI_API_KEY")
# #     prompt = (
# #         f"The song '{info['name']}' by {info['artists'][0]['name']} has valence={features['valence']}, "
# #         f"energy={features['energy']}, danceability={features['danceability']}. "
# #         "Describe the listener's mood in 1 sentence."
# #     )

# #     try:
# #         response = openai.Completion.create(
# #             model="text-davinci-003",
# #             prompt=prompt,
# #             max_tokens=60
# #         )
# #         mood_text = response.choices[0].text.strip()
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

# #     return {
# #         "name": info["name"],
# #         "artist": info["artists"][0]["name"],
# #         "valence": features["valence"],
# #         "energy": features["energy"],
# #         "tempo": features["tempo"],
# #         "danceability": features["danceability"],
# #         "mood": mood_text
# #     }


# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import requests, base64, os, json
# from dotenv import load_dotenv
# from openai import OpenAI

# load_dotenv()

# app = FastAPI()

# # ------------------ CORS ------------------
# origins = ["http://localhost:5173"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ------------------ Models ------------------
# class TrackInput(BaseModel):
#     track_url: str

# # ------------------ Spotify Token ------------------
# def get_access_token():
#     client_id = os.getenv("SPOTIPY_CLIENT_ID")
#     client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

#     if not client_id or not client_secret:
#         raise HTTPException(status_code=500, detail="Missing Spotify credentials")

#     auth = f"{client_id}:{client_secret}"
#     b64_auth = base64.b64encode(auth.encode()).decode()

#     headers = {
#         "Authorization": f"Basic {b64_auth}",
#         "Content-Type": "application/x-www-form-urlencoded"
#     }

#     data = {"grant_type": "client_credentials"}

#     res = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)

#     if res.status_code != 200:
#         raise HTTPException(status_code=500, detail=f"Spotify token error: {res.text}")

#     return res.json()["access_token"]

# # ------------------ Helpers ------------------
# def extract_track_id(track_url: str) -> str:
#     try:
#         if "spotify:track:" in track_url:
#             return track_url.split(":")[-1]
#         return track_url.split("/")[-1].split("?")[0]
#     except Exception:
#         raise HTTPException(status_code=400, detail="Invalid Spotify track URL")

# # ------------------ Main API ------------------
# @app.post("/mood")
# def analyze_mood(data: TrackInput):
#     token = get_access_token()
#     track_id = extract_track_id(data.track_url)
#     print("🎵 TRACK ID:", track_id)

#     headers = {"Authorization": f"Bearer {token}"}

#     track_res = requests.get(
#         f"https://api.spotify.com/v1/tracks/{track_id}",
#         headers=headers
#     )

#     if track_res.status_code != 200:
#         raise HTTPException(
#             status_code=track_res.status_code,
#             detail={"track_error": track_res.json()}
#         )

#     features_res = requests.get(
#         f"https://api.spotify.com/v1/audio-features/{track_id}",
#         headers=headers,
#         params={"market": "IN"}
#     )

#     # ---- Fallback if features blocked (403) ----
#     if features_res.status_code == 200:
#         features = features_res.json()
#     else:
#         features = {
#             "valence": 0.5,
#             "energy": 0.5,
#             "danceability": 0.5,
#             "tempo": 120
#         }

#     info = track_res.json()

#     # ------------------ OpenAI ------------------
#     client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#     print("🔑 OPENAI KEY:", os.getenv("OPENAI_API_KEY"))


#     prompt = (
#         f"The song '{info['name']}' by {info['artists'][0]['name']} "
#         f"has valence={features['valence']}, energy={features['energy']}, "
#         f"danceability={features['danceability']}. "
#         "Describe the listener's mood in one short sentence."
#     )
      

#     try:
#         response = client.responses.create(
#             model="gpt-3.5-turbo",
#             input=prompt
#         )
#         mood_text = response.output_text
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"OpenAI error: {str(e)}")

#     # ------------------ Response ------------------
#     return {
#         "name": info["name"],
#         "artist": info["artists"][0]["name"],
#         "valence": features["valence"],
#         "energy": features["energy"],
#         "danceability": features["danceability"],
#         "tempo": features["tempo"],
#         "mood": mood_text
#     }
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import base64
import os
import re
from dotenv import load_dotenv

# ------------------ LOAD ENV ------------------
load_dotenv()

# ------------------ APP ------------------
app = FastAPI()

# ------------------ CORS ------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ MODEL ------------------
class TrackInput(BaseModel):
    track_url: str

# ------------------ SPOTIFY TOKEN ------------------
def get_access_token():
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise HTTPException(status_code=500, detail="Missing Spotify credentials")

    auth = f"{client_id}:{client_secret}"
    encoded = base64.b64encode(auth.encode()).decode()

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={"grant_type": "client_credentials"},
    )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Spotify token error")

    return response.json()["access_token"]

# ------------------ TRACK ID EXTRACTOR ------------------
def extract_track_id(url: str) -> str:
    if url.startswith("spotify:track:"):
        return url.split(":")[-1]

    match = re.search(r"track/([A-Za-z0-9]{22})", url)
    if match:
        return match.group(1)

    raise HTTPException(status_code=400, detail="Invalid Spotify track URL")

# ------------------ MAIN API ------------------
@app.post("/mood")
def analyze_mood(data: TrackInput):
    token = get_access_token()
    track_id = extract_track_id(data.track_url)

    print("🎵 TRACK ID:", track_id)

    headers = {"Authorization": f"Bearer {token}"}

    # ---------- TRACK INFO ----------
    track_res = requests.get(
        f"https://api.spotify.com/v1/tracks/{track_id}",
        headers=headers,
        params={"market": "IN"},
    )

    if track_res.status_code != 200:
        raise HTTPException(
            status_code=track_res.status_code,
            detail={"track_error": track_res.json()},
        )

    info = track_res.json()

    # ---------- AUDIO FEATURES ----------
    features_res = requests.get(
        f"https://api.spotify.com/v1/audio-features/{track_id}",
        headers=headers,
        params={"market": "IN"},
    )

    if features_res.status_code == 200:
        features = features_res.json()
    else:
    # 🎯 Dynamic fallback using track metadata
     popularity = info.get("popularity", 50)   # 0–100
    duration_ms = info.get("duration_ms", 180000)  # song length

    # Tempo estimation (slow song ≠ fast song)
    if duration_ms > 240000:          # long songs → calm
        tempo = 70
    elif duration_ms < 150000:        # short songs → energetic
        tempo = 130
    else:
        tempo = 100

    # Energy & valence estimation
    energy = int(min(100, max(10, popularity)))
    valence = int(min(100, max(10, popularity * 0.8)))

    # Danceability heuristic
    if tempo > 120:
        danceability = 75
    elif tempo < 80:
        danceability = 35
    else:
        danceability = 55

    features = {
        "energy": energy,
        "valence": valence,
        "danceability": danceability,
        "tempo": tempo
    }


    # ---------- PROMPT ----------
    prompt = (
        f"The song '{info['name']}' by {info['artists'][0]['name']} "
        f"has valence={features['valence']}, energy={features['energy']}, "
        f"danceability={features['danceability']}. "
        "Describe the listener's mood in one short sentence."
    )

    # ---------- OPENAI WITH FALLBACK ----------
    try:
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60,
        )

        mood_text = response.choices[0].message["content"].strip()

    except Exception:
        # 🔁 NO OPENAI / NO QUOTA FALLBACK
        # ------------------ MOOD INSIGHT LOGIC ------------------
     energy = features["energy"]
     valence = features["valence"]

    if energy >= 70 and valence >= 70:
     mood_text = "The song feels energetic, happy, and uplifting."
    elif energy >= 50 and valence >= 50:
     mood_text = "The song feels positive, lively, and enjoyable."
    elif energy < 40 and valence < 40:
     mood_text = "The song feels calm, emotional, and slightly melancholic."
    elif energy < 40:
     mood_text = "The song feels relaxed and soothing."
    elif valence < 40:
     mood_text = "The song feels emotional and introspective."
    else:
     mood_text = "The song has a balanced and relaxed emotional tone."


    # ---------- RESPONSE ----------
    return {
        "name": info["name"],
        "artist": info["artists"][0]["name"],
        "valence": features["valence"],
        "energy": features["energy"],
        "danceability": features["danceability"],
        "tempo": features["tempo"],
        "mood": mood_text,
    }
