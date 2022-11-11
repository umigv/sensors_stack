sudo cp ./51-garmin.rules /etc/udev/rules.d/51-garmin.rules
sudo udevadm control --reload-rules && sudo udevadm trigger
