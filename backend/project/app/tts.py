from gtts import gTTS
import os
# install: pip install gTTS
from gtts import gTTS
import math

def generate_tts_gtts(text,
                      output_audio_file="output.mp3",
                      lang="en",
                      tld="com",
                      slow=False,
                      words_per_minute=150):
    """
    Generate speech with gTTS (no API key required).
    Returns: (output_audio_file, timing_data)

    Parameters:
      text (str): text to speak
      output_audio_file (str): path to save MP3
      lang (str): language (e.g. 'en')
      tld (str): top-level domain to choose a specific Google domain voice (common: "com", "co.uk", "com.au")
      slow (bool): if True, speak more slowly (gTTS param)
      words_per_minute (int/float): for naive timing estimate (default 150 wpm)
    """
    if not text:
        raise ValueError("text must be a non-empty string")

    # 1) request audio from gTTS (requires internet but no API key)
    tts = gTTS(text=text, lang=lang, tld=tld, slow=slow)
    tts.save(output_audio_file)

    # 2) naive timing estimate (same approach as your Google TTS version)
    words = text.split()
    # avoid zero division
    if len(words) == 0:
        return output_audio_file, []

    # Convert WPM to seconds per word
    sec_per_word = 60.0 / float(words_per_minute)  # e.g. 150 wpm -> 0.4s/word
    timing_data = []
    current_time = 0.0
    # Optionally round times to 2 decimals for use in UI / websockets
    for w in words:
        timing_data.append({"word": w, "time": round(current_time, 2)})
        current_time += sec_per_word

    return output_audio_file, timing_data

