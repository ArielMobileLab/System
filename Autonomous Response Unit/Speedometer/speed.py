#!/usr/bin/env python
# Speed meter for all scripts
import rospy
from sensor_msgs.msg import NavSatFix
import os
import sys
from PyQt5.QtGui import QGuiApplication, QScreen
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication
import signal
#from carla_msgs.msg import CarlaEgoVehicleStatus
from std_msgs.msg import Float32, Int8, Float64, Float32
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication


rospy.init_node("speedometer")


class fonts:  # works only for print() function
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'


def callback(msg):

    #speed = msg.velocity
    #speed = msg.altitude
    #print(msg)
    #print(speed)
    
    #window.ui.widget.updateValue(round(speed * 3.6, 1))
    window.ui.widget.updateValue(msg.data* 3.6)
    # print(fonts.RED + str(round(speed * 3.6, 1)) + " km/h")


################################################################################################
# Convert UI to PyQt5 py file
################################################################################################
os.system("pyuic5 -o analoggaugewidget_demo_ui.py analoggaugewidget_demo.ui")
# os.system("pyuic5 -o analoggaugewidget_demo_ui.py analoggaugewidget_demo.ui.oQCkCR")

################################################################################################
# Import the generated UI
################################################################################################
from analoggaugewidget_demo_ui import *


################################################################################################
# MAIN WINDOW CLASS
################################################################################################
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        ################################################################################################
        # Setup the UI main window
        ################################################################################################
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        #self.ui.widget.setStyleSheet("background-color: #F5F5F5;")  # Show window on second screen at the bottom left
        ################################################################################################
        screen = QGuiApplication.screens()[0]  # secound screen
        screen_geometry = screen.geometry()
        window_width, window_height = 300, 300  # dimensions of the window
        x = screen_geometry.center().x() - window_width / 2  # x-coordinate of the top-left corner at the bottom middle
        y = screen_geometry.bottom() - window_height  # y-coordinate of the top-left corner at the bottom of the screen
        self.setGeometry(x, y, window_width, window_height)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

	    
        ################################################################################################
        # Show window
        ################################################################################################
        self.show()


def signal_handler(signal, frame):
    # Close the window
    window.close()
    # Exit the application
    sys.exit(0)

#Get a signal form Adaptive traning to close the speedometer
signal.signal(signal.SIGUSR1, signal_handler)
sub = rospy.Subscriber("/carla/ego_vehicle/speedometer", Float32, callback, queue_size=10)
#sub =rospy.Subscriber("/carla/ego_vehicle/gnss",NavSatFix,GPS,queue_size=1)

app = QApplication(sys.argv)
########################################################################
##
########################################################################
window = MainWindow()
window.show()
sys.exit(app.exec_())

rospy.spin()
