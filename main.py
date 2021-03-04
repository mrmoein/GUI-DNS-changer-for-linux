from utils.initGui import GUI
import os
from utils.data import Data

cur_path = os.path.dirname(__file__)
gui = GUI(cur_path)
gui.start()

# data = Data('{}/utils/data.json'.format(cur_path))
# print(data.data['dns_list'][0]['name'])