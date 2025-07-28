from flask import Flask, request, jsonify
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route('/')
def home():
    return "Real Video Downloader Backend Active 🎬"

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({'error': 'URL is missing'}), 400

    # Unique file name
    video_id = str(uuid.uuid4())
    filename = f"{video_id}.mp4"
    output_path = f"./downloads/{filename}"

    os.makedirs("downloads", exist_ok=True)

    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        return jsonify({
            'message': 'Download successful',
            'download_url': request.host_url + f"download/{filename}"
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def serve_file(filename):
    from flask import send_from_directory
    return send_from_directory("downloads", filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
