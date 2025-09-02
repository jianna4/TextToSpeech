from PyPDF2 import PdfReader
from gtts import gTTS
import pygame
import os

PDF_PATH = r"F:\Program Files\projects\Reader\backend\WasteWise_Company_Profile.pdf"
reader= PdfReader(PDF_PATH)
number_of_pages = len(reader.pages)
print(f"Number of pages: {number_of_pages}")

for page in reader.pages:
    text = page.extract_text()
    print(text)
    tts = gTTS(text=text, lang='en')
    tts.save("page.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("page.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # wait for music to finish playing
        continue