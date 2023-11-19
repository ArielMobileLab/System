# CMake generated Testfile for 
# Source directory: /home/omer/carla-ros-bridge/catkin_ws/src/ros-bridge/carla_manual_control
# Build directory: /home/omer/carla-ros-bridge/catkin_ws/build/carla_manual_control
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(_ctest_carla_manual_control_roslaunch-check_launch "/home/omer/carla-ros-bridge/catkin_ws/build/carla_manual_control/catkin_generated/env_cached.sh" "/usr/bin/python2" "/opt/ros/melodic/share/catkin/cmake/test/run_tests.py" "/home/omer/carla-ros-bridge/catkin_ws/build/carla_manual_control/test_results/carla_manual_control/roslaunch-check_launch.xml" "--return-code" "/usr/bin/cmake -E make_directory /home/omer/carla-ros-bridge/catkin_ws/build/carla_manual_control/test_results/carla_manual_control" "/opt/ros/melodic/share/roslaunch/cmake/../scripts/roslaunch-check -o \"/home/omer/carla-ros-bridge/catkin_ws/build/carla_manual_control/test_results/carla_manual_control/roslaunch-check_launch.xml\" \"/home/omer/carla-ros-bridge/catkin_ws/src/ros-bridge/carla_manual_control/launch\" ")
subdirs("gtest")
