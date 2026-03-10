from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import json

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

DATA_FILE = 'anime_data.json'
MY_PASSWORD = "anime123"  # Upload password

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/')
def index():
    data = load_data()
    # Unique Anime Names nikalne ke liye
    anime_list = list(set([item['anime'] for item in data]))
    anime_list.sort()
    return render_template('index.html', anime_list=anime_list, data=data)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        password = request.form.get('password')
        if password != MY_PASSWORD:
            return "Access Denied!"
        
        anime_name = request.form.get('anime_name').strip()
        episode_no = request.form.get('episode_no')
        video = request.files.get('video')
        
        if video and anime_name and episode_no:
            filename = video.filename
            video.save(os.path.join(UPLOAD_FOLDER, filename))
            
            data = load_data()
            data.append({
                'anime': anime_name,
                'episode': episode_no,
                'video': filename
            })
            save_data(data)
            return redirect(url_for('index'))
            
    return render_template('upload.html')

@app.route('/watch/<filename>')
def watch(filename):
    return render_template('watch.html', filename=filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)