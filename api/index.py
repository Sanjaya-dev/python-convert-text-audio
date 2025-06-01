from flask import Flask, request, send_file, jsonify
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
from io import BytesIO
import zipfile
import os
import tempfile

app = Flask(__name__)
elevenlabs = ElevenLabs(api_key="sk_a6a556b179da933b9995bd93188ce4d3ecb729609cccf961")

@app.route("/generate-audio", methods=["POST"])
def generate_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    if not file.filename.endswith('.zip'):
        return jsonify({"error": "Only .zip files are supported"}), 400

    # Buat direktori sementara untuk mengekstrak ZIP
    with tempfile.TemporaryDirectory() as tempdir:
        zip_path = os.path.join(tempdir, 'input.zip')
        file.save(zip_path)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(tempdir)

        output_audios = []
        for root, dirs, files in os.walk(tempdir):
            for filename in files:
                if filename.endswith(".txt"):
                    txt_path = os.path.join(root, filename)
                    with open(txt_path, 'r', encoding='utf-8') as f:
                        text = f.read()

                    audio = elevenlabs.text_to_speech.convert(
                        text=text,
                        voice_id="XB0fDUnXU5powFXDhCwa",
                        model_id="eleven_multilingual_v2",
                        output_format="mp3_44100_128",
                        voice_settings=VoiceSettings(
                            stability=0.4,
                            similarity_boost=0,
                            use_speaker_boost=True,
                            speed=0.9
                        )
                    )

                    audio_buffer = BytesIO()
                    for chunk in audio:
                        audio_buffer.write(chunk)
                    audio_buffer.seek(0)
                    output_audios.append((filename.replace(".txt", ".mp3"), audio_buffer.read()))

        # Kemas semua audio ke dalam satu ZIP
        output_zip = BytesIO()
        with zipfile.ZipFile(output_zip, 'w') as zip_out:
            for audio_filename, audio_bytes in output_audios:
                zip_out.writestr(audio_filename, audio_bytes)
        output_zip.seek(0)

        return send_file(
            output_zip,
            download_name="converted_audio.zip",
            mimetype="application/zip"
        )
