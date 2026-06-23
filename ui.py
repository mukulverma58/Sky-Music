import streamlit as st
import cv2
from deepface import DeepFace
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

load_dotenv()


emotion_emoji = {
    "happy": "😄",
    "sad": "😢",
    "angry": "😠",
    "neutral": "😐",
    "fear": "😨",
    "surprise": "😲",
    "disgust": "🤢"
}

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
))

def get_songs(emotion):
    mood_map = {
        "happy":    "happy upbeat pop",
        "sad":      "sad acoustic heartbreak",
        "angry":    "aggressive rock intense",
        "neutral":  "lofi chill study",
        "fear":     "calm ambient peaceful",
        "surprise": "energetic electronic dance",
        "disgust":  "chill indie vibes"
    }
    query = mood_map.get(emotion, "chill music")
    results = sp.search(q=query, limit=5)
    songs = []
    for track in results["tracks"]["items"]:
        songs.append({
            "name": track["name"],
            "artist": track["artists"][0]["name"],
            "url": track["external_urls"]["spotify"],
            "image": track["album"]["images"][0]["url"]
        })
    return songs


st.title("🎵 Sky Music")
st.subheader("Your mood. Your music.")

if st.button("📷 Detect My Mood & Get Songs"):
    try:
        with st.spinner("Reading your emotion..."):
            cap = cv2.VideoCapture(0)
            emotions_detected = []
            emotions_detected = []

            for i in range(10):
                ret, frame = cap.read()
                try:
                    result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
                    emotions_detected.append(result[0]["dominant_emotion"])
                except:
                    pass

            cap.release()

            # Pick the most common emotion
            from collections import Counter
            emotion = Counter(emotions_detected).most_common(1)[0][0]
            result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
            emotion = result[0]["dominant_emotion"]
            emoji = emotion_emoji.get(emotion, "😊")
            st.success(f"Detected Emotion: **{emotion.upper()}** {emoji}")

            songs = get_songs(emotion)
            st.subheader("🎶 Songs for you:")
            st.caption("Click any song to open in Spotify")

            for song in songs:
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image(song["image"], width=80)
                with col2:
                    st.markdown(f"**{song['name']}**")
                    st.markdown(f"{song['artist']}")
                    st.markdown(f"[▶ Play on Spotify]({song['url']})")
                st.divider()

    except Exception as e:
        st.error("Could not detect emotion. Please try again!")