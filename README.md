# Python Code For Raspberry Pi

## Setup

* For LEDs:
  * Set LightCount to the number of LEDs
  * Choose message or rotate
  * Change delay, to balance LED animations
* RIO coms:
  * use `pip3 install` with all necessary imports
  * enable i2c bus in the settings

### Running program as a linux service

1. Open a terminal in the project folder
2. `sudo ln -s $(pwd)/led1038.service /lib/systemd/system/led1038.service`
3. `sudo ln -s $(pwd)/hub1038.service /lib/systemd/system/hub1038.service`
4. `sudo systemctl daemon-reload`
5. `sudo systemctl enable led1038`
6. `sudo systemctl enable hub1038`
7. Restart the pi

## Troubleshooting

### Lasers

* If you get errorno 121, check wiring
* Add pins connected to laser XSHUT pins to commented list

## Known Issues

* If lasers are in use, you have to power-cycle the pi to restart the hub program
