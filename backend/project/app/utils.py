# audiobook.py

import pdfplumber
from gtts import gTTS
import pygame
import os
import json
import time

# === CONFIGURATION ===
PDF_PATH = "book.pdf"           # Change this to your PDF file
OUTPUT_DIR = "output"
AUDIO_FILE = os.path.join(OUTPUT_DIR, "audiobook.mp3")
WORDS_DATA_FILE = os.path.join(OUTPUT_DIR, "words_data.json")
READING_SPEED_WPM = 140         # Words per minute (adjust as needed)

# Create output folder
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === STEP 1: Extract Text + Word Positions ===
def extract_words_with_position(pdf_path):
    print("📄 Extracting text and word positions from PDF...")
    all_words = []
    with pdfplumber.open(pdf_path) as pdf:
        current_time = 0.0
        seconds_per_word = 60 / READING_SPEED_WPM

        for page_num, page in enumerate(pdf.pages):
            print(f"   → Extracting page {page_num + 1}...")
            words = page.extract_words(extra_attrs=["text"])

            for word_info in words:
                text = word_info["text"].strip()
                if not text:  # Skip empty
                    continue

                word_obj = {
                    "text": text,
                    "page": page_num,
                    "x0": round(word_info["x0"], 2),
                    "top": round(word_info["top"], 2),
                    "x1": round(word_info["x1"], 2),
                    "bottom": round(word_info["bottom"], 2),
                    "width": round(word_info["x1"] - word_info["x0"], 2),
                    "height": round(word_info["bottom"] - word_info["top"], 2),
                    "start": round(current_time, 2)
                }
                all_words.append(word_obj)
                current_time += seconds_per_word  # Move time forward

    print(f"✅ Extracted {len(all_words)} words from {len(pdf.pages)} pages.")
    return all_words

# === STEP 2: Convert Full Text to Speech ===
def generate_audio(text, output_file, lang='en'):
    print("🔊 Generating audio with gTTS...")
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(output_file)
        print(f"✅ Audio saved: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error generating audio: {e}")
        return False

# === STEP 3: Play Audio with pygame ===
def play_audio(file_path):
    print("🎧 Playing audio...")
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    # Wait while playing
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    print("✅ Finished playing.")

# === STEP 4: Save Word Data to JSON ===
def save_word_data(words, output_file):
    print(f"💾 Saving word data to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(words, f, ensure_ascii=False, indent=2)
    print("✅ Word data saved! Use this in React later.")

# === MAIN PROGRAM ===
if __name__ == "__main__":
    # Step 1: Check if PDF exists
    if not os.path.exists(PDF_PATH):
        print(f"❌ PDF not found: {PDF_PATH}")
        print("Please place your PDF file here and update PDF_PATH.")
    else:
        # Step 2: Extract words with position and timing
        words_data = extract_words_with_position(PDF_PATH)

        if not words_
            print("❌ No text extracted. Is your PDF scanned?")
        else:
            # Step 3: Get full text for TTS
            full_text = " ".join([word["text"] for word in words_data])

            # Optional: Limit text for testing
            # full_text = " ".join(full_text.split()[:100])  # First 100 words

            # Step 4: Generate audio
            if generate_audio(full_text, AUDIO_FILE, lang='en'):
                # Step 5: Save word data (for React later)
                save_word_data(words_data, WORDS_DATA_FILE)

                # Step 6: Ask user if they want to play
                play_now = input("\n▶️ Play audio now? (y/n): ").strip().lower()
                if play_now == 'y':
                    play_audio(AUDIO_FILE)