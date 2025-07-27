from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Video Downloader Backend Running"

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    video_url = data.get('url')
    if not video_url:
        return jsonify({"error": "URL missing"}), 400
    return jsonify({"message": f"Processing download for {video_url}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
