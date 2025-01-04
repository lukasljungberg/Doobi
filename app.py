from flask import Flask, render_template, request, jsonify, send_file, Response, stream_with_context
import os
import json
from flask_cors import CORS
# Initialize Flask and pygame mixer
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_songs', methods=['POST'])
def add_songs():
    file = request.files.get("song")
    cover = request.files.get("cover")
    artist = request.form.get("artist")
    genre = request.form.get("genre")
    obj = {}
    file_path = os.path.join("uploads/songs", file.filename)
    file.save(file_path)
    obj['file_path'] = str(file_path).replace('/', '.')
    obj['artist'] = artist
    obj['genre'] = genre
    cover_path = os.path.join("uploads/covers", cover.filename)
    cover.save(cover_path)
    obj['cover_path'] = str(cover_path).replace('/', '.')
    with open('uploads/objects/'+file.filename+artist+'.json', 'w') as fp:
        json.dump(obj, fp)
    return jsonify({"status": "success!"})

@app.route('/objects/songs/<string:id>', methods=['GET'])
def download_multiple_files(id):
    dir = os.listdir('uploads/objects')
    idx = int(id)
    try:
        dir[idx]
    except:
        if len(dir) > 0:
            idx = (idx + 1) % (len(dir))
            with open('uploads/objects/'+dir[idx], 'r') as f:
                obj = json.load(f)
            return jsonify(obj)
        return Response(status=404)

# Stream an image file
@app.route('/stream-image/<string:fp>', methods=['GET'])
def stream_image(fp):
    fp = str(fp).replace('.', '/').replace('/jpg', '.jpg').replace('/png', '.png')
    def generate():
        with open(fp, 'rb') as f:
            while chunk := f.read(4096):  # Stream in chunks of 4096 bytes
                yield chunk
    return Response(generate(), content_type='image/jpeg')

# Stream an audio file
@app.route('/stream-audio/<string:fp>', methods=['GET'])
def stream_audio(fp):
    fp = str(fp).replace('.', '/').replace('/mp3', '.mp3')
    def generate():
        with open(fp, 'rb') as f:
            while chunk := f.read(4096):  # Stream in chunks of 4096 bytes
                yield chunk
    return Response(generate(), content_type='audio/mpeg')


if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
