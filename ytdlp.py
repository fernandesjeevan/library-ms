import sys
import os
from pathlib import Path
from yt_dlp import YoutubeDL

# Add the path to ffmpeg executables to the system path
ffmpeg_path = r"C:\Users\abdul\Downloads\ffmpeg-2024-11-18-git-970d57988d-full_build\ffmpeg-2024-11-18-git-970d57988d-full_build\bin"  # Adjust this to the actual location of your ffmpeg binaries
sys.path.append(ffmpeg_path)

def download_video(url, options):
    try: 
        with YoutubeDL(options) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"Error: {e}")

def get_available_formats(url):
    """Get available video formats and their resolution."""
    with YoutubeDL() as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get('formats', [])
        resolutions = {}
        for fmt in formats:
            if 'height' in fmt and 'ext' in fmt:
                resolution = fmt['height']
                extension = fmt['ext']
                resolutions[f"{resolution}p {extension}"] = fmt['format_id']
        return resolutions

def main():
    print("Welcome to YouTube Downloader!")
    print("1. Download Video")
    print("2. Download Audio")
    print("3. Download with Subtitles")

    choice = input("Enter your choice (1/2/3): ").strip()
    url = input("Enter the Video URL: ").strip()

    # Get available video formats (resolutions)
    available_resolutions = get_available_formats(url)
    
    if not available_resolutions:
        print("No available video formats found.")
        return
    
    print("Available resolutions:")
    for idx, resolution in enumerate(available_resolutions.keys(), 1):
        print(f"{idx}. {resolution}")

    resolution_choice = input("Choose the resolution (enter number): ").strip()
    try:
        resolution_choice = int(resolution_choice)
        if resolution_choice < 1 or resolution_choice > len(available_resolutions):
            print("Invalid choice!")
            return
    except ValueError:
        print("Invalid input!")
        return

    selected_format_id = list(available_resolutions.values())[resolution_choice - 1]

    # Default download location
    downloads_path = "C:/YoutubeVideos"
    os.makedirs(downloads_path, exist_ok=True)

    if choice == "1":
        options = {
            'outtmpl' : f'{downloads_path}/%(title)s.%(ext)s',
            'format': f'{selected_format_id}+bestaudio',
            'ffmpeg_location': ffmpeg_path,  # Ensure yt-dlp uses ffmpeg
        }
        download_video(url, options)
    elif choice == "2":
        options = {
            'outtmpl' : f'{downloads_path}/%(title)s.%(ext)s',
            'format' : 'bestaudio',
            'postprocessors' : [{
                'key' : 'FFmpegExtractAudio',
                'preferredcodec' : 'mp3',
                'preferredquality' : '192'
            }],
            'ffmpeg_location': ffmpeg_path,  # Ensure yt-dlp uses ffmpeg
        }
        download_video(url, options)
    elif choice == "3":
        options = {
            'outtmpl' : f'{downloads_path}/%(title)s.%(ext)s',
            'format': f'{selected_format_id}+bestaudio',
            'writesubtitles' : True,
            'subtitleslangs': ['en'],
            'ffmpeg_location': ffmpeg_path,  # Ensure yt-dlp uses ffmpeg
        }
        download_video(url, options)
    else:
        print("Invalid choice! Please restart")

    print("Download Completed!")

if __name__ == "__main__":
    main()