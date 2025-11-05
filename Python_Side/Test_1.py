import time, sys, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GEN_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'generated')

sys.path.insert(0, os.path.join(GEN_DIR, 'python'))

from MAVLinkConnection.MAVLink import MAVLinkConnection

# Configuration
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 57600
SYSTEM_ID = 1
COMPONENT_ID = 1

sentTime = 0.0

def create_connection():
    print(f"Connecting to {SERIAL_PORT} at {BAUD_RATE} baud...")
    
    conn = MAVLinkConnection(SERIAL_PORT, BAUD_RATE, SYSTEM_ID, COMPONENT_ID)
    conn.wait_heartbeat(timeout=5.0)
    
    return conn

def send_data_block(conn, msg_id, value):
    conn.send_data_block(msg_id, value)
    print(f"\n>>\nSent DATA_BLOCK: id={msg_id}, value={value:.2f}")

def receive_heartbeat(msg):
    pass
    # print(f"Received heartbeat from system {msg.get_srcSystem()}, component {msg.get_srcComponent()}")

def receive(msg, msg_type):
    if(msg_type == "DATA_BLOCK"):
        print(f"Recv DATA_BLOCK: id={msg.id}, value={msg.value}")
        print(f"<< Latency: {(time.time() - sentTime)*500:.2f} ms")

if __name__ == "__main__":
    try:
        conn : MAVLinkConnection = create_connection()
        conn.bind_receive_event(receive)
        conn.bind_receive_event(receive_heartbeat, "HEARTBEAT")
        
        counter = 0.0
        
        while True:
            sentTime = time.time()
            send_data_block(conn, 42, counter)
            time.sleep(1)
            counter += 1.5
        
    except Exception as e:
        print(f"Error: {e}")