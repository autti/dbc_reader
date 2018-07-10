import os

INTERFACE = "socketcan"
CHANNEL = "hs1"

PATH = os.path.dirname(os.path.realpath(__file__)) + '/'
DATA_FILE = PATH + '../dbc/data_ff_2018.dbc'
RADAR_FILE = PATH + '../dbc/radar_ff_2018.dbc'