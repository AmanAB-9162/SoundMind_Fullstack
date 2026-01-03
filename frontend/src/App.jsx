import './index.css'

import React, { useState } from "react";

function App() {
  const [trackUrl, setTrackUrl] = useState("");
  const [mood, setMood] = useState(null);
  const [error, setError] = useState("");

  const handleSubmit = async () => {

    if (
    !trackUrl.includes("open.spotify.com/track") &&
    !trackUrl.startsWith("spotify:track:")
  ) {
    setError("Please paste a valid Spotify track link");
    return;
  }
    try {
      const res = await fetch("http://localhost:8000/mood", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ track_url: trackUrl }),
      });
      const data = await res.json();
      if (res.ok) {
        setMood(data);
        setError("");
      } else {
         console.error("Backend error:", data);
        setError(data.detail || "Error fetching mood");
      }
    } catch (err) {
       console.error("Fetch failed:", err);
      setError("Server error.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center gap-6 p-4">
      <h1 className="text-4xl font-bold text-center">🎧 SoundMind – Music-Based Mood Coach</h1>
      <input
        type="text"
        placeholder="Paste a Spotify track link"
        className="outline-cyan-500 px-4 py-2 text-white rounded w-full  max-w-lg"
        value={trackUrl}
        onChange={(e) => setTrackUrl(e.target.value)}
      />
      <button onClick={handleSubmit} className="bg-purple-600 px-6 py-2 rounded hover:bg-purple-800">
        Analyze Mood
      </button>
      {mood && (
        <div className="text-center">
          <h2 className="text-2xl font-semibold">Track: {mood.name} by {mood.artist}</h2>
          <p>🎵Song Name : {mood.name}</p>
          <p>💃Artist Name : {mood.artist}</p>
          <p>🎵 Energy: {mood.energy}</p>
          <p>💃 Danceability: {mood.danceability}</p>
          <p>🎚️ Valence: {mood.valence}</p>
          <p>🔁 Tempo: {mood.tempo}</p>
          <p>🧠 Mood Insight: {mood.mood}</p>
        </div>
      )}
      {error && (
        typeof error === "object" && error !== null ? (
          <div className="text-red-500">
            {error.track_error && <p>Track error: {typeof error.track_error === "string" ? error.track_error : JSON.stringify(error.track_error)}</p>}
            {error.features_error && (
              <p>
                Features error: {
                  typeof error.features_error === "string"
                    ? error.features_error
                    : error.features_error && error.features_error.error && error.features_error.error.status
                      ? `Spotify API status ${error.features_error.error.status}`
                      : JSON.stringify(error.features_error)
                }
              </p>
            )}
          </div>
        ) : (
          <p className="text-red-500">{error}</p>
        )
      )}
    </div>
  );
}

export default App;
