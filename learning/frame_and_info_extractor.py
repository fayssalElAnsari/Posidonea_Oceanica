import cv2
import pandas as pd
import re
from datetime import datetime, timedelta
from tqdm import tqdm
import os

# Function to parse subtitle file
def parse_srt(file_path):
    pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n<font size="28">FrameCnt: (\d+), DiffTime: \d+ms\n(.*?)\[latitude: ([\d\.]+)\] \[longitude: ([\d\.]+)\] \[rel_alt: ([\d\.]+) abs_alt: [\d\.]+\]', re.DOTALL)
    
    with open(file_path, 'r') as file:
        content = file.read()
    
    matches = pattern.findall(content)
    
    data = []
    for match in matches:
        frame_info = {
            "frame_nb": int(match[3]),
            "start_time": match[1],
            "end_time": match[2],
            "latitude": float(match[5]),
            "longitude": float(match[6]),
            "altitude": float(match[7]),
            "datetime": datetime.strptime(match[4].split('\n')[0], "%Y-%m-%d %H:%M:%S.%f")
        }
        data.append(frame_info)
    
    return pd.DataFrame(data)

# Function to extract frames and match with subtitle info
def extract_frames_and_match_subtitles(video_path, subtitle_df, frame_interval=15, output_folder="frames_2"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    subtitle_df['frame_time'] = (subtitle_df['datetime'] - subtitle_df['datetime'][0]).dt.total_seconds()
    subtitle_df['frame_time'] *= fps
    subtitle_df['frame_time'] = subtitle_df['frame_time'].astype(int)
    
    matched_data = []
    
    for i in tqdm(range(0, frame_count, frame_interval), desc="Extracting frames"):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if not ret:
            break
        frame_name = f"frame_{i}.jpg"
        cv2.imwrite(f"{output_folder}/{frame_name}", frame)
        
        closest_subtitle = subtitle_df.iloc[(subtitle_df['frame_time'] - i).abs().argsort()[:1]]
        matched_data.append({
            "name": frame_name,
            "long": closest_subtitle['longitude'].values[0],
            "lat": closest_subtitle['latitude'].values[0],
            "H": closest_subtitle['altitude'].values[0],
            "time": closest_subtitle['datetime'].values[0]
        })
    
    cap.release()
    
    return pd.DataFrame(matched_data)

# Paths to the video and subtitle files
video_path = "DJI_20231125134955_0002_D.MP4"
srt_path = "DJI_20231125134955_0002_D.SRT"

# Parse subtitle file
subtitle_df = parse_srt(srt_path)

# Extract frames and match with subtitle info
matched_df = extract_frames_and_match_subtitles(video_path, subtitle_df)

# Save to CSV
matched_df.to_csv("output_2.csv", index=False)

print("Extraction and matching complete. The data has been saved to output_2.csv.")
