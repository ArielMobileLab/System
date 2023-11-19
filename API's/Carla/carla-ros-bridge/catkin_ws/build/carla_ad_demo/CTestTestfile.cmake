# CMake generated Testfile for 
# Source directory: /home/omer/carla-ros-bridge/catkin_ws/src/ros-bridge/carla_ad_demo
# Build directory: /home/omer/carla-ros-bridge/catkin_ws/build/carla_ad_demo
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(_ctest_carla_ad_demo_roslaunch-check_launch "/home/omer/carla-ros-bridge/catkin_ws/build/carla_ad_demo/catkin_generated/env_cached.sh" "/usr/bin/python2" "/opt/ros/melodic/share/catkin/cmake/test/run_tests.py" "/home/omer/carla-ros-bridge/catkin_ws/build/carla_ad_demo/test_results/carla_ad_demo/roslaunch-check_launch.xml" "--return-code" "/usr/bin/cmake -E make_directory /home/omer/carla-ros-bridge/catkin_ws/build/carla_ad_demo/test_results/carla_ad_demo" "/opt/ros/melodic/share/roslaunch/cmake/../scripts/roslaunch-check -o \"/home/omer/carla-ros-bridge/catkin_ws/build/carla_ad_demo/test_results/carla_ad_demo/roslaunch-check_launch.xml\" \"/home/omer/carla-ros-bridge/catkin_ws/src/ros-bridge/carla_ad_demo/launch\" ")
subdirs("gtest")
