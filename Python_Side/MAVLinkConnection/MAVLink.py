import time, sys, os
from serial import Serial
from threading import Thread

import mt_mav

from serial import Serial

class MAVLinkConnection:
    """Wrapper class to handle MAVLink communication with custom dialect"""
    
    def __init__(self, serial_port, baud_rate, system_id=1, component_id=1):
        self.ser = Serial(serial_port, baud_rate, timeout=1)
        self.mav = mt_mav.MAVLink(self.ser, srcSystem=system_id, srcComponent=component_id)
        
        self.receive_event = None
        self.receive_event_type = {}
        
        self.receive_thread = Thread(target=self.receive_message_loop)
        self.receive_thread.daemon = True
        self.receive_thread.start()
    
    def bind_receive_event(self, event, _type=None):
        """Bind an event handler for received messages"""
        if(_type is None):
            self.receive_event = event
        else:
            print(f"Binding event for message type: {_type}")
            self.receive_event_type[_type] = event

    def send_data_block(self, msg_id, value):
        """Send a DATA_BLOCK message"""
        self.mav.data_block_send(msg_id, value)
        
    def receive_message(self, timeout=0.1):
        """Receive and parse messages"""
        start_time = time.time()
        
        while True:
            # Check timeout
            if time.time() - start_time > timeout:
                return None
            
            # Check if data is available
            if self.ser.in_waiting > 0:
                try:
                    # Parse incoming bytes
                    msg = self.mav.parse_char(self.ser.read(1))
                    if msg:
                        return msg
                except Exception as e:
                    # Continue parsing on error
                    pass
            else:
                time.sleep(0.001)  # Small delay to prevent busy waiting
                
        return None
    
    def receive_message_loop(self):
        """Receive and process messages"""
        try:
            while True:
                msg = self.receive_message(timeout=0.1)

                if msg:
                    msg_type = msg.get_type()
                    
                    if(msg_type == "BAD_DATA"):
                        continue
                    
                    if(self.receive_event is not None):
                        self.receive_event(msg, msg_type)
                    
                    if(msg_type in self.receive_event_type):
                        self.receive_event_type[msg_type](msg)
        except Exception as e:
            print(f"Error in receive_message_loop: {e}")

    def wait_heartbeat(self, timeout=5.0):
        """Wait for a heartbeat message"""
        print("Waiting for heartbeat...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            msg = self.receive_message(timeout=0.1)
            if msg and msg.get_type() == 'HEARTBEAT':
                print(f"Heartbeat received from system {msg.get_srcSystem()}, component {msg.get_srcComponent()}")
                return True
        
        print("Warning: No heartbeat received")
        return False
    
    def close(self):
        """Close the serial connection"""
        self.ser.close()