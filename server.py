from flask import Flask, Response, jsonify, send_from_directory
from facialTracking import FacialTracking
import time


app = Flask(__name__, static_folder = "static")
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
            frame = controller.get_frame_jpeg()
            if frame:
                yield (b"--frame\r\n"
                       b"Content-Type: image/jpeg\r\n\r\n" +
                       frame +
                       b"\r\n")
            time.sleep(0.03)

    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
