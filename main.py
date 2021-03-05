from utils.initGui import GUI
import sys, os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

cur_path = sys.path[0]
# cur_path = ROOT_DIR
gui = GUI(cur_path)
gui.start()