# 🎓 RAG-Based AI Teaching Assistant

A **Retrieval-Augmented Generation (RAG)** based AI Teaching Assistant that allows students to ask natural language questions and receive **grounded, timestamp-accurate answers** directly from course lecture videos.

Instead of relying on generic AI knowledge, this system retrieves relevant video transcript chunks, injects them into a carefully constrained prompt, and generates answers that reference **exact videos and timestamps** — making learning faster, clearer, and more reliable.

---

## ✨ Key Features

- 🎥 **Video-first learning** – Answers are grounded in actual lecture videos  
- ⏱️ **Timestamp-accurate guidance** – Points students to the exact moment a concept is taught  
- 🔍 **Semantic search with embeddings** – Finds relevant content using vector similarity  
- 🧠 **RAG architecture** – Eliminates hallucinations by answering strictly from retrieved context  
- 🧩 **Modular pipeline** – Easy to adapt for any course or video dataset  
- 💻 **Flexible deployment** – Runs locally with lightweight models and supports cloud LLMs  

---

## 🏗️ Project Architecture

```
Videos
  ↓
Audio Extraction (ffmpeg)
  ↓
Speech-to-Text (Whisper)
  ↓
Chunked Transcripts (JSON)
  ↓
Embeddings (Vectorization)
  ↓
Vector Similarity Search
  ↓
Prompt Construction (RAG)
  ↓
LLM Answer with Video + Timestamp
```

---

## 📂 Project Structure

```
RAG-based-ai/
│
├── videos/                  # Raw course videos (not included due to size limits)
├── audios/                  # Extracted mp3 audio files
├── jsons/                   # Timestamped transcript chunks
│
├── video_to_mp3.py          # Converts videos → mp3 using ffmpeg
├── mp3_to_json.py           # Transcribes mp3 → JSON using Whisper
├── preprocess_json.py       # Generates embeddings & saves vector store
├── process_incoming.py      # Query → retrieval → prompt → LLM answer
│
├── embeddings.joblib        # Stored vector embeddings
├── prompt.txt               # Generated RAG prompt (for inspection)
├── response.txt             # Model response output
└── README.md                # Project documentation
```

---

## ⚙️ How It Works (Step-by-Step)

### 1️⃣ Convert Videos to Audio

All lecture videos are converted to `.mp3` format for transcription.

```bash
python video_to_mp3.py
```

Uses `ffmpeg` to extract audio while preserving video numbering and titles.

### 2️⃣ Transcribe Audio to Timestamped JSON

Each audio file is transcribed using OpenAI Whisper, producing timestamped subtitle chunks.

```bash
python mp3_to_json.py
```

Each chunk contains:
1. Video number
2. Video title
3. Start time
4. End time
5. Spoken text

### 3️⃣ Generate Embeddings (Vectorization)

All transcript chunks are converted into embeddings using Ollama's embedding API.

```bash
python preprocess_json.py
```

- Embeddings are saved as `embeddings.joblib`
- Enables fast semantic similarity search

### 4️⃣ Ask Questions (RAG Inference)

Students can ask questions in natural language.

```bash
python process_incoming.py
```

The system:
- Embeds the user question
- Retrieves top-K relevant transcript chunks
- Builds a strict RAG prompt
- Sends it to a lightweight LLM
- Returns a grounded answer with video number & timestamps

---

## 🧠 Prompt Design (Anti-Hallucination)

The model is explicitly restricted to answer only from retrieved transcript chunks.

If the answer is not present in the videos, the system responds:

> "I could not find this topic clearly explained in the provided videos."

This ensures trustworthy, course-aligned answers.

---

## 🖥️ Models Used

### 🎙️ Speech-to-Text
**Whisper (base)** – stable and CPU-friendly

### 🔍 Embeddings
**nomic-embed-text** (via Ollama)
- 768-dimensional embeddings
- Optimized for semantic search

### 🤖 Language Model
**qwen2.5:1.5b** – lightweight and local-friendly
- Easy to swap with cloud LLMs (OpenAI, Groq, etc.)

---

## ⚠️ Hardware Notes

Designed to work on low-resource systems. Local LLMs are intentionally lightweight.

For best performance:
- Use cloud LLM APIs for inference
- Keep embeddings and retrieval local

---

## 🧪 Example Query

**Question:**  
Where were semantic tags taught?

**Answer:**  
**Video 11:** Installing VS Code & How Websites Work  
**Timestamp:** 109.82 – 145.30 seconds  
**Explanation:** This section introduces semantic HTML tags, explains their purpose, and why they improve structure and accessibility.

---

## 🚀 Use Cases

- AI tutor for recorded courses
- Timestamp-based doubt resolution
- Self-paced learning assistant
- EdTech platforms
- Internal corporate training
- Lecture search & summarization

---

## 🔮 Future Improvements

- 🌐 Web UI (FastAPI + Frontend)
- 🔗 Clickable video timestamps
- 📊 Confidence scoring for answers
- 🧠 Personalized learning paths
- ☁️ Cloud GPU deployment
- 📚 Multi-course support

---

## 👤 Author

**Huzaif Ulla Khan**  
BE in Computer Science Engineering  
AI & Machine Learning Enthusiast

**Project:** RAG-Based AI Teaching Assistant
