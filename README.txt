Clean Mastered - Minimal Docker App
-----------------------------------
Endpoints:
  GET  /        -> "Docker OK" test
  POST /master  -> upload 'file' (wav/flac/mp3/aiff), returns mastered.wav

Quick Deploy (Render, using Dockerfile):
1) Push this folder to GitHub.
2) render.com -> New -> Web Service -> Use Dockerfile.
3) Deploy. Open the URL.

Test locally (if you have Docker):
docker build -t cleanmastered .
docker run -p 8080:8080 cleanmastered
