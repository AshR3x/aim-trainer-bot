from mss import MSS
import time
import os
from pathlib import Path
import webbrowser
def open_game():
    webbrowser.open_new(url='https://humanbenchmark.com/tests/aim')
open_game()
def make_dir():
    try:
        folder = Path(__file__).resolve().parent / "Screen_cap"
        folder.mkdir(exist_ok=True)
        os.chdir(folder)
    except:
        return

make_dir()
for i in range(0,60):
    time.sleep(0.5)
    with MSS() as sct:
        sct.shot(output=f"Frame{i}.png")
