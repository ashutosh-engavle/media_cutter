import os
import json
import mimetypes
from moviepy.editor import VideoFileClip, AudioFileClip
from tqdm import tqdm
import sys

def get_media_type(filename):
    mime_type, _ = mimetypes.guess_type(filename)
    if mime_type:
        if mime_type.startswith('audio'):
            return 'audio'
        elif mime_type.startswith('video'):
            return 'video'
    return None

def get_media_length(filepath, media_type):
    clip = None
    try:
        if media_type == 'video':
            clip = VideoFileClip(filepath)
        else:  # media_type == 'audio'
            clip = AudioFileClip(filepath)
        return clip.duration
    except Exception as e:
        # print(f"Error getting length for {filepath}: {e}")
        print(f"Error getting length for {filepath}: File might be corrupted.")
        return None
    finally:
        if clip:
            clip.close()


def list_media_files(directory):
    media_info = {'songs': {}, 'videos': {}}
    files_to_process = [(root, file) for root, _, files in os.walk(directory) for file in files]
    
    with tqdm(files_to_process, desc="Processing Files", unit="file") as pbar:
        for root, file in pbar:
            relative_path = os.path.relpath(root, directory)
            display_path = os.path.join(relative_path, file)
            pbar.set_description(f"Processing {display_path}")
            
            media_type = get_media_type(file)
            if media_type:
                full_path = os.path.join(root, file)
                length = get_media_length(full_path, media_type)
                if length is not None:
                    if media_type == 'video':
                        media_info['videos'][full_path] = {'length': length, 'new_length': length}
                    else:
                        media_info['songs'][full_path] = {'length': length, 'new_length': length}

    return media_info

def write_to_json(data, output_file='media_info.json'):
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: list.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"The specified path '{directory}' is not a valid directory.")
        sys.exit(1)

    media_info = list_media_files(directory)
    write_to_json(media_info)
    print("Media information has been written to media_info.json in the current working directory.")
