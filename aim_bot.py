from pathlib import Path
import webbrowser
from mss import MSS
from ultralytics import YOLO
import pyautogui
import time
import numpy
import vlc

BASE = Path(__file__).resolve().parent
p = vlc.MediaPlayer(str(BASE / "osu-hit-sound.mp3"))
pyautogui.PAUSE = 0
model = YOLO(str(BASE / "best.pt"))
hits=0
def open_in_browser():
    webbrowser.open_new(url='https://humanbenchmark.com/tests/aim')
    time.sleep(5)
# accepts all formats - image/dir/Path/URL/video/PIL/ndarray. 0 for webcam

def grab_frame(sct):
    shot = sct.grab(sct.monitors[1])   # monitor 1 = your main screen
    frame = numpy.array(shot)          # raw pixels -> NumPy array (BGRA)
    return frame[:, :, :3]             # keep first 3 channels -> BGR

def find_target(frame):
    results = model.predict(frame, verbose=False)
    coords = results[0].boxes.xywh.tolist()
    if not coords:
        return None
    x = round(coords[0][0])
    y = round(coords[0][1])
    return x, y

def clicker(x,y):
    pyautogui.click(x,y)
    time.sleep(0.1)
open_in_browser()
with MSS() as sct:
    while hits<31:

        frame = grab_frame(sct)
        target = find_target(frame)
        if target:
            clicker(*target)
            p.play()
            hits=hits+1
