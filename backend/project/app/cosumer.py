# pdf_reader/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TextHighlightConsumer(AsyncWebsocketConsumer):
    """
    This WebSocket consumer sends word-by-word highlighting data
    to the frontend during TTS playback.

    The frontend listens and highlights the matching word.

    It's identified by task_id (e.g., session ID).
    """
    async def connect(self):
        # Get task_id from URL (e.g., ws://.../highlight/abc123/)
        self.task_id = self.scope['url_route']['kwargs']['task_id']
        self.group_name = f'highlight_{self.task_id}'

        # Join group (multiple clients can listen to same task)
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
        print(f"[WebSocket] Connected: Task {self.task_id}")

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        print(f"[WebSocket] Disconnected: Task {self.task_id}")

    async def receive(self, text_data):
        # Optional: frontend can send play/pause
        data = json.loads(text_data)
        print(f"[WebSocket] Received: {data}")

    async def send_word(self, event):
        """
        Called by backend to send a word to highlight.
        Event contains: { "word": "hello", "page": 2, "time": 1.2 }
        """
        word = event['word']
        page = event.get('page', 1)
        time = event.get('time', 0)

        # Send to WebSocket
        await self.send(text_data=json.dumps({
            'word': word,
            'page': page,
            'time': time
        }))