#! /usr/bin/env python3

# adapted from https://github.com/chriswsuarez/garmin18x_usb/blob/master/src/ros_stream.py

import sys
import os
import math
import rospy
from sensor_msgs.msg import NavSatFix

sys.path.append(os.path.dirname(os.path.dirname(
    os.path.realpath(__file__))) + "/pygarmin")
import garmin

class GarminGPS:

    def __init__(self):
        self.pub_topic = rospy.get_param("pub_topic", "/gps/fix")
        self.frame_id = rospy.get_param("frame_id", "gps")
        pub_rate = rospy.get_param("pub_rate", 1.0)
        port = rospy.get_param("port", "/dev/garmin_gps")

        self.fix = NavSatFix()
        self.fix_pub = rospy.Publisher(self.pub_topic, NavSatFix, queue_size=1)
        self.rate = rospy.Rate(pub_rate)

        phys = garmin.SerialLink(port)
        self.gps = garmin.Garmin(phys)
        self.gps.pvtOn()
    
    def run(self):
        while not rospy.is_shutdown():
            data = self.gps.getPvt()
            lat = data.rlat * 180 / math.pi
            lon = data.rlon * 180 / math.pi

            if abs(int(lat * 1e10) - int(self.fix.latitude * 1e10)) > 0 and abs(int(lon * 1e10) - int(self.fix.latitude * 1e10)) > 0 and abs(int(data.alt * 1e10) - int(self.fix.altitude * 1e10)) > 0:
                self.fix.status.status = 1
            else:
                self.fix.status.status = 0

            self.fix.header.stamp = rospy.Time.now()
            self.fix.header.frame_id = self.frame_id
            self.fix.status.service = 1
            self.fix.latitude = lat
            self.fix.longitude = lon
            self.fix.altitude = data.alt
            self.fix.position_covariance = [0] * 9
            self.fix.position_covariance_type = 0

            self.fix_pub.publish(self.fix)

            self.gps.getPvt()
            self.rate.sleep()

if __name__ == '__main__':
    rospy.init_node('garmin_gps')

    try:
        garmin_gps = GarminGPS()
        garmin_gps.run()
    except rospy.ROSInterruptException:
        pass