import time

from hqyj_mqtt import MQTTClient


# 链接mqtt服务器
mqtt_client = MQTTClient('127.0.0.1', 21883, 'bb', 'aa', 3000)

# 传送带运行
mqtt_client.control_device('conveyor', 'run')
time.sleep(1)


# 控制一号推杆
mqtt_client.control_device("rod_control", "first_push")
time.sleep(1)
mqtt_client.control_device("rod_control", "first_pull")
time.sleep(1)

while True:
    on_off = int(input("请输入0/1 (0结束，1继续)?"))
    if on_off == 0:
        break
    elif on_off == 1:
        # 控制一号推杆
        mqtt_client.control_device("rod_control", "first_push")
        time.sleep(1)
        mqtt_client.control_device("rod_control", "first_pull")
        time.sleep(1)
    else:
        pass


# 传送带停止
mqtt_client.control_device('conveyor', 'stop')
time.sleep(1)