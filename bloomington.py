import subprocess

class M3U8Downloader:
    def __init__(self, url, output_file):
        self.url = url
        self.output_file = output_file + ".aac"

    def download_audio(self):
        subprocess.run(['ffmpeg', '-i', self.url, '-vn', '-acodec', 'copy', self.output_file])

    def convert_to_mp3(self):
        mp3_file = self.output_file[:-4] + '.mp3'
        subprocess.run(['ffmpeg', '-i', self.output_file, '-vn', '-acodec', 'libmp3lame', mp3_file])
        return mp3_file

    def remove_file(self, file_path):
        subprocess.run(['rm', file_path])

    def process_m3u8(self):
        self.download_audio()
        mp3_file = self.convert_to_mp3()
        self.remove_file(self.output_file)
        return mp3_file

# Example usage
m3u8_url = "https://reflect-bcit.cablecast.tv/vod-45/51283-VMix-SBMTG-10-10-22-ca-v1/vod.m3u8"
output_file = "audio"

downloader = M3U8Downloader(m3u8_url, output_file)
mp3_file = downloader.process_m3u8()

print(f"MP3 file saved as: {mp3_file}")
