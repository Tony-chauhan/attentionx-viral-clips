# AttentionX 🎥⚡️ 
**Automated Content Repurposing Engine (AttentionX AI Hackathon)**

Transform boring 16:9 long-form videos into viral 9:16 shorts. AttentionX combines audio processing, NLP, and Computer Vision to find the most engaging moment in a video, dynamically crop it centering the speaker, and generate an AI hook.

## 🚀 Impact & Innovation
- **Audio-Semantic Peak Detection**: Uses `Librosa` combined with `Whisper` transcripts to find high-energy, emotionally profound moments.
- **Dynamic Face-Centered Cropping**: Uses `MediaPipe` Face Detection with an Exponential Moving Average (EMA) algorithm to smoothly pan and keep the subject perfectly in extreme 9:16 crops.
- **GenAI Hooks**: `Gemini 1.5 Flash` reads the peak's transcript to generate a click-optimized headline.

## 🔗 Links
- [LIVE DEMO APP (Streamlit)](#) <!-- Add Hosted Link -->
- [WATCH DEMO VIDEO (YouTube)](#) <!-- CRITICAL: Add link before 8pm -->

## ⚙️ Architecture & Tech Stack
- Frontend: `Streamlit`
- Video Processing: `MoviePy`
- CV/Tracking: `mediaPipe`
- Audio/Transcripts: `Librosa`, `Whisper (tiny)`
- LLM: `Google Gemini 1.5 Flash`

## 🛠️ Setup Instructions (Local Deployment)
1. Clone the repo:
   ```bash
   git clone <your-repo>
   cd attentionx
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your Gemini API key:
   * Windows: `set GEMINI_API_KEY="your-api-key"`
   * Mac/Linux: `export GEMINI_API_KEY="your-api-key"`

4. Run the Streamlit Application:
   ```bash
   streamlit run app.py
   ```

## 🎥 Sample Demo Execution
We have included a "Demo Mode" fallback in our app design because cloud platforms like Streamlit Community Edition do not provide GPUs, making MediaPipe/MoviePy generation too slow for a live 2-minute demo window. Toggle `Use Demo Mode` in the UI to instantly see our high-fidelity generated clips.

*Known Limitations: Real-world production would use Celery workers on AWS EC2 instances with GPU acceleration.*

## 👥 The Squad
- **Dharmender Chauhan** (Team Leader / Architecture & Cloud)
- **Rishita Sorout** (Backend ML Pipelines & API Integrations)
- **Heena Chauhan** (Frontend Vision & UI/UX Lead)
