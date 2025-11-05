# MAVLink Experiments
This is an experiment using mavlink protocol to communicate between python and Arduino. For this experiment, I used a XIAO ESP32-C6.

`MAVLink`, or `Micro Air Vehicle Link` is a lightweight, open-source communication protocol for unmanned systems like drones and robots. It defines a set of messages for exchanging information between a vehicle and a ground control station, allowing for telemetry, control, and command transmission. MAVLink is used in major autopilot systems like ArduPilot and PX4 and is designed to work efficiently over unreliable, low-bandwidth links.

Here, I tried to create my own custom message type and use it to send and receive data from the ESP32 and a python script. You can also create your own message type by simply add an xml file in the `/descriptions` directory and running the `generate.sh` bash script. This will create the necessary python and c headers. Then upload the arduino code to your microcontroller and run the python test file.

## Usage
Step 1:
Clone this repo:
```
git clone https://github.com/A-N-M-Noor/mavlink-experiment.git
```

Step 2:
Install necessary packages:
```
pip3 install -r requirements.txt
```

Step 3:
Upload the arduino code from
```
/Arduino_Side/Arduino_Side.ino
```

Step 4:
Run the python file from 
```
/Python_Side/Test_1.py
```

## Result

I was successful in establishing a mavlink connection between the esp32 and python script. The custom message - DATA_BLOCK, has two fields: id and value.

The current code works like this:

1. The python script sends a DATA_BLOCK with id 42 and a count value.
2. The MCU receives the packet and sends back a value with the same id and a value of count+1.
3. Python script reveives the packet and calculates the latency.

The typical latency is around 1 to 2 milliseconds which is pretty impressive.