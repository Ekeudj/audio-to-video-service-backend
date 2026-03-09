# 🎙️ AudioFlow: AI Faceless Video Engine (v0.1.0 Alpha)

**From Raw Audio to AI-Synced Video in Seconds.**

AudioFlow is an automated pipeline designed to solve the "procrastination loop." It takes your voice recordings, understands them, finds matching visuals, and stitches together a high-quality video—all while you stay focused on creating.

## The MVP Logic

Currently, the engine handles the heavy lifting "off-screen":

1. **Upload:** Fast API receives your audio (`.mp3`, `.wav`).
2. **Transcription:** Powered by **Groq AI (Whisper-Large-v3-Turbo)** for near-instant speech-to-text.
3. **Intelligence:** Uses **Llama 3.1** to extract the perfect keywords from your sentences.
4. **Visual Sourcing:** Automatically queries the **Pexels API** for high-quality, relevant images.
5. **Production:** **MoviePy** stitches the images and original audio into a final `.mp4`.

## 🛠️ Tech Stack

- **Backend:** [FastAPI](https://fastapi.tiangolo.com) (Asynchronous & Fast)
- **AI Models:** Groq (Whisper + Llama 3.1)
- **Database:** [Supabase](https://supabase.com) (SQLModel)
- **Media Engine:** MoviePy & Pexels API
- **Language:** Python 3.12.9

## 🚦 Status: #BuildInPublic

This project is a 6-year procrastination dream finally turned into code.

- [x] Background Task Pipeline
- [x] Database Schema & Persistence
- [x] Automated Image-to-Audio Sync
- [ ] Frontend Dashboard (Coming Soon)
- [ ] Supabase Auth Integration (Coming Soon)

##  How it Works

1. **POST `/upload`**: Send an audio file.
2. **Groq AI**: Transcribes the audio using Whisper-Large-v3.
3. **Llama 3.1**: Picks the best visual keywords from your sentences.
4. **Pexels API**: Grabs high-quality matching images.
5. **MoviePy**: Stitches everything into a synced `.mp4` video.


## 🚀 Getting Started (For Testers)

Want to try it out? Follow these steps:

### 1. Clone & Install

```bash
git clone https://github.com
cd audio-flow
pip install -r requirements.txt
