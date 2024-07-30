import youtube_dl
from youtube_transcript_api import YouTubeTranscriptApi
from googletrans import Translator

def download_video(video_url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None

def save_transcript_to_file(transcript, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        for entry in transcript:
            file.write(entry['text'] + '\n')

def translate_to_hindi(text):
    translator = Translator()
    translation = translator.translate(text, dest='hi')
    return translation.text

if __name__ == "__main__":
    video_url = input("Enter YouTube video URL: ")
    output_path = input("Enter output path for the transcript file (e.g., transcript.txt): ")

    video_info = youtube_dl.YoutubeDL().extract_info(url=video_url, download=False)
    video_id = video_info['id']

    download_video(video_url, f"{video_id}.mp4")
    transcript = get_transcript(video_id)

    if transcript:
        transcript_list = []
        translated_transcript_list = []

        for entry in transcript:
            transcript_list.append(entry['text'])
            translated_text = translate_to_hindi(entry['text'])
            translated_transcript_list.append(translated_text)

        save_transcript_to_file(transcript, output_path)

        print(f"Transcript saved to {output_path}")
        print("Original Transcript Entries:")
        for entry in transcript_list:
            print(entry)

        print("\nTranslated Transcript Entries (Hindi):")
        for entry in translated_transcript_list:
            print(entry)
    else:
        print("Failed to retrieve transcript.")
