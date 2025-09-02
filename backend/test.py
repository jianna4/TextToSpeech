from PyPDF2 import PdfReader
from gtts import gTTS
import pygame
import os

print("🎉 All libraries imported successfully!")
# Step 1: Convert text to speech
tts = gTTS(text="Hello, this is a test!", lang='en')
tts.save("test.mp3")