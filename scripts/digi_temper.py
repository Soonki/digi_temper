#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Temperature

import usb # 1.0 not 0.4
from arduino.usbdevice import ArduinoUsbDevice
from cStringIO import StringIO
import json

class DigisparkTemperature():
    def __init__(self):
        try:
            self.device = ArduinoUsbDevice(idVendor=0x16c0, idProduct=0x05df)
        except:
            raise rospy.ROSException("No DigiUSB Device Found")

        rospy.init_node('temperature_sensor_publisher')

        self.pub = rospy.Publisher('temp', Temperature, queue_size=50)
        self.rate = 1.0

    def handle(self):

        self.device.write(ord('\n'))
        temp = Temperature()
        temp.header.stamp = self.current_time
        temp.header.frame_id = 'temp_frame'

        buf = StringIO()
        while True:
            try:
                c = chr(self.device.read())
                if c == '\n':
                    break
                buf.write(c)
            except Exception:
                continue

        try:
            rospy.loginfo(buf.getvalue())
            v = json.loads(buf.getvalue())
            temp.temperature = v['temp']
        except ValueError as e:
            rospy.loginfo(e)
            return
        except Exception as e:
            rospy.logerror(e)
            return

        self.pub.publish(temp)

    def spin(self):
        r = rospy.Rate(self.rate)
        while not rospy.is_shutdown():
            self.current_time = rospy.Time.now()
            self.handle()
            r.sleep()

if __name__ == '__main__':
                                
    sensor = DigisparkTemperature()
    rospy.loginfo("=== run")
    sensor.spin()
    rospy.loginfo("=== end")
