#!/usr/bin/env python3
"""
Video Frame Parser - All-in-One CLI Edition
Simple Python script that serves HTML GUI but does all processing via CLI backend.

Usage:
    python video_frame_parser.py
    
Then open browser to: http://localhost:8000
"""

from flask import Flask, render_template_string, request, jsonify, send_file
from werkzeug.utils import secure_filename
import cv2
import os
import base64
from pathlib import Path
import tempfile
import shutil

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Frame Parser - CLI Edition</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        
        .card {
            background: white;
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            margin-bottom: 20px;
        }
        
        h1 {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-align: center;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }
        
        .control-group {
            margin-bottom: 25px;
        }
        
        label {
            display: block;
            font-weight: 600;
            color: #555;
            margin-bottom: 8px;
        }
        
        input[type="text"],
        input[type="number"],
        select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
            transition: all 0.3s ease;
        }
        
        input:focus, select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .button {
            width: 100%;
            padding: 15px;
            font-size: 1.1em;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-bottom: 10px;
        }
        
        .button-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .button-primary:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        
        .button-primary:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .button-secondary {
            background: white;
            color: #667eea;
            border: 2px solid #667eea;
        }
        
        .button-secondary:hover {
            background: #667eea;
            color: white;
        }
        
        .file-input-wrapper {
            position: relative;
            overflow: hidden;
            display: inline-block;
            width: 100%;
        }
        
        .file-input-wrapper input[type=file] {
            position: absolute;
            left: -9999px;
        }
        
        .file-label {
            display: block;
            padding: 15px;
            background: #f8f9fa;
            border: 2px dashed #667eea;
            border-radius: 8px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .file-label:hover {
            background: #e8e9ff;
            border-color: #764ba2;
        }
        
        .file-name {
            margin-top: 10px;
            color: #667eea;
            font-weight: 600;
        }
        
        .info-box {
            background: #e8f4f8;
            border-left: 4px solid #667eea;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            color: #555;
        }
        
        .progress {
            width: 100%;
            height: 30px;
            background: #e0e0e0;
            border-radius: 15px;
            overflow: hidden;
            margin-bottom: 20px;
            display: none;
        }
        
        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            width: 0%;
            transition: width 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
        }
        
        .status {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
            font-weight: 500;
        }
        
        .status.success {
            background: #d4edda;
            color: #155724;
            border-left: 4px solid #28a745;
        }
        
        .status.error {
            background: #f8d7da;
            color: #721c24;
            border-left: 4px solid #dc3545;
        }
        
        .status.info {
            background: #d1ecf1;
            color: #0c5460;
            border-left: 4px solid #17a2b8;
        }
        
        .video-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
            display: none;
        }
        
        .info-card {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        
        .info-label {
            font-size: 0.85em;
            color: #999;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        
        .info-value {
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
        }
        
        .log {
            background: #2d2d2d;
            color: #0f0;
            padding: 20px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            max-height: 300px;
            overflow-y: auto;
            display: none;
        }
        
        .log-line {
            margin-bottom: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>🎬 Video Frame Parser</h1>
            <p class="subtitle">CLI-Powered Frame Extraction</p>
            
            <div class="status" id="status"></div>
            
            <div class="control-group">
                <label>📹 Select Video File</label>
                <div class="file-input-wrapper">
                    <label for="videoFile" class="file-label">
                        <span>Click to Browse Video Files</span>
                    </label>
                    <input type="file" id="videoFile" accept="video/*">
                </div>
                <div class="file-name" id="fileName"></div>
            </div>
            
            <div class="control-group">
                <label for="outputDir">📁 Output Directory</label>
                <input type="text" id="outputDir" placeholder="C:\\Users\\YourName\\Videos\\Frames" 
                       value="">
                <small style="color: #999; display: block; margin-top: 5px;">
                    Leave empty to use temporary directory
                </small>
            </div>
            
            <div class="control-group">
                <label for="frameInterval">🎯 Frame Interval</label>
                <select id="frameInterval">
                    <option value="1">Every Frame (1:1)</option>
                    <option value="2">Every 2nd Frame (1:2)</option>
                    <option value="5">Every 5th Frame (1:5)</option>
                    <option value="10" selected>Every 10th Frame (1:10)</option>
                    <option value="30">Every 30th Frame (1:30)</option>
                    <option value="60">Every 60th Frame (1:60)</option>
                </select>
            </div>
            
            <div class="control-group">
                <label for="quality">🎨 Image Quality (1-100)</label>
                <input type="number" id="quality" min="1" max="100" value="90">
            </div>
            
            <div class="control-group">
                <label for="format">📄 Output Format</label>
                <select id="format">
                    <option value="jpg" selected>JPEG (.jpg)</option>
                    <option value="png">PNG (.png)</option>
                </select>
            </div>
            
            <div class="info-box">
                💡 <strong>Tip:</strong> All processing happens via CLI backend using OpenCV. 
                No browser limitations - can handle videos of any size!
            </div>
            
            <button class="button button-primary" id="extractBtn" disabled onclick="extractFrames()">
                🚀 Extract Frames (CLI)
            </button>
            
            <div class="progress" id="progress">
                <div class="progress-bar" id="progressBar">0%</div>
            </div>
            
            <div class="video-info" id="videoInfo">
                <div class="info-card">
                    <div class="info-label">Frames</div>
                    <div class="info-value" id="totalFrames">0</div>
                </div>
                <div class="info-card">
                    <div class="info-label">Duration</div>
                    <div class="info-value" id="duration">0s</div>
                </div>
                <div class="info-card">
                    <div class="info-label">FPS</div>
                    <div class="info-value" id="fps">0</div>
                </div>
                <div class="info-card">
                    <div class="info-label">Extracted</div>
                    <div class="info-value" id="extracted">0</div>
                </div>
            </div>
            
            <div class="log" id="log">
                <div class="log-line">📟 CLI Output:</div>
            </div>
            
            <button class="button button-secondary" id="openFolderBtn" style="display: none;" 
                    onclick="openOutputFolder()">
                📂 Open Output Folder
            </button>
        </div>
    </div>
    
    <script>
        let currentVideoFile = null;
        let outputPath = '';
        
        // File input handler
        document.getElementById('videoFile').addEventListener('change', function(e) {
            if (e.target.files.length > 0) {
                currentVideoFile = e.target.files[0];
                document.getElementById('fileName').textContent = '✓ ' + currentVideoFile.name;
                document.getElementById('extractBtn').disabled = false;
                showStatus('Video selected: ' + currentVideoFile.name, 'success');
            }
        });
        
        // Extract frames function
        async function extractFrames() {
            if (!currentVideoFile) {
                showStatus('Please select a video file first', 'error');
                return;
            }
            
            const formData = new FormData();
            formData.append('video', currentVideoFile);
            formData.append('output_dir', document.getElementById('outputDir').value);
            formData.append('interval', document.getElementById('frameInterval').value);
            formData.append('quality', document.getElementById('quality').value);
            formData.append('format', document.getElementById('format').value);
            
            // UI updates
            document.getElementById('extractBtn').disabled = true;
            document.getElementById('progress').style.display = 'block';
            document.getElementById('log').style.display = 'block';
            document.getElementById('videoInfo').style.display = 'grid';
            addLog('🚀 Starting CLI extraction...');
            
            try {
                const response = await fetch('/extract', {
                    method: 'POST',
                    body: formData
                });
                
                if (!response.ok) {
                    throw new Error('Server error');
                }
                
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                
                while (true) {
                    const {value, done} = await reader.read();
                    if (done) break;
                    
                    const text = decoder.decode(value);
                    const lines = text.split('\\n');
                    
                    for (const line of lines) {
                        if (!line.trim()) continue;
                        
                        try {
                            const data = JSON.parse(line);
                            handleProgressUpdate(data);
                        } catch (e) {
                            // Not JSON, just log it
                            if (line.trim()) addLog(line);
                        }
                    }
                }
                
            } catch (error) {
                showStatus('Error: ' + error.message, 'error');
                addLog('❌ Error: ' + error.message);
            } finally {
                document.getElementById('extractBtn').disabled = false;
            }
        }
        
        // Handle progress updates from server
        function handleProgressUpdate(data) {
            if (data.type === 'info') {
                document.getElementById('totalFrames').textContent = data.total_frames || '0';
                document.getElementById('duration').textContent = data.duration || '0s';
                document.getElementById('fps').textContent = data.fps || '0';
            }
            else if (data.type === 'progress') {
                const percent = Math.round((data.current / data.total) * 100);
                document.getElementById('progressBar').style.width = percent + '%';
                document.getElementById('progressBar').textContent = percent + '%';
                document.getElementById('extracted').textContent = data.current;
                addLog(`✓ Frame ${data.current}/${data.total} saved`);
            }
            else if (data.type === 'complete') {
                showStatus(`Success! Extracted ${data.frames_saved} frames`, 'success');
                addLog(`\\n✅ Complete! ${data.frames_saved} frames saved to:\\n   ${data.output_path}`);
                outputPath = data.output_path;
                document.getElementById('openFolderBtn').style.display = 'block';
            }
            else if (data.type === 'error') {
                showStatus('Error: ' + data.message, 'error');
                addLog('❌ ' + data.message);
            }
            else if (data.type === 'log') {
                addLog(data.message);
            }
        }
        
        // Open output folder
        async function openOutputFolder() {
            if (!outputPath) return;
            
            try {
                const response = await fetch('/open-folder', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({path: outputPath})
                });
                
                const data = await response.json();
                if (data.status === 'success') {
                    showStatus('Opened folder in file explorer', 'success');
                } else {
                    showStatus('Could not open folder: ' + data.message, 'error');
                }
            } catch (error) {
                showStatus('Error opening folder', 'error');
            }
        }
        
        // UI helper functions
        function showStatus(message, type) {
            const status = document.getElementById('status');
            status.textContent = message;
            status.className = 'status ' + type;
            status.style.display = 'block';
            
            if (type === 'success' || type === 'error') {
                setTimeout(() => {
                    status.style.display = 'none';
                }, 5000);
            }
        }
        
        function addLog(message) {
            const log = document.getElementById('log');
            const line = document.createElement('div');
            line.className = 'log-line';
            line.textContent = message;
            log.appendChild(line);
            log.scrollTop = log.scrollHeight;
        }
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    """Serve the HTML interface"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/extract', methods=['POST'])
def extract_frames():
    """Extract frames from video using OpenCV (CLI backend)"""
    import json
    
    def generate():
        try:
            # Get form data
            video_file = request.files.get('video')
            output_dir = request.form.get('output_dir', '').strip()
            interval = int(request.form.get('interval', 10))
            quality = int(request.form.get('quality', 90))
            format_ext = request.form.get('format', 'jpg')
            
            if not video_file:
                yield json.dumps({'type': 'error', 'message': 'No video file provided'}) + '\n'
                return
            
            # Save uploaded video to temp file
            temp_dir = tempfile.mkdtemp()
            video_path = os.path.join(temp_dir, secure_filename(video_file.filename))
            video_file.save(video_path)
            
            yield json.dumps({'type': 'log', 'message': f'📹 Video saved: {video_file.filename}'}) + '\n'
            
            # Create output directory
            if not output_dir:
                output_dir = os.path.join(temp_dir, 'frames')
            
            os.makedirs(output_dir, exist_ok=True)
            yield json.dumps({'type': 'log', 'message': f'📁 Output directory: {output_dir}'}) + '\n'
            
            # Open video with OpenCV
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                yield json.dumps({'type': 'error', 'message': 'Could not open video file'}) + '\n'
                return
            
            # Get video info
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            duration = total_frames / fps if fps > 0 else 0
            
            yield json.dumps({
                'type': 'info',
                'total_frames': total_frames,
                'fps': f'{fps:.2f}',
                'duration': f'{duration:.1f}s'
            }) + '\n'
            
            yield json.dumps({'type': 'log', 'message': f'🎬 Total frames: {total_frames}'}) + '\n'
            yield json.dumps({'type': 'log', 'message': f'⚡ FPS: {fps:.2f}'}) + '\n'
            yield json.dumps({'type': 'log', 'message': f'⏱️  Duration: {duration:.1f}s'}) + '\n'
            yield json.dumps({'type': 'log', 'message': f'🎯 Extracting every {interval} frames...'}) + '\n'
            
            # Extract frames
            frame_count = 0
            saved_count = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Save frame at specified interval
                if frame_count % interval == 0:
                    # Generate filename
                    filename = f'frame_{str(saved_count).zfill(6)}.{format_ext}'
                    filepath = os.path.join(output_dir, filename)
                    
                    # Save frame
                    if format_ext == 'jpg':
                        cv2.imwrite(filepath, frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
                    else:  # png
                        cv2.imwrite(filepath, frame, [cv2.IMWRITE_PNG_COMPRESSION, 9])
                    
                    saved_count += 1
                    
                    # Send progress update
                    if saved_count % 10 == 0 or saved_count == 1:
                        yield json.dumps({
                            'type': 'progress',
                            'current': saved_count,
                            'total': total_frames // interval
                        }) + '\n'
                
                frame_count += 1
            
            cap.release()
            
            # Clean up temp video file
            try:
                os.remove(video_path)
            except:
                pass
            
            # Send completion message
            yield json.dumps({
                'type': 'complete',
                'frames_saved': saved_count,
                'output_path': output_dir
            }) + '\n'
            
        except Exception as e:
            yield json.dumps({'type': 'error', 'message': str(e)}) + '\n'
    
    return app.response_class(generate(), mimetype='application/json')


@app.route('/open-folder', methods=['POST'])
def open_folder():
    """Open output folder in file explorer"""
    import subprocess
    import platform
    
    try:
        data = request.get_json()
        folder_path = data.get('path', '')
        
        if not os.path.exists(folder_path):
            return jsonify({'status': 'error', 'message': 'Folder does not exist'}), 400
        
        # Open folder based on OS
        system = platform.system()
        
        if system == 'Windows':
            os.startfile(folder_path)
        elif system == 'Darwin':  # macOS
            subprocess.run(['open', folder_path])
        else:  # Linux
            subprocess.run(['xdg-open', folder_path])
        
        return jsonify({'status': 'success', 'message': 'Folder opened'}), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


def print_banner():
    """Print startup banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║         🎬 VIDEO FRAME PARSER - ALL-IN-ONE CLI EDITION 🎬       ║
║                                                                  ║
║  Server running on: http://localhost:8000                       ║
║  Open this URL in your browser to use the GUI                   ║
║                                                                  ║
║  All processing happens via CLI backend using OpenCV            ║
║  No browser limitations - handles videos of any size!           ║
║                                                                  ║
║  Press Ctrl+C to stop the server                                ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """
    print(banner)


if __name__ == '__main__':
    print_banner()
    
    # Run server
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=False,
        threaded=True
    )
