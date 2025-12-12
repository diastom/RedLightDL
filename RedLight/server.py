from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os
import traceback

# Ensure we can import from local package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from RedLight.api import (
    GetActiveDownloads,
    StartResumableDownload,
    GetVideoInfo,
    CancelDownload,
    GetStatistics,
    GetDownloadHistory
)
from RedLight.config import ConfigManager

app = Flask(__name__) # Initialize first to access helpers if needed, but we'll override static config

def get_static_folder():
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app 
        # path into variable _MEIPASS.
        # For 'onedir' mode, we expect assets in the same dir as executable/script
        base_path = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(os.path.abspath(__file__))
        
        # When using --add-data, folders are preserved. 
        # We mapped "gui/client/dist" -> "gui/client/dist"
        return os.path.join(base_path, 'gui', 'client', 'dist')
    else:
        # Normal python execution
        return '../gui/client/dist'

static_folder = get_static_folder()
app = Flask(__name__, static_folder=static_folder, static_url_path='/')
CORS(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        stats = GetStatistics()
        return jsonify(stats)
    except Exception as e:
        traceback.print_exc()
        try:
            with open(os.path.expanduser("~/.RedLight/error.log"), "a") as f:
                f.write(traceback.format_exc() + "\n")
        except:
            pass
        return jsonify({"error": str(e)}), 500

@app.route('/api/downloads/history', methods=['GET'])
def get_history():
    try:
        limit = int(request.args.get('limit', 10))
        history = GetDownloadHistory(limit=limit)
        return jsonify(history)
    except Exception as e:
        traceback.print_exc()
        try:
            with open(os.path.expanduser("~/.RedLight/error.log"), "a") as f:
                f.write(traceback.format_exc() + "\n")
        except:
            pass
        return jsonify({"error": str(e)}), 500

@app.route('/api/downloads/active', methods=['GET'])
def get_active():
    try:
        active = GetActiveDownloads()
        return jsonify(active)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/download', methods=['POST'])
def start_download():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    try:
        # Start async/resumable download
        download_id = StartResumableDownload(url)
        return jsonify({"success": True, "id": download_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/cancel', methods=['POST'])
def cancel_download():
    data = request.json
    download_id = data.get('download_id')
    if not download_id:
        return jsonify({"error": "Download ID is required"}), 400
    try:
        success = CancelDownload(download_id)
        return jsonify({"success": success})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/info', methods=['GET'])
def get_info():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400
    try:
        info = GetVideoInfo(url)
        return jsonify(info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/config', methods=['GET'])
def get_config():
    try:
        from RedLight.config import GetConfig
        config = GetConfig()
        return jsonify(config.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/config', methods=['POST'])
def update_config():
    try:
        from RedLight.config import GetConfigManager, Config
        data = request.json
        cm = GetConfigManager()
        current_config = cm.get()
        
        # Update download settings
        if 'downloadPath' in data:
            current_config.download.output_directory = data['downloadPath']
        if 'maxConcurrent' in data:
            current_config.download.max_concurrent = int(data['maxConcurrent'])
        if 'quality' in data:
            current_config.download.default_quality = data['quality']
        
        cm.save(current_config)
        return jsonify({"success": True, "config": current_config.to_dict()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/search', methods=['GET'])
def search_videos():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Query is required"}), 400
    try:
        from RedLight.multi_search import MultiSiteSearch
        engine = MultiSiteSearch()
        results = engine.search_all(query)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/playlist', methods=['GET'])
def get_playlist_videos():
    """Get list of videos from a channel/playlist URL"""
    url = request.args.get('url')
    limit = int(request.args.get('limit', 10))
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    try:
        from RedLight.playlist import PlaylistDownloader
        downloader = PlaylistDownloader()
        videos = downloader.GetChannelVideos(url, limit=limit)
        return jsonify({"videos": videos, "count": len(videos)})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/playlist/download', methods=['POST'])
def download_playlist():
    """Start downloading all videos from a playlist"""
    data = request.json
    url = data.get('url')
    limit = int(data.get('limit', 10))
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    try:
        from RedLight.playlist import PlaylistDownloader
        downloader = PlaylistDownloader()
        videos = downloader.GetChannelVideos(url, limit=limit)
        
        download_ids = []
        for video_url in videos:
            try:
                download_id = StartResumableDownload(video_url)
                download_ids.append({"url": video_url, "id": download_id})
            except Exception as e:
                download_ids.append({"url": video_url, "error": str(e)})
        
        return jsonify({"success": True, "downloads": download_ids})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting RedLight API Server on port 5000...")
    app.run(host='127.0.0.1', port=5000, debug=True)
