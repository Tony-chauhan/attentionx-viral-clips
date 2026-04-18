import streamlit as st
import os
import time
import tempfile
import sys

# Optional: if you run into module load errors during development
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from processing.audio_ai import extract_and_analyze
from processing.video_ai import process_video

# ------------- Configuration ------------- #
st.set_page_config(
    page_title="AttentionX",
    page_icon="🎥",
    layout="wide"
)

# Custom CSS for UI/UX (Heena's design spec)
st.markdown("""
<style>
    .stApp { background-color: #0A0A0A; color: #FFFFFF; }
    h1 { color: #8A2BE2; font-family: sans-serif; font-weight: 800; }
    .stFileUploader { background-color: rgba(138, 43, 226, 0.05); border: 2px dashed #8A2BE2; border-radius: 10px; padding: 2em; }
    .stButton>button { background-color: #8A2BE2; color: white; border-radius: 5px; font-weight: bold; border: none; padding: 10px 20px;}
    .stButton>button:hover { background-color: #9B30FF; border: none; }
</style>
""", unsafe_allow_html=True)

# ------------- Hero ------------- #
st.title("AttentionX 🎥⚡️")
st.markdown("### Automated Content Repurposing Engine")
st.markdown("Upload a 16:9 long-form video. We'll automatically find the best moment, smart-crop to 9:16 keeping the speaker centered, and burn an AI viral hook!")

# ------------- Inputs ------------- #
demo_mode = st.checkbox("🚀 Use Demo Mode (Instant Processing / Safety Net)", value=False)
uploaded_file = st.file_uploader("Upload Long-Form Video (.mp4)", type=["mp4"])

# ------------- Processing Logic ------------- #
if uploaded_file is not None:
    if st.button("Generate Shorts 🚀"):
        if demo_mode:
            st.warning("Running in Demo Mode: Serving pre-processed sample data.")
            with st.spinner("🎧 Analyzing Audio..."):
                time.sleep(1)
            with st.spinner("🔍 Tracking Faces & MUXing..."):
                time.sleep(1)
            with st.spinner("✍️ Writing AI Hook..."):
                time.sleep(1)
                
            demo_video_path = os.path.join("sample_data", "output.mp4")
            
            # Use placeholder if it doesn't exist
            if not os.path.exists(demo_video_path):
                st.error("No sample data found. Please run a real file first and save the output in sample_data/output.mp4!")
            else:
                st.success("Analysis Complete!")
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.video(demo_video_path)
                with col2:
                    st.markdown("### 🎣 Viral AI Hook")
                    st.subheader("WAIT UNTIL THE END FOR THIS SECRETS")
                    st.markdown("### 📝 Subtitles Fragment")
                    st.write("...so anyway the key to success is actually taking action instead of just waiting...")
                        
                    with open(demo_video_path, "rb") as file:
                        btn = st.download_button(
                            label="Download 9:16 Short",
                            data=file,
                            file_name="attentionx_short.mp4",
                            mime="video/mp4"
                        )

        else:
            # REAL PROCESSING
            # Save uploaded clip to temp
            temp_in = tempfile.mktemp(suffix=".mp4")
            with open(temp_in, "wb") as f:
                f.write(uploaded_file.read())
                
            st.info("Starting AI Pipeline. This might take a minute on CPU.")
            
            with st.status("Pipeline Execution", expanded=True) as status:
                st.write("🎧 Extracting audio and running Librosa RMS...")
                try:
                    # Target 15 seconds window
                    results = extract_and_analyze(temp_in, window_duration=15)
                    st.write(f"✅ Found emotional peak. Start: {results['start_time']:.1f}s, End: {results['end_time']:.1f}s")
                    st.write(f"✅ Whisper Transcript Generated")
                    st.write(f"✍️ Gemini 1.5 Flash Hook: {results['hook']}")
                    
                    st.write("🔍 Running MediaPipe Face Tracking and Cropping (EMA Smoothed)...")
                    output_mp4 = process_video(
                        temp_in, 
                        results['start_time'], 
                        results['end_time'], 
                        results['hook'],
                        results['transcript']
                    )
                    st.write("✅ Video Muxed successfully.")
                    status.update(label="All processes completed!", state="complete", expanded=False)
                    
                    st.success("Generation Complete!")
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.video(output_mp4)
                    with col2:
                        st.markdown("### 🎣 Viral AI Hook")
                        st.subheader(results['hook'])
                        st.markdown("### 📝 Transcript Fragment")
                        st.write(f'"{results["transcript"]}"')
                        
                        with open(output_mp4, "rb") as file:
                            btn = st.download_button(
                                label="Download 9:16 Short",
                                data=file,
                                file_name="attentionx_short.mp4",
                                mime="video/mp4"
                            )
                            
                except Exception as e:
                    status.update(label=f"Failed: {e}", state="error", expanded=True)
                    st.error(f"Pipeline crashed. Try Demo Mode if running out of time. \nError: {str(e)}")
                    
            if os.path.exists(temp_in):
                os.remove(temp_in)
else:
    st.info("Please upload an MP4 file to begin. Max size for live demo ~15MB recommended.")
    
st.markdown("---")
st.markdown("Built by Hackathon Winning Squad: Heena, Dharmender, Rishita. Submission: 18th April 2026")
