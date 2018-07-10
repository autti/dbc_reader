#!/usr/bin/python

import cantools
import rospy
import can
import math

from common import RADAR_FILE, INTERFACE, CHANNEL
from sensor_msgs.msg import PointCloud
from geometry_msgs.msg import Point
from std_msgs.msg import Header

# can configuration

can.rc['interface'] = INTERFACE
can.rc['channel'] = CHANNEL

class RadarReader:
      def __init__(self, dbc_file):
            rospy.init_node('RadarReader', anonymous=True)
            self._dbc = cantools.db.load_file(dbc_file)
            self._can_bus = can.interface.Bus()
            print self._dbc.messages
            self._radar_pub = rospy.Publisher('radar', PointCloud, queue_size=20)

            self._point_cloud = PointCloud()
            self._point_cloud.header = Header()
            self._point_cloud.header.frame_id = 'map'
            self._point_cloud.points = [Point(i + 1, i + 1, 0) for i in xrange(len(self._dbc.messages))]

      def show_data(self):
            data = self._can_bus.recv()
            message_name = self._dbc._find_message_by_frame_id(data.arbitration_id)
            if message_name is not None:
                  print "radar info", message_name.name
                  message_number = int(message_name.name.split('_')[1])
                  output = self._dbc.decode_message(data.arbitration_id, data.data)
                  print output['X_Rel'], output['X_Rel'] * output['Angle'] * math.pi / 180.
                  self._point_cloud.points[message_number] = Point(output['X_Rel'], output['X_Rel'] * output['Angle'] * math.pi / 180., 0)
                  self._point_cloud.header.stamp = rospy.Time.now()
                  self._radar_pub.publish(self._point_cloud)
                  
if __name__ == '__main__':
      reader = RadarReader(RADAR_FILE)
      while not rospy.is_shutdown():
            reader.show_data()  