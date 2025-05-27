from flask import Flask, request, send_file
from elevenlabs.client import ElevenLabs
from io import BytesIO

app = Flask(__name__)

elevenlabs = ElevenLabs(api_key="sk_a6a556b179da933b9995bd93188ce4d3ecb729609cccf961")

@app.route("/generate-audio", methods=["POST"])
def generate_audio():
    data = request.get_json()
    text = data.get("text", "Hello world")
    file_name = data.get("file_name", "output_audio")

    audio = elevenlabs.text_to_speech.convert(
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    audio_buffer = BytesIO()
    for chunk in audio:
        audio_buffer.write(chunk)
    audio_buffer.seek(0)

    return send_file(
        audio_buffer,
        download_name=f"{file_name}.mp3",
        mimetype="audio/mpeg"
    )

