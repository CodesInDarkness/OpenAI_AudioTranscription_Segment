import os
from openai import OpenAI
from pydub import AudioSegment
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)
import datetime
import requests
from requests.exceptions import RequestException

def download_mp3(url, file_path):
    try:
        # Send a HTTP request to the URL of the MP3 file
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for HTTP errors
        # Open the file in write mode to download the MP3 file
        with open(file_path, 'wb') as audio:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    audio.write(chunk)
        print(f"Downloaded successfully: {file_path}")
        return file_path
    except RequestException as e:
        print(f"Error during the request of {url}: {str(e)}")
        return None
    except Exception as e:
        print(f"Error during the download of {url}: {str(e)}")
        return None

# Transcribe audio file using Whisper API
def transcribe_audio_whisper_api(file_path):
    try:
        with open(file_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1", 
                file=file
                )
        return transcription
    except Exception as e:
        print(f"{datetime.datetime.now()} [ERROR]: Error in transcription: {e}")
        return None

# Summarize text using OpenAI Chat model
def summarize_text(text, style):
    try:
        # Using the chat endpoint
        if style != "4":
            if style == "1":
                content = f"Summarize the following text in bullet points, ordered by importance:\n{text}"
            elif style == "2":
                content = f"Summarize the following text in a short paragraph of 4 to 5 lines:\n{text}"
            elif style == "3":
                content = f"Summarize the following text concisely:\n{text}"
            elif style == "5":
                text_question = input("Please enter your custom query: ")
                content = f"{text_question}:\n{text}"
        
            messages = [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": content}]
            response = client.chat.completions.create(model="gpt-3.5-turbo-16k",
            messages=messages,
            max_tokens=1000)
            summary = response.choices[0].message.content
            return summary
        
        if style == "4":
            summary = text.text
            return summary

    except Exception as e:
        print(f"{datetime.datetime.now()} [ERROR]: Error in summarization: {e}")
        return None

# User input for source of MP3 file
print("Select the source of MP3 file:")
print("1 - Local MP3 File")
print("2 - Insert MP3 Link")
source = input("Enter 1 or 2: ")

file_path = None
if source == "1":
    file_path = input("Provide file path: ")
    print(f"{datetime.datetime.now()} [INFO]: User provided file '{file_path}'")
elif source == "2":
    # Download the MP3 file from the given link
    url = input("Enter the MP3 link: ")
    file_path = input("Enter the name of the podcast: ")
    file_path = file_path + '.mp3'
    file_path = download_mp3(url, file_path)
else:
    print("Invalid option selected. Please select either 1 or 2.")


if file_path:
    # Transcribe the audio using Whisper API
    podcast = AudioSegment.from_file(file_path)
    timestamp_grab = input("Provide the timestamp mark (hh:mm:ss): ")
    timestamp_go_back = int(input("How far back in mins should I go: "), 16)

    # User input for summarization style
    print("Select summarization style:")
    print("1 - Bullet Points")
    print("2 - Short Paragraph")
    print("3 - Concise")
    print("4 - Transcript")
    print("5 - Custom")
    style = input("Enter 1, 2, 3, 4, or 5: ")

    timestamp_end_sec = sum(int(x) * 60 ** i for i, x in enumerate(reversed(timestamp_grab.split(':'))))
    timestamp_end = (timestamp_end_sec + 15) * 1000
    timestamp_start = timestamp_end - (((timestamp_go_back) * 60 * 1000) + (15 * 1000))
    podcast_seg = podcast[timestamp_start:timestamp_end]

    original_file = Path(file_path)
    original_file_name = original_file.stem
    original_file_ext = original_file.suffix
    output_file = original_file_name + '_segment_' + timestamp_grab + original_file_ext

    summary_text_file = 'summary_' + original_file_name + '_' + timestamp_grab + '.txt'

    print(f"{datetime.datetime.now()} [INFO]: Exporting segment to audio file {output_file}...")
    podcast_seg.export(output_file, format=original_file_ext.replace('.',''))

    print(f"{datetime.datetime.now()} [INFO]: Transcribing audio...")
    transcription = transcribe_audio_whisper_api(output_file)

    # Analyze emotion from the transcription using OpenAI GPT model
    if transcription:
        # Summarize the transcription using OpenAI Chat model
        print(f"{datetime.datetime.now()} [INFO]: Summarizing text...")
        summary = summarize_text(transcription, style)
        print(f"{datetime.datetime.now()} [INFO]: Summary: {summary}")

        # Download the summary as a text file
        with open(summary_text_file, 'w') as f:
            f.write(summary)