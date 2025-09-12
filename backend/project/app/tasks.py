import os
import time
from app.tts import generate_tts_gtts   # <- use your gTTS version
from app.utils import extract_text_from_pdf
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def process_pdf_and_tts(pdf_path, task_id, lang="en", tld="com", slow=False):
    """
    Background task:
    1. Extract text from PDF
    2. Generate TTS audio with gTTS
    3. Stream word timings & page numbers via WebSocket
    """
    channel_layer = get_channel_layer()
    group_name = f"highlight_{task_id}"

    # Step 1: Extract text by page
    pages = extract_text_from_pdf(pdf_path)
    full_text = "\n".join([p["text"] for p in pages])

    # Step 2: Build word → [pages] map (list of page numbers)
    page_map = {}  # word -> list of page numbers
    for page in pages:
        for word in page["text"].split():
            word = word.strip()
            if not word:
                continue
            if word not in page_map:
                page_map[word] = []
            page_map[word].append(page["page_number"])

    # Step 3: Generate TTS audio with gTTS
    audio_file = os.path.join("../audio", f"{task_id}.mp3")
    audio_path, timing_data = generate_tts_gtts(
        full_text,
        output_audio_file=audio_file,
        lang=lang,
        tld=tld,
        slow=slow,
    )

    # Step 4: Send each word via WebSocket
    for item in timing_data:
        word = item["word"]
        # get *all* pages for this word, or fallback [1]
        pages_for_word = page_map.get(word, [1])

        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send_word",   # maps to consumers.send_word()
                "word": word,
                "pages": pages_for_word,
                "time": item["time"],
            },
        )

        # Simulate playback delay
        time.sleep(0.01)  # in real case, use item["time"] differences
