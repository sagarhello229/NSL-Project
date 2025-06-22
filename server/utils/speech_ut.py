from gtts import gTTS
import os
from datetime import datetime
import uuid

def text_to_speech(text, lang='ne', output_dir='static'):
    """
    Convert text to speech and save as MP3.

    Args:
        text (str): Text to convert.
        lang (str): Language code (default: 'ne' for Nepali).
        output_dir (str): Folder where the audio file will be saved.

    Returns:
        str: Path to the saved audio file, or None if failed.
    """
    if not text.strip():
        print("Warning: Empty text provided for speech.")
        return None

    os.makedirs(output_dir, exist_ok=True)

    # Unique filename using timestamp + uuid
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = uuid.uuid4().hex[:6]
    filename = f"speech_{timestamp}_{unique_id}.mp3"
    output_path = os.path.join(output_dir, filename)

    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(output_path)
        return output_path
    except Exception as e:
        print(f"Error during speech synthesis: {e}")
        return None
