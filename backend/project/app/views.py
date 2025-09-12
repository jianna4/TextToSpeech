from django.shortcuts import render

# Create your views here.
# pdf_reader/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
import uuid
from .tasks import process_pdf_and_tts
import threading

@csrf_exempt
def upload_pdf(request):
    """
    API Endpoint: POST /upload/
    - Accepts PDF file
    - Saves to media/
    - Starts background TTS + WebSocket task
    - Returns audio URL and task_id
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    if 'pdf' not in request.FILES:
        return JsonResponse({'error': 'No PDF uploaded'}, status=400)

    pdf_file = request.FILES['pdf']

    # Generate unique task ID
    task_id = str(uuid.uuid4())

    # Save PDF
    pdf_path = os.path.join(settings.MEDIA_ROOT, f'{task_id}.pdf')
    with open(pdf_path, 'wb') as f:
        for chunk in pdf_file.chunks():
            f.write(chunk)

    # Start background task
    # ⚠️ In production, use Celery instead of threading
    thread = threading.Thread(
        target=process_pdf_and_tts,
        args=(pdf_path, task_id, "en-US-Wavenet-D")  # You can pass voice later
    )
    thread.start()

    # Return response
    audio_url = f'/audio/{task_id}.mp3'
    ws_url = f'ws://localhost:8000/ws/highlight/{task_id}/'

    return JsonResponse({
        'task_id': task_id,
        'audio_url': audio_url,
        'websocket_url': ws_url,
        'status': 'processing'
    })