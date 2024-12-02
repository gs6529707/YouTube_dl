from flask import Flask, render_template, request, send_from_directory
import yt_dlp
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form['url']
    try:
        
        ydl_opts = {
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',  
            'format': 'bestvideo+bestaudio/best',              
            'merge_output_format': 'mp4',   
        }

        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        
        downloaded_files = os.listdir(DOWNLOAD_FOLDER)
        downloaded_files.sort(key=lambda x: os.path.getmtime(os.path.join(DOWNLOAD_FOLDER, x)))
        latest_file = downloaded_files[-1]

        return send_from_directory(DOWNLOAD_FOLDER, latest_file, as_attachment=True)

    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
