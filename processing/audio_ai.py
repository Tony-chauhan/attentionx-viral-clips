import librosa
import numpy as np
import whisper
import google.generativeai as genai
import os
import tempfile
import moviepy.editor as mp

def get_peak_window(audio_path, window_duration=15):
    """Finds the 15-second window with the highest RMS average energy."""
    try:
        y, sr = librosa.load(audio_path)
        rms = librosa.feature.rms(y=y)[0]
        frames_per_sec = len(rms) / (len(y) / sr)
        window_frames = int(window_duration * frames_per_sec)
        
        if len(rms) < window_frames:
            return 0.0, len(y)/sr # Video is shorter than window
            
        # Find the window with highest average energy
        window_energies = np.convolve(rms, np.ones(window_frames)/window_frames, mode='valid')
        peak_frame = np.argmax(window_energies)
        start_time = peak_frame / frames_per_sec
        return start_time, start_time + window_duration
    except Exception as e:
        print(f"Error in audio peak detection: {e}")
        return 0.0, window_duration

def generate_hook(text):
    """Generates a viral hook using Gemini 1.5 Flash."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "VIRAL AI HIGHLIGHT" # Fallback
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Create a short, catchy, 5-word viral TikTok/Reels hook headline based ONLY on this text. Do not use quotes or punctuation. Text: {text}"
        response = model.generate_content(prompt)
        if response.text:
            return response.text.strip().upper()
        return "MUST WATCH AI MOMENT"
    except Exception as e:
        print(f"Gemini error: {e}")
        return "CRAZY AI REBORN MOMENT"

def extract_and_analyze(video_path, window_duration=15):
    """
    1. Extracts audio from video.
    2. Finds peak window.
    3. Transcribes peak segment.
    4. Generates a hook from transcript.
    """
    # 1. Extract audio
    audio_path = tempfile.mktemp(suffix=".wav")
    try:
        video = mp.VideoFileClip(video_path)
        if video.audio is None:
            raise ValueError("No audio found in video")
        video.audio.write_audiofile(audio_path, logger=None)
    except Exception as e:
        print(f"Audio extraction error: {e}")
        return {"start_time": 0.0, "end_time": window_duration, "transcript": "", "hook": "VIRAL AI CLIP"}

    # 2. Get Peak
    start_time, end_time = get_peak_window(audio_path, window_duration)
    
    # Trim Audio for whisper to save time instead of full video transcription
    segment_path = tempfile.mktemp(suffix=".wav")
    try:
        y, sr = librosa.load(audio_path, offset=start_time, duration=end_time-start_time)
        import soundfile as sf
        sf.write(segment_path, y, sr)
    except Exception as e:
        print(f"Segment extraction error: {e}")
        segment_path = audio_path
        
    # 3. Transcribe
    try:
        model = whisper.load_model("tiny")
        result = model.transcribe(segment_path)
        transcript = result["text"]
    except Exception as e:
        print(f"Whisper error: {e}")
        transcript = ""
        
    # 4. Generate Hook
    hook = generate_hook(transcript)
    
    # Cleanup
    if os.path.exists(audio_path): os.remove(audio_path)
    if os.path.exists(segment_path): os.remove(segment_path)
    
    return {
        "start_time": start_time,
        "end_time": end_time,
        "transcript": transcript,
        "hook": hook
    }
