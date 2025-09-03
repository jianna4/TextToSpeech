from PyPDF2 import PdfReader
from gtts import gTTS
import pygame
import os

PDF_PATH = r"F:\Program Files\projects\Reader\backend\WasteWise_Company_Profile.pdf"
reader= PdfReader(PDF_PATH)
number_of_pages = len(reader.pages)
print(f"Number of pages: {number_of_pages}")

pygame.mixer.init()
for i, page in enumerate(reader.pages, start=1):

    text = page.extract_text()
    print(f"\n--- Reading page {i} ---")

    file_name=f"page_{i}.mp3"
    tts = gTTS(text=text, lang='en')
    tts.save(file_name)

   
    pygame.mixer.music.load(file_name)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # wait for music to finish playing
        continue