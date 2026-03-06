# Audio-to-Video Service (Backend)

An automated MVP that transforms raw audio into professional, "faceless" style videos.

## The Vision

Building a seamless pipeline to:

1. **Enhance:** Clean audio & remove filler words.
2. **Transcribe:** Convert speech to text, with [Groq AI](https://groq.com/) whisper model.
3. **Stitch:** Intelligently match audio with [Pexels](https://pexels.com) visuals.

## Tech Stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com)
- **Database/Auth:** [Supabase](https://supabase.com)
- **Language:** Python  3.12.9

## Status: #BuildInPublic

Currently in early development. Just finished the initial repository setup and environment configuration.
Any User can now upload file.
In the background:
    The file gets transcribed.
    The text is then stored in the Supabase database.
    We then use use this text to generate sentences, which are then used to search Pexels API for specific keywords.
    These iamges are then saved in a folder trailor for the specific project.
