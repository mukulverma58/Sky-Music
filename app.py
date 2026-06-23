import cv2
from deepface import DeepFace
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

# Load keys
load_dotenv()

# Connect to Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
))

# Emotion to music mapping
def get_songs(emotion):
    mood_map = {
        "happy":    "Boyfriend",
        "sad":      "Arz kiya hai",
        "angry":    "Aari aari",
        "neutral":  "Malang",
        "fear":     "Mahavatar Narsingh",
        "surprise": "Sher aaya sher",
        "disgust":  "Wu shang clan"
    }
    query = mood_map.get(emotion, "chill music")
    results = sp.search(q=query, limit=5)
    
    songs = []
    for track in results["tracks"]["items"]:
        songs.append({
            "name": track["name"],
            "artist": track["artists"][0]["name"],
            "url": track["external_urls"]["spotify"]
        })
    return songs

# Webcam + emotion detection
cap = cv2.VideoCapture(0)
frame_count = 0
current_emotion = "neutral"

print("Starting... Press Q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Analyze every 30th frame (for speed)
    if frame_count % 30 == 0:
        try:
            result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
            current_emotion = result[0]["dominant_emotion"]

            # Fetch songs for detected emotion
            songs = get_songs(current_emotion)
            print(f"\nEmotion: {current_emotion.upper()}")
            print("Recommended Songs:")
            for song in songs:
                print(f"  {song['name']} — {song['artist']}")
                print(f"  {song['url']}")

        except:
            pass

    # Show emotion on webcam
    cv2.putText(frame, current_emotion, (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Sky Music - Emotion Detector", frame)

    frame_count += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()