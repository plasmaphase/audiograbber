import requests
import json
from moviepy.editor import VideoFileClip

class StPaulVideo:
    def __init__(self, url, output_file):
        self.url = url
        self.output_file = output_file

    def download_mp4(self):
        # Send a GET request to the website
        response = requests.get(self.url)

        # Extract the JavaScript code from the response
        javascript_code = response.text

        # Find the start and end index of the ViewModelData object
        start_index = javascript_code.find("ViewModelData = {")
        end_index = javascript_code.find("};", start_index) + 1

        if start_index != -1 and end_index != -1:
            # Extract the ViewModelData object from the JavaScript code
            json_string = javascript_code[start_index:end_index]

            # Remove unwanted characters and convert to valid JSON format
            json_string = json_string.replace("ViewModelData =", "")
            json_string = json_string.replace(";", "")
            json_string = json_string.strip()

            # Load the JSON data
            data = json.loads(json_string)

            # Extract the MP4 link
            mp4_link = data.get("ThumbnailAssets", [{}])[0].get("FileDownloadUrl")

            if mp4_link:
                print(mp4_link)
                # Download the video
                response = requests.get(mp4_link)
                if response.status_code == 200:
                    # Save the video file
                    with open(self.output_file, 'wb') as file:
                        file.write(response.content)
                        print("Video downloaded successfully!")

                    # Extract audio from the video and save as MP3
                    audio_output_file = self.output_file.replace('.mp4', '.mp3')
                    self.extract_audio(self.output_file, audio_output_file)
                    print("Audio extracted successfully!")
                else:
                    print("Failed to download the video.")
            else:
                print("MP4 link not found in the HTML content.")
        else:
            print("ViewModelData object not found in the JavaScript code.")

    @staticmethod
    def extract_audio(video_path, audio_path):
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(audio_path)


