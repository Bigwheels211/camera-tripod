from flask import Flask, Response, jsonify, send_from_directory, send_file
from facialTracking import FacialTracking
import time
import camera
import os
import stopwatch

app = Flask(__name__, static_folder = "static")
app.config['DOWNLOAD_FOLDER'] = 'static'
controller = FacialTracking()

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/startFacial")
def start():
    controller.start()
    return jsonify({"status": "started"})

@app.route("/stop")
def stop():
    controller.stop()
    return jsonify({"status": "stopped"})


@app.route("/status")
def status():
    return jsonify({"running": controller.running})

@app.route("/video")
def video():
    def generate():
        while True:
            if controller.running:
                frame = controller.get_frame_jpeg()
            else:
                frame = camera.getJPEG()
            if frame:
                yield (b"--frame\r\n"
                       b"Content-Type: image/jpeg\r\n\r\n" +
                       frame +
                       b"\r\n")
            time.sleep(0.03)

    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")
@app.route("/takePic")
def takePic():
    camera.saveJPEG()
    return send_file("static/bufferimage.jpeg", mimetype='image/jpeg')
@app.route("/previewimg")
def previewimg():
    return send_file("static/bufferimage.jpeg", mimetype='image/jpeg')
@app.route("/downloadimg")
def downloadimg():
    return send_from_directory('static', 'bufferimage.jpeg', as_attachment=True)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=camera.getPort(), threaded=True)
