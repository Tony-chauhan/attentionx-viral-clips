import cv2
import mediapipe as mp
import moviepy.editor as mp_edit
from moviepy.video.tools.subtitles import SubtitlesClip
import numpy as np
import tempfile
import os

def get_smoothed_face_x(video_path, start_time, end_time, alpha=0.1):
    """
    Extracts frames, uses MediaPipe to find the face X-coordinate,
    and applies Exponential Moving Average (EMA) smoothing to prevent jitter.
    """
    mp_face = mp.solutions.face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.4)
    clip = mp_edit.VideoFileClip(video_path).subclip(start_time, end_time)
    
    x_positions = []
    
    # Iterate through frames
    for frame in clip.iter_frames():
        # MediaPipe needs RGB
        results = mp_face.process(frame)
        if results.detections:
            # Take the first face
            bbox = results.detections[0].location_data.relative_bounding_box
            # Middle of the bounding box
            x_center = bbox.xmin + (bbox.width / 2)
            # Clamp between 0 and 1
            x_positions.append(max(0.0, min(1.0, x_center)))
        else:
            # Fallback to previous position or center
            x_positions.append(x_positions[-1] if x_positions else 0.5)
            
    mp_face.close()

    if not x_positions:
        return [0.5]

    # Smooth the positions using EMA
    smoothed = [x_positions[0]]
    for i in range(1, len(x_positions)):
        smoothed.append(alpha * x_positions[i] + (1 - alpha) * smoothed[-1])
        
    return smoothed, clip.fps

def process_video(video_path, start_time, end_time, hook_text, transcript_text=""):
    """
    Takes the peak video segment, crops it to 9:16 keeping the face centered,
    and burns the visual hook into the video.
    """
    # 1. Get smoothed face track
    smoothed_x, fps = get_smoothed_face_x(video_path, start_time, end_time)
    
    clip = mp_edit.VideoFileClip(video_path).subclip(start_time, end_time)
    
    W, H = clip.size
    
    # Target dimensions for 9:16
    # We want max height, and width will be H * (9/16)
    target_H = H
    target_W = int(H * 9 / 16)
    
    # Avoid errors if target_W is bigger than W
    if target_W > W:
        target_W = W
        target_H = int(W * 16 / 9)
        
    def add_margins_and_crop(get_frame, t):
        # We need to know which frame index this corresponds to
        frame_idx = min(int(t * fps), len(smoothed_x) - 1)
        if frame_idx < 0: frame_idx = 0
            
        x_relative = smoothed_x[frame_idx]
        x_center_px = int(x_relative * W)
        
        # Calculate boundaries
        x1 = x_center_px - (target_W // 2)
        x2 = x_center_px + (target_W // 2)
        
        # Clamp to edges
        if x1 < 0:
            x1 = 0
            x2 = target_W
        if x2 > W:
            x2 = W
            x1 = W - target_W
            
        frame = get_frame(t)
        # Crop frame to height target_H and width target_W
        y1 = (H - target_H) // 2
        y2 = y1 + target_H
        
        cropped = frame[y1:y2, x1:x2]
        return cropped

    cropped_clip = mp_edit.VideoClip(add_margins_and_crop, duration=clip.duration)
    cropped_clip.fps = clip.fps
    cropped_clip = cropped_clip.set_audio(clip.audio)
    
    # 2. Add Overlay Hooks (Text)
    # Background for hook
    hook_bg = mp_edit.ColorClip(size=(target_W, int(target_H * 0.15)), color=(138, 43, 226)) # Purple
    hook_bg = hook_bg.set_opacity(0.8).set_duration(clip.duration).set_pos(("center", int(target_H * 0.05)))
    
    # Hook Text
    try:
        hook_text_clip = mp_edit.TextClip(
            hook_text, 
            fontsize=50, 
            color='white', 
            font='Arial-Bold', 
            method='caption', 
            size=(target_W*0.9, None), # Wrap to 90%
            align='center'
        )
        hook_text_clip = hook_text_clip.set_duration(clip.duration).set_pos(("center", int(target_H * 0.08)))
        
        # Assemble
        final = mp_edit.CompositeVideoClip([cropped_clip, hook_bg, hook_text_clip])
    except Exception as e:
        print(f"TextClip error (happens without ImageMagick). Ignoring text overlay: {e}")
        final = cropped_clip
        
    output_path = tempfile.mktemp(suffix=".mp4")
    # Use h264 for web compatibility
    final.write_videofile(
        output_path, 
        codec="libx264", 
        audio_codec="aac", 
        temp_audiofile='temp-audio.m4a', 
        remove_temp=True,
        logger=None # suppress verbose output for streamlit
    )
    
    return output_path
