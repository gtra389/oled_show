#!/bin/bash

sleep 5
sudo python /home/pi/oled_show/oledTest
while :
do
  if [ `ps -U root -u root u | grep python | wc -m` -eq 0 ]
  then 
    sudo python sudo python /home/pi/oled_show/oledTest
    sleep 180
  else
    sleep 180
  fi
done
