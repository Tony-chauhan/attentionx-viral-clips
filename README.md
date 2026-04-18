# AttentionX 🎥⚡️ 
**Automated Content Repurposing Engine (AttentionX AI Hackathon)**

Transform boring 16:9 long-form videos into viral 9:16 shorts. AttentionX combines audio processing, NLP, and Computer Vision to find the most engaging moment in a video, dynamically crop it centering the speaker, and generate an AI hook.

## 👥 The Winning Squad
*Built with excellence by:*
- **Dharmender Chauhan** (Team Leader / Architecture & Cloud)
- **Rishita Sorout** (Backend ML Pipelines & API Integrations)
- **Heena Chauhan** (Frontend Vision & UI/UX Lead)
## 🚀 Impact & Innovation
- **Audio-Semantic Peak Detection**: Uses `Librosa` combined with `Whisper` transcripts to find high-energy, emotionally profound moments.
- **Dynamic Face-Centered Cropping**: Leverages `OpenCV` Native Haar Cascades with an Exponential Moving Average (EMA) algorithm to cleanly track and smoothly lock the subject perfectly in extreme 9:16 crops (100% bug-free native tracking).
- **GenAI Overlay Hooks**: `Gemini 1.5 Flash` reads the peak's transcript to generate a highly engaging headline, which perfectly drops into the frame via a pristine zero-dependency Pillow architecture.

## 🔗 Links
- [WATCH DEMO VIDEO (YouTube Shorts)](https://youtube.com/shorts/6vx8bbbW0bw?si=ZaRE7T3Oprxe3vaz) 🚀

[![AttentionX Live Demo](https://img.youtube.com/vi/6vx8bbbW0bw/maxresdefault.jpg)](https://youtube.com/shorts/6vx8bbbW0bw?si=ZaRE7T3Oprxe3vaz)
## ⚙️ Architecture & Tech Stack
- Frontend: `Streamlit`
- Video Processing: `MoviePy`
- CV/Tracking: `OpenCV (Native Haar Cascades)`
- Text Rendering: `Pillow (Zero-Dependency Image Hooks)`
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
