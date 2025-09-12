// src/App.js
import React, { useState, useRef } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import axios from 'axios';

// Configure PDF.js worker (for rendering PDF)
pdfjs.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

function App() {
  const [file, setFile] = useState(null);
  const [numPages, setNumPages] = useState(null);
  const [highlightedWord, setHighlightedWord] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [isPlaying, setIsPlaying] = useState(false);
  const [text, setText] = useState([]); // Store extracted text per page
  const [audioUrl, setAudioUrl] = useState('');
  const audioRef = useRef(null);
  const wsRef = useRef(null); // Reference to WebSocket

  // Handle file input change
  const onFileChange = (e) => {
    setFile(e.target.files[0]);
    resetState();
  };

  // Reset all states before new upload
  const resetState = () => {
    setNumPages(null);
    setHighlightedWord('');
    setCurrentPage(1);
    setIsPlaying(false);
    setText([]);
    setAudioUrl('');
    if (wsRef.current) {
      wsRef.current.close();
    }
  };

  // Upload PDF and start reading
  const uploadPdf = async () => {
    if (!file) return alert("Please select a PDF first.");

    const formData = new FormData();
    formData.append('pdf', file);

    try {
      // 👉 Send to Django backend
      const res = await axios.post('http://localhost:8000/api/upload/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      const { task_id, audio_url, pages } = res.data;

      setAudioUrl(audio_url);
      setText(pages);
      setNumPages(pages.length);

      // ✅ Start audio and WebSocket
      startReading(task_id, audio_url);
    } catch (err) {
      console.error("Upload failed:", err);
      alert("Upload failed. Check if the Django server is running.");
    }
  };

  // Start audio + WebSocket connection
  const startReading = (task_id, audio_url) => {
    // 🔊 Play audio
    const audio = new Audio(audio_url);
    audioRef.current = audio;
    audio.play().catch(err => console.error("Audio play error:", err));
    setIsPlaying(true);

    // 🔁 Connect to Django WebSocket
    const ws = new WebSocket(`ws://localhost:8000/ws/highlight/${task_id}/`);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log('✅ WebSocket connected to Django');
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      // Update highlighted word and current page
      setHighlightedWord(data.word || '');
      if (data.page) setCurrentPage(data.page);
    };

    ws.onclose = () => {
      console.log('🔌 WebSocket disconnected');
      setIsPlaying(false);
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  };

  // Callback when PDF loads
  const onDocumentLoadSuccess = ({ numPages }) => {
    setNumPages(numPages);
  };

  return (
    <div className="min-h-screen p-6 max-w-5xl mx-auto transition-all duration-300">
      {/* Header */}
      <header className="text-center mb-8">
        <h1 className="text-4xl font-extrabold text-blue-600">📖 PDF Audio Reader</h1>
        <p className="text-gray-600 mt-2">Upload a PDF and listen as it reads aloud with live highlighting</p>
      </header>

      {/* Upload Section */}
      <section className="bg-white shadow-lg rounded-xl p-8 mb-8 border hover:shadow-xl transition-shadow">
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Choose a PDF file
        </label>
        <input
          type="file"
          accept="application/pdf"
          onChange={onFileChange}
          className="block w-full text-sm text-gray-500
                     file:mr-4 file:py-2 file:px-4
                     file:rounded-full file:border-0
                     file:text-sm file:font-semibold
                     file:bg-blue-50 file:text-blue-700
                     hover:file:bg-blue-100"
        />
        <button
          onClick={uploadPdf}
          disabled={!file || isPlaying}
          className={`mt-4 w-full py-3 px-6 rounded-xl font-semibold text-white
                     transition-all transform hover:scale-105 focus:outline-none
                     ${isPlaying 
                       ? 'bg-gray-400 cursor-not-allowed' 
                       : 'bg-blue-600 hover:bg-blue-700'}`}
        >
          {isPlaying ? '🎧 Reading...' : '📤 Upload & Read Aloud'}
        </button>
      </section>

      {/* Live Status Bar */}
      {isPlaying && (
        <section className="bg-green-50 border-l-4 border-green-400 text-green-700 p-4 rounded mb-8 flex justify-between items-center shadow-md">
          <div>
            <strong>Now reading:</strong> "{highlightedWord || '...'}"
          </div>
          <div>
            <strong>Page:</strong> {currentPage}
          </div>
        </section>
      )}

      {/* PDF Viewer */}
      {file && (
        <section className="mt-6">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">📄 PDF Preview</h2>
          <div className="border border-gray-200 rounded-lg overflow-hidden shadow-sm bg-white">
            <Document
              file={file}
              onLoadSuccess={onDocumentLoadSuccess}
              className="select-text"
            >
              {Array.from(new Array(numPages), (_, i) => (
                <Page
                  key={`page_${i + 1}`}
                  pageNumber={i + 1}
                  width={window.innerWidth > 768 ? 650 : window.innerWidth - 40}
                  renderTextLayer={true}
                  renderAnnotationLayer={false}
                  className="drop-shadow-sm"
                />
              ))}
            </Document>
          </div>
          <p className="text-center text-sm text-gray-500 mt-4">
            Page {currentPage} of {numPages}
          </p>
        </section>
      )}
    </div>
  );
}

export default App;