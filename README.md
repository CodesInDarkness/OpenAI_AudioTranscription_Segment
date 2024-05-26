# OpenAI_AudioTranscription_Segment
Python script which will segment an audio file locally or download from URL link and send the segment to OpenAI Whisper for Transcription

## Getting Started
### Prerequisites
Ensure the following is installed:
- Python 3
- Pip (Python Package Installer)

## Installing
1. Clone the repository
    - ``` bash
      git clone https://github.com/CodesInDarkness/OpenAI_AudioTranscription_Segment.git
      ```
2. Navigate to the Project Directory
    - ```bash
      cd OpenAI_AudioTranscription_Segment
      ```
3. Create a Python virtualenv
    - ```bash
      python -m venv env
      ```
4. Use the current virtualenv (linux)
    - ```bash
      source env/bin/activate
      ```
5. Install the required Python Libraries
    - ```bash
      pip install -r requirements.txt
      ```
6. Add OpenAI API Key to .env file
    - ```bash
      nano .env
      ```
7. In the file add the following Variable and include your OpenAI API Key
    - ```bash
      OPENAI_API_KEY=
      ```

## Running the Program
Once the above requirements have been satisfied all you need to do is run the script. If you have a link or local file you will pass the full URL or full path to the file into the script when asked

To run the script all you need to do is call it:
```bash
python3 OpenAI_AudioTranscription_SegementAudio.py
```
