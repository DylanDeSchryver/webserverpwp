import cv2
import threading
import numpy as np
from flask import Flask, request, jsonify, Response

video = cv2.VideoCapture(0)


def generate_frames():
    while True:

        # get every frame of video
        ret, frame = video.read()
        # breaks if the video has ended
        if frame is None:
            break
        # duplicate the frame
        dup = frame.copy()

        # turns into grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # gaussian blur
        gray = cv2.GaussianBlur(gray, (15, 15), 0)
        # gets all the edges

        # finds the black areas
        darkmask = cv2.inRange(gray, 50, 100)
        # isolates the darker areas
        maskedimg = cv2.bitwise_and(gray, darkmask)
        maskedimg = cv2.Canny(maskedimg, 80, 150)

        # gets the  height and width of the frame
        height, width = maskedimg.shape
        # this makes a trapezoid
        mask = np.zeros_like(gray)
        # array showing the coordinates of the trapezoid
        trapezoid = np.array([[(0, height), (0, 75), (width, 75), (width, height)]])
        # creates plolygon
        mask = cv2.fillPoly(mask, trapezoid, 255)
        # adds the mask
        mask = cv2.bitwise_and(maskedimg, mask)

        # houghlines (gets a set of lines that are outlined in the masked image)
        lines = cv2.HoughLinesP(mask, 1, np.pi / 180, 50, maxLineGap=150)
        # lists for slopes and xy values for the endpoints of the lines
        # used to calculate midline
        xval = []
        yval = []
        xval2 = []
        yval2 = []
        # makes sure there are lines
        if lines is not None:
            for line in lines:
                # gets endpoints for line
                x1, y1, x2, y2 = line[0]
                # finds slope of line
                if (x1 - x2) != 0:
                    sloped = (y1 - y2) / (x1 - x2)
                else:
                    sloped = 99999999
                # if the line is close to being vertical it ignores the line
                if -0.1 < sloped < 0.1:
                    continue
                # isolates the slopes of the right line
                elif sloped > 0:
                    xval.append(x2)
                    yval.append(y2)
                    xval.append(x1)
                    yval.append(y1)
                # isolates the slopes of the left line
                else:
                    xval2.append(x2)
                    yval2.append(y2)
                    xval2.append(x1)
                    yval2.append(y1)
                # makes the lines

        # makes sure the lists aren't empty
        if yval != [] and xval != [] and xval2 != [] and yval2 != []:

            # finds average of the x values of the top two lines
            endpointrighttop = (int(min(xval)), int(min(yval)))
            endpointrightbottom = (int(max(xval)), int(max(yval)))
            endpointlefttop = (int(max(xval2)), int(min(yval2)))
            endpointleftbottom = (int(min(xval2)), int(max(yval2)))
            cv2.line(frame, endpointleftbottom, endpointlefttop, (180, 105, 255), 15)
            cv2.line(frame, endpointrightbottom, endpointrighttop, (180, 105, 255), 15)

            slopeleft = (endpointlefttop[1] - endpointleftbottom[1]) / (endpointlefttop[0] - endpointleftbottom[0])
            sloperight = (endpointrighttop[1] - endpointrightbottom[1]) / (endpointrighttop[0] - endpointrightbottom[0])
            if endpointrighttop[1] > endpointlefttop[1]:
                yvaltop = endpointlefttop[1]
                xvalmean = (endpointlefttop[0] + ((endpointlefttop[1] - endpointrightbottom[1]) / sloperight) +
                            endpointrightbottom[0]) / 2

            else:
                yvaltop = endpointrighttop[1]
                xvalmean = (endpointrighttop[0] + ((endpointrighttop[1] - endpointleftbottom[1]) / slopeleft) +
                            endpointleftbottom[0]) / 2

            if endpointrightbottom[1] > endpointleftbottom[1]:
                yvalbottom = endpointrightbottom[1]
                xvalmeanb = (endpointrightbottom[0] + endpointlefttop[0] - (
                            endpointlefttop[1] - endpointrightbottom[1]) / slopeleft) / 2

            else:
                yvalbottom = endpointleftbottom[1]
                xvalmeanb = (endpointleftbottom[0] + endpointrighttop[0] - (
                            endpointrighttop[1] - endpointleftbottom[1]) / sloperight) / 2
            ything = yvaltop
            xthing = xvalmean

            ything2 = yvalbottom

            # the ything variables find the max and min y values of the two side lines

            xthing2 = xvalmeanb

            if (xthing - xthing2) != 0 or (ything - ything2) != 0:
                slopedd = (ything - ything2) / (xthing - xthing2)
                finder = (height - ything2) / slopedd + xthing2
            else:
                finder = xthing2
            # uses slope of two lines to extend the middle line to the bottom of the frame
            cv2.line(frame, (int(xvalmean), int(yvaltop)), (int(finder), int(height)), (255, 0, 0), 3)
            # adds the line to the frame

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def cam():
    while True:

        # get every frame of video
        ret, frame = video.read()
        # breaks if the video has ended
        if frame is None:
            break
        # duplicate the frame
        dup = frame.copy()

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# Start a separate thread to continuously capture frames
threading.Thread(target=generate_frames, daemon=True).start(
)


def get_overlay_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def get_camera_feed():
    return Response(cam(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')