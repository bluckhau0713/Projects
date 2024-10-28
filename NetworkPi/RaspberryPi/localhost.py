from flask import Flask, send_from_directory, render_template, send_file

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/static/<filename>')
def serve_image(filename):
    return send_from_directory('static', filename)

@app.route('/static/videos/<filename>')
def video(filename):
    video_path = f'static/videos/{filename}'
    return send_from_directory('static/videos', filename, mimetype='video/mp4', conditional=True)

app.run(host='secretIP', port=5000, debug=False)
