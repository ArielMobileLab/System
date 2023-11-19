execute_process(COMMAND "/home/omer/carla-ros-bridge/catkin_ws/build/carla_waypoint_publisher/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/omer/carla-ros-bridge/catkin_ws/build/carla_waypoint_publisher/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
