from gtts import gTTS
import os
from datetime import datetime

def text_to_speech(text, lang='ne', output_dir='static'):
    """
    Convert text to speech and save as MP3.

    Args:
        text (str): Text to convert.
        lang (str): Language code (default: 'ne' for Nepali).
        output_dir (str): Folder where the audio file will be saved.

    Returns:
        str: Path to the saved audio file.
    """
    os.makedirs(output_dir, exist_ok = True)

    # overwrite lai avoid garne ra filename generate garne
    filename = f"speech_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    output_path = os.path.join(output_dir, filename)

    # speech object banaune
    tts = gTTS(text=text, lang=lang)
    tts.save(output_path)

    return output_path