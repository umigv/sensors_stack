#!/bin/bash
#
# Script to configure network for velodyne connection
#
# Colin Yoon
# February 6, 2022
#
# Use: ./config_velodyne_connection.sh

# sudo ifconfig eno1 192.168.191.2
sudo ifconfig enp48s0 192.168.191.1
# sudo route add 192.168.191.254 eno1
sudo route add 192.168.191.254 enp48s0
