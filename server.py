from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify({'status': 'Server is online'})

@app.route('/download', methods=['POST'])
def handle_download():
    data = request.get_json() or {}
    video_url = data.get('url')
    format_type = data.get('format', 'mp4')

    if not video_url:
        return jsonify({'error': 'Please provide a valid URL'}), 400

    ydl_opts = {
        'format': 'bestaudio/best' if format_type == 'mp3' else 'best',
        'quiet': True,
        'socket_timeout': 15,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        },
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios']
            }
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return jsonify({
                'title': info.get('title'),
                'url': info.get('url'),
                'format': format_type
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
