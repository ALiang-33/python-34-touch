import time

from hqyj_mqtt import MQTTClient


# 链接mqtt服务器
mqtt_client = MQTTClient('127.0.0.1', 21883, 'bb', 'aa', 3000)

# 传送带运行
mqtt_client.control_device('conveyor', 'run')
time.sleep(3)

mqtt_client.control_device("rod_control", "first_push")
time.sleep(0.5)
mqtt_client.control_device("rod_control", "first_pull")
time.sleep(0.5)

while True:
    json_msg = mqtt_client.mqtt_queue.get()

    if 'first_switch' in json_msg:

        if json_msg['first_switch']:
            print("检测到货物")

            time.sleep(0.8)
            mqtt_client.control_device("rod_control", "second_push")
            time.sleep(0.5)
            mqtt_client.control_device("rod_control", "second_pull")
            time.sleep(0.5)

            print("已退出")
            break
        else:
            break


mqtt_client.control_device('conveyor', 'stop')