from flask import Flask, request, jsonify, Response
from adafruit_motorkit import MotorKit
import time



# Initialize the MotorKit
kit = MotorKit(0x40)

# Create a dictionary to store the robot's current state eg. stopped
robot_state = "stopped"


#Define movement functions
def move_forward():
    kit.motor1.throttle = 0.77
    kit.motor2.throttle = 0.73
    robot_state = "moving forward"


def move_backward():
    kit.motor1.throttle = -0.80
    kit.motor2.throttle = -0.76
    robot_state = "moving backward"


def turn_left():
    kit.motor1.throttle = 0.75
    kit.motor2.throttle = -0.75
    robot_state = "turning left"


def turn_right():
    kit.motor1.throttle = -0.76
    kit.motor2.throttle = 0.75
    robot_state = "turning right"


def stop_robot():
    kit.motor1.throttle = 0.0
    kit.motor2.throttle = 0.0
    robot_state = "stopped"


def play_course():
    move_forward()
    time.sleep(4.1)
    stop_robot()
    time.sleep(1)
    turn_left()
    time.sleep(0.9)
    stop_robot()
    time.sleep(1)
    move_forward()
    time.sleep(2.4)
    stop_robot()
    time.sleep(1)
    move_backward()
    time.sleep(4.6)
    stop_robot()
    time.sleep(1)
    move_forward()
    time.sleep(2.5)
    stop_robot()
    time.sleep(1)
    turn_right()
    time.sleep(1.8)
    stop_robot()
    time.sleep(1)
    move_backward()
    time.sleep(5)
    stop_robot()
    time.sleep(1)
    move_forward()
    time.sleep(5)
    stop_robot()
    time.sleep(1)
    turn_right()
    time.sleep(0.9)
    stop_robot()
    time.sleep(1)
    move_forward()
    time.sleep(2.87)
    stop_robot()
    time.sleep(1)
    move_backward()
    time.sleep(4)
    stop_robot()


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












