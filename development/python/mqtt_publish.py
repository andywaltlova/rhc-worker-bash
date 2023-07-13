#!/usr/bin/env python3
import json
import socket
import uuid
import paho.mqtt.client as mqtt

def get_ip_address():
  host_ip = ""
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80))
  host_ip = s.getsockname()[0]
  s.close()
  return host_ip

# This is changed everytime you refresh the box and register the machine again.
CLIENT_ID = "973afbce-19b4-4862-9d7a-6e9d8c410674"
BROKER = '127.0.0.1'
BROKER_PORT = 1883
TOPIC = f"yggdrasil/{CLIENT_ID}/data/in"

# NOTE: currently can be whatever you placed inside devleopment/nginx/data folder
SERVED_FILENAME = "yaml-file"

MESSAGE = {
  "type": "data",
  "message_id": str(uuid.uuid4()),
  "version": 1,
  "sent": "2021-01-12T14:58:13+00:00", # str(datetime.datetime.now().isoformat()),
  "directive": 'rhc-worker-bash',
  "content": f'http://{get_ip_address()}:8000/data/{SERVED_FILENAME}',
  "metadata": {
      "correlation_id": "00000000-0000-0000-0000-000000000000",
      "return_url": f'http://{get_ip_address()}:8000/api/ingress/v1/upload',
      "return_content_type": "application/vnd.redhat.tasks.filename+tgz"
  }
}


def main():
  client = mqtt.Client()
  client.connect(BROKER, BROKER_PORT, 60)
  client.publish(TOPIC, json.dumps(MESSAGE), 1, False)
  print("Published message to MQTT, serving content.")


if __name__ == "__main__":
   main()
