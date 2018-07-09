#!/usr/bin/python

import cantools
import rospy
import can
import os

from pprint import pprint

# can configuration

can.rc['interface'] = 'socketcan'
can.rc['channel'] = 'hs1'

# Constants
FILEPATH = os.path.dirname(os.path.realpath(__file__)) + '/'

class DBCReader:
    def __init__(self, dbc_file):
        rospy.init_node('DBCReader', anonymous=True)
        self._dbc = cantools.db.load_file(dbc_file)
        self._can_bus = can.interface.Bus()
        print self._dbc.messages

    def recv_message(self):
        message = self._can_bus.recv()
        if self._dbc._find_message_by_frame_id(message.arbitration_id) is not None:
            print self._dbc.decode_message(message.arbitration_id, message.data)

if __name__ == '__main__':
    reader = DBCReader(FILEPATH + '../dbc/ford_fusion_2018.dbc')
    while not rospy.is_shutdown():
        reader.recv_message()
