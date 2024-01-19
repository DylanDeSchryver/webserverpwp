# from movement import *
from camera import *
from flask import Flask, request, jsonify, Response

app = Flask(__name__)


@app.route('/')
def index():
    return 'ClosedAI'


@app.route('/move', methods=['POST'])
def move_robot():

    global robot_state

    data = request.get_json()
    direction = data.get('direction')
    if direction == 'forward':
        move_forward()
    elif direction == 'backward':
        move_backward()
    elif direction == 'left':
        turn_left()
    elif direction == 'right':
        turn_right()
    elif direction == 'stop':
        stop_robot()
    elif direction == 'play':
        play_course()
    return jsonify({'message': f"Robot is now {robot_state}"})


@app.route('/overlay')
def get_overlay_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/cam')
def get_camera_feed():
    return Response(cam(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4200)
