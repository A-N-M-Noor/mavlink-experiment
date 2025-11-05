#include "../generated/c/mt_mav/mt_mav/mavlink.h"

#define MAVLINK_SERIAL Serial
#define BAUD_RATE 57600
#define SYSTEM_ID 1
#define COMPONENT_ID 200

unsigned long last_heartbeat = 0;
unsigned long last_data_send = 0;
const unsigned long HEARTBEAT_INTERVAL = 100;

uint16_t data_counter = 0;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);

  MAVLINK_SERIAL.begin(BAUD_RATE);
  while (!MAVLINK_SERIAL){}

  delay(1000);
}

void loop() {
  unsigned long now = millis();

  if (now - last_heartbeat > HEARTBEAT_INTERVAL) {
    send_heartbeat();
    last_heartbeat = now;
  }

  receive_messages();
}

void send_heartbeat() {
  mavlink_message_t msg;
  uint8_t buf[MAVLINK_MAX_PACKET_LEN];

  mavlink_msg_heartbeat_pack(
    SYSTEM_ID,
    COMPONENT_ID,
    &msg,
    MAV_TYPE_GENERIC,
    MAV_AUTOPILOT_INVALID,
    MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    0,
    MAV_STATE_ACTIVE);

  uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
  MAVLINK_SERIAL.write(buf, len);
}

void send_data_block(uint16_t id, float value) {
  mavlink_message_t msg;
  uint8_t buf[MAVLINK_MAX_PACKET_LEN];

  mavlink_msg_data_block_pack(
    SYSTEM_ID,
    COMPONENT_ID,
    &msg,
    id,
    value);

  uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
  MAVLINK_SERIAL.write(buf, len);
}

void receive_messages() {
  mavlink_message_t msg;
  mavlink_status_t status;

  while (MAVLINK_SERIAL.available() > 0) {
    uint8_t c = MAVLINK_SERIAL.read();

    if (mavlink_parse_char(MAVLINK_COMM_0, c, &msg, &status)) {
      handle_message(&msg);
    }
  }
}

void handle_message(mavlink_message_t* msg) {
  switch (msg->msgid) {
    case MAVLINK_MSG_ID_DATA_BLOCK:
      {
        mavlink_data_block_t data;
        mavlink_msg_data_block_decode(msg, &data);
        send_data_block(data.id, data.value+1);

        digitalWrite(LED_BUILTIN, LOW);
        delay(250);
        digitalWrite(LED_BUILTIN, HIGH);
        break;
      }

    case MAVLINK_MSG_ID_HEARTBEAT:
      {
        break;
      }

    default:
      Serial.print("Received unknown message ID: ");
      Serial.println(msg->msgid);
      break;
  }
}