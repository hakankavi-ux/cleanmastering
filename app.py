import os, tempfile, subprocess
from flask import Flask, request, send_file, abort

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 1024  # 1 GB
ALLOWED = {".wav", ".flac", ".mp3", ".aiff", ".aif"}

def ext_ok(filename):
    return any(filename.lower().endswith(e) for e in ALLOWED)

@app.get("/")
def home():
    return "Clean Mastered — Docker OK"

@app.post("/master")
def master():
    if "file" not in request.files:
        abort(400, "No file")
    f = request.files["file"]
    if not f.filename or not ext_ok(f.filename):
        abort(400, "Unsupported format")

    with tempfile.TemporaryDirectory() as td:
        inp = os.path.join(td, "in")
        out = os.path.join(td, "out.wav")
        f.save(inp)

        # Example: 96kHz 24/32-bit style processing + light limiter (demo)
        ffmpeg_cmd = [
            "ffmpeg", "-y", "-i", inp,
            "-af", "alimiter=limit=0.0dB:level=disabled,aresample=96000",
            "-ar", "96000", "-sample_fmt", "s32",
            out
        ]
        subprocess.run(ffmpeg_cmd, check=True)

        return send_file(out, as_attachment=True,
                         download_name="mastered.wav", mimetype="audio/wav")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
