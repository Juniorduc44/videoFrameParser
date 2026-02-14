# 🎬 Video Frame Parser - Simple All-in-One CLI Edition

**One Python script. GUI buttons run CLI backend. Super simple.**

---

## 🚀 Quick Start (3 Steps!)

### Step 1: Install Dependencies
```bash
pip install -r requirements_simple.txt
```

Or manually:
```bash
pip install Flask opencv-python Werkzeug
```

### Step 2: Run the Script
```bash
python video_frame_parser.py
```

You'll see:
```
╔══════════════════════════════════════════════════════════════════╗
║         🎬 VIDEO FRAME PARSER - ALL-IN-ONE CLI EDITION 🎬       ║
║  Server running on: http://localhost:8000                       ║
╚══════════════════════════════════════════════════════════════════╝
```

### Step 3: Open Browser
Go to: **http://localhost:8000**

Done! 🎉

---

## 📋 How It Works

1. **Browse** for your video file (any format: MP4, AVI, MOV, MKV, etc.)
2. **Set output directory** (or leave empty for temp folder)
3. **Choose settings**:
   - Frame interval (every 1, 2, 5, 10, 30, or 60 frames)
   - Quality (1-100)
   - Format (JPG or PNG)
4. **Click "Extract Frames"**
5. **Watch real-time CLI output** in the log
6. **Click "Open Output Folder"** when done

---

## ✨ Features

✅ **All-in-One**: HTML embedded in Python script  
✅ **CLI Backend**: Uses OpenCV for professional video processing  
✅ **Real-time Progress**: See CLI output live in browser  
✅ **No Limits**: Handles videos of ANY size (not browser-limited)  
✅ **Smart Processing**: OpenCV extracts frames efficiently  
✅ **Auto-Open Folder**: Click button to open output in file explorer  
✅ **Live Stats**: See total frames, FPS, duration, progress  

---

## 🎯 Perfect For

- Extracting frames from long videos (no browser timeouts)
- Processing large video files (multi-GB)
- Batch frame extraction with custom intervals
- Creating image datasets from videos
- Video analysis and thumbnailing

---

## 💻 Technical Details

**Backend:**
- Python + Flask (serves HTML + handles processing)
- OpenCV (cv2) for video processing
- Streams progress updates to browser in real-time

**Frontend:**
- Simple HTML form (embedded in Python)
- JavaScript handles file upload and progress display
- CSS styling for modern look

**How GUI Buttons Run CLI:**
1. User clicks "Extract Frames" in GUI
2. JavaScript sends video file to Python backend via POST
3. Python CLI (OpenCV) processes video frame-by-frame
4. Progress streamed back to browser as JSON
5. GUI updates in real-time with CLI output
6. Files saved directly to disk (no browser downloads!)

---

## 🎓 Example Usage

### Extract every 30th frame from a movie:
```
1. Run: python video_frame_parser.py
2. Open: http://localhost:8000
3. Upload: movie.mp4
4. Set: "Every 30th Frame"
5. Output: C:\Movies\Frames
6. Extract!
```

Result: All frames saved directly to C:\Movies\Frames with no browser prompts!

---

## 🔧 Customization

### Change Port
Edit line at bottom of script:
```python
app.run(host='0.0.0.0', port=9000)  # Use port 9000 instead
```

### Change Default Quality
Edit this line:
```python
quality = int(request.form.get('quality', 95))  # Default 95% instead of 90%
```

### Add More Format Options
Find this section in HTML and add options:
```html
<select id="format">
    <option value="jpg">JPEG (.jpg)</option>
    <option value="png">PNG (.png)</option>
    <option value="webp">WebP (.webp)</option>  <!-- Add this -->
</select>
```

---

## ❓ FAQ

**Q: Do I need to keep the browser open while extracting?**  
A: Yes, the browser shows progress. But the actual CLI processing happens on the server, so it won't timeout like pure JavaScript would.

**Q: Where do files get saved?**  
A: Either the directory you specify, or a temp folder if you leave it empty. Use "Open Output Folder" button to find them.

**Q: Can I process multiple videos?**  
A: Yes! Just upload a new video after the first finishes. The server stays running.

**Q: What video formats are supported?**  
A: Whatever OpenCV supports: MP4, AVI, MOV, MKV, FLV, WMV, WEBM, and many more.

**Q: Is this faster than the browser version?**  
A: YES! OpenCV is highly optimized C++ code. Much faster than browser Canvas API.

---

## 🐛 Troubleshooting

### "Module not found" error
```bash
pip install opencv-python Flask
```

### "Cannot open video file"
- Make sure video file isn't corrupted
- Try converting to MP4 first
- Check file permissions

### Server won't start (port in use)
```bash
# Find what's using port 8000
# Windows:
netstat -ano | findstr :8000

# Linux/Mac:
lsof -i :8000

# Then change port in script or kill the process
```

---

## 🎨 Why This Approach?

**Simple All-in-One Script vs Multi-File Setup:**

| Feature | All-in-One | Multi-File |
|---------|------------|------------|
| Setup | ✅ One file | ❌ Multiple files |
| Deployment | ✅ Copy one script | ❌ Copy folder structure |
| Maintenance | ✅ Edit one place | ❌ Update HTML + Python |
| Portability | ✅ Perfect | ⚠️ Good |
| Separation | ❌ HTML in Python | ✅ Clean separation |

**This all-in-one approach is perfect for:**
- Quick tools and utilities
- Single-purpose applications
- Easy sharing (just send one file!)
- Learning and prototyping

---

## 📦 What You Get

Just **TWO files**:
1. `video_frame_parser.py` - The complete application
2. `requirements_simple.txt` - Dependencies list

That's it! No separate HTML, CSS, or JS files to manage.

---

## 🚀 Pro Tips

1. **For very long videos**: Start with interval 30 or 60 to get a preview, then re-run with lower interval if needed
2. **Disk space**: JPEG at 90% quality is usually perfect - PNG files can be 5-10x larger
3. **Keep server running**: Process multiple videos without restarting
4. **Background processing**: Minimize browser, extraction continues in CLI
5. **Organize output**: Use descriptive folder names like "MovieName_Scene1"

---

**That's it! Simple, powerful, all-in-one.** 🎬✨

Built by Marcus Webwright - 50 years of making things simple and effective.
