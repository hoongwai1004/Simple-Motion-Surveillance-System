from gpiozero import MotionSensor
from picamera import PiCamera
from datetime import datetime
from time import sleep
from subprocess import CalledProcessError
import subprocess
import os.path
import shlex

pir = MotionSensor(4)

camera = PiCamera()

camera.vflip = True
camera.hflip = True

print('good')

while True:
    pir.wait_for_motion()
    now = datetime.now()
    save_path = '/home/pi/Desktop/test2'
    save_path2 = '/home/pi/Desktop/test3'
    filename = '{0:%Y}-{0:%m}-{0:%d}-{0:%H}-{0:%M}-{0:%S}.h264'.format(now)
    completed_video = os.path.join(save_path, filename)
    print('Motion Detected')
    camera.start_recording(completed_video)
    sleep(5)
    pir.wait_for_no_motion()
    print('Motion Not Detected')
    camera.stop_recording()

    command = "MP4Box -add {} {}.mp4".format(completed_video, os.path.splitext(os.path.join(save_path2, filename))[0])
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        print('FAIL:\ncmd:{}\noutput:{}'.format(e.cmd, e.output))
