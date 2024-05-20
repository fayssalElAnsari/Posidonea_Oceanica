import cv2
import os
import numpy as np
from tqdm import tqdm

def extract_frames(video_path, output_folder, frame_interval):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    extracted_count = 0

    with tqdm(total=frame_count // frame_interval, desc="Extracting frames") as pbar:
        for i in range(frame_count):
            ret, frame = cap.read()
            if not ret:
                break
            if i % frame_interval == 0:
                frame_filename = os.path.join(output_folder, f"frame_{extracted_count:04d}.jpg")
                cv2.imwrite(frame_filename, frame)
                extracted_count += 1
                pbar.update(1)

    cap.release()

def read_frames_from_folder(folder):
    frame_files = sorted([os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.jpg')])
    frames = []
    
    with tqdm(total=len(frame_files), desc="Reading frames") as pbar:
        for file in frame_files:
            frame = cv2.imread(file)
            frames.append(frame)
            pbar.update(1)
    
    return frames

def stitch_frames(frames):
    stitcher = cv2.createStitcher() if int(cv2.__version__.split('.')[0]) < 4 else cv2.Stitcher_create()
    print("Stitching frames...")
    with tqdm(total=1, desc="Stitching") as pbar:
        status, pano = stitcher.stitch(frames)
        pbar.update(1)
    if status == cv2.Stitcher_OK:
        return pano
    else:
        print("Error during stitching. Status code:", status)
        return None

def save_image(image, output_path):
    print("Saving stitched image...")
    with tqdm(total=1, desc="Saving") as pbar:
        cv2.imwrite(output_path, image)
        pbar.update(1)

def generate_2d_map(video_path, output_folder, output_path, frame_interval=30):
    extract_frames(video_path, output_folder, frame_interval)
    frames = read_frames_from_folder(output_folder)
    if len(frames) == 0:
        print("No frames extracted.")
        return

    panorama = stitch_frames(frames)
    if panorama is not None:
        save_image(panorama, output_path)
        print(f"2D map saved to {output_path}")
    else:
        print("Stitching failed.")

# Example usage
video_path = 'sample.mp4'
output_folder = 'frames'
output_path = 'output_map.jpg'
generate_2d_map(video_path, output_folder, output_path)
