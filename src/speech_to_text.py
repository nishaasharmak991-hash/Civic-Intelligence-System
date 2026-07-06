import tempfile
from google.genai import types

def transcribe_audio(client, audio_bytes):

    # ----------------------------------------
    # Save Audio Temporarily
    # ----------------------------------------

    with tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    ) as temp_audio:

        temp_audio.write(audio_bytes)

        audio_path = temp_audio.name

    # ----------------------------------------
    # Upload Audio
    # ----------------------------------------

    with open(audio_path, "rb") as f:
        audio_bytes = f.read()

    audio_part = types.Part.from_bytes(
        data=audio_bytes,
        mime_type="audio/wav"
    )

    # ----------------------------------------
    # Prompt
    # ----------------------------------------

    prompt = """
You are an expert speech recognition assistant.

Convert the uploaded audio into text.

Rules:

1. Return ONLY the spoken complaint.

2. Do NOT explain.

3. Do NOT summarize.

4. Preserve the original language.

5. Correct obvious speech recognition mistakes.

"""

    # ----------------------------------------
    # Gemini Response
    # ----------------------------------------

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            prompt,
            audio_part
        ]
    )

    return response.text.strip()
