#!/usr/bin/python

import cantools
import rospy
import can

from pprint import pprint
from std_msgs.msg import Float32, String
from common import DATA_FILE, INTERFACE, CHANNEL

# can configuration

can.rc['interface'] = INTERFACE
can.rc['channel'] = CHANNEL

string_messages = set(['Cruise_State', 'Lkas_Action', 'Lkas_Alert', 'LaActAvail_D_Actl', 'Lines_Hud'])

class DataReader:
    def __init__(self, dbc_file):
        rospy.init_node('DataReader', anonymous=True)
        self._dbc = cantools.db.load_file(dbc_file)
        self._can_bus = can.interface.Bus()
        self._publishers = {}
        print self._dbc._messages
        for message in self._dbc._messages:
            message_name = message.name
            for signal in message.signals:
                complete_name = message_name + "/" + signal.name
                current_type = Float32 if signal.name not in string_messages else String
                self._publishers[complete_name] = rospy.Publisher(complete_name, current_type, queue_size=20)

    def recv_message(self):
        message = self._can_bus.recv()
        if self._dbc._find_message_by_frame_id(message.arbitration_id) is not None:
            message_name = self._dbc._find_message_by_frame_id(message.arbitration_id).name
            output = self._dbc.decode_message(message.arbitration_id, message.data)
            for key in output:
                signal_name = key
                value_output = output[key]
                # print key, value_output
                full_name = message_name + "/" + signal_name
                self._publishers[full_name].publish(value_output)

if __name__ == '__main__':
    reader = DataReader(DATA_FILE)
    while not rospy.is_shutdown():
        reader.recv_message()
