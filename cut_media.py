import os
import sys
import json
import mimetypes
from moviepy.editor import VideoFileClip, AudioFileClip
from tqdm import tqdm

def cut_media(file_path, new_length, output_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    clip = None

    if mime_type and mime_type.startswith('video'):
        clip = VideoFileClip(file_path)
    elif mime_type and mime_type.startswith('audio'):
        clip = AudioFileClip(file_path)
    else:
        print(f"Unsupported media type for file {file_path}")
        return

    cut_clip = clip.subclip(0, new_length)

    if mime_type.startswith('video'):
        cut_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
    else:
        cut_clip.write_audiofile(output_path)

    clip.close()
    cut_clip.close()

def process_media_json(json_file):
    with open(json_file, 'r') as f:
        media_info = json.load(f)

    media_entries = {**media_info['songs'], **media_info['videos']}.items()
    for file_path, details in tqdm(media_entries, desc="Initializing...", unit="file"):
        length, new_length = details['length'], details['new_length']
        if new_length < length:
            tqdm.write(f"Cutting {os.path.basename(file_path)}")
            output_path = file_path.rsplit('.', 1)[0] + '_cut.' + file_path.split('.')[-1]
            cut_media(file_path, new_length, output_path)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: cut_media.py <path to json>")
        sys.exit(1)

    json_file = sys.argv[1]
    process_media_json(json_file)
    print("Finished processing media files.")
