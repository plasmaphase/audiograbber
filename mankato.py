import os
import subprocess

class Mankato:
    def __init__(self, url, output_file):
        self.url = url
        self.output_file = output_file

    def download(self):
        # Specify the output directory for downloaded video files
        output_directory = os.path.dirname(self.output_file)

        # Download the videos using youtube-dl with the specified output directory
        subprocess.call(["youtube-dl", self.url, "--output", os.path.join(output_directory, "%(title)s.%(ext)s")])

        # Get the list of downloaded MP4 files
        video_files = [file for file in os.listdir(output_directory) if file.endswith(".mp4")]

        # Sort the video files based on their names
        video_files.sort()

        # Create a file to store the list of video files for concatenation
        file_list_path = os.path.join(output_directory, "file_list.txt")
        with open(file_list_path, "w") as f:
            for file in video_files:
                f.write(f"file '{os.path.join(output_directory, file)}'\n")

        # Concatenate the videos using ffmpeg
        concatenated_file = os.path.join(output_directory, "concatenated_video.mp4")
        subprocess.call(["ffmpeg", "-f", "concat", "-safe", "0", "-i", file_list_path, "-c", "copy", concatenated_file])

        # Convert the concatenated video to MP3
        mp3_output_file = os.path.splitext(self.output_file)[0] + ".mp3"
        subprocess.call(["ffmpeg", "-i", concatenated_file, mp3_output_file])

        # Clean up temporary files
        os.remove(file_list_path)
        os.remove(concatenated_file)
        for file in video_files:
            os.remove(os.path.join(output_directory, file))
  
        print("Conversion to MP3 complete.")
