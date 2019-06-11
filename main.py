from umqtt.simple import MQTTClient
import ubinascii
import machine
import credentials
import time

relay = machine.Pin(0)

# this consumes 200 mA when on and 70 mA when off

def relay_on():
 relay.off()

def relay_off():
 relay.on()

def sub_cb(topic, msg):
  # print((topic, msg))
  if msg == b'1':
    relay_on()
  if msg == b'0':
    relay_off()

def connect_and_subscribe():
  client_id = ubinascii.hexlify(machine.unique_id())
  mqtt_server = credentials.mqtt_server
  topic_sub = credentials.topic
  client = MQTTClient(client_id, mqtt_server)
  client.user = credentials.user
  client.pswd = credentials.pswd
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

while True:
  try:
    new_message = client.check_msg()
    if new_message != None:
      client.publish(credentials.topic, b'received')
    time.sleep(1)
  except OSError as e:
    restart_and_reconnect()
