import sys
from utils.initGui import GUI

cur_path = sys.path[0]
gui = GUI(cur_path)
gui.start()