from ultralytics import YOLO # 导入YOLO模型库
from hqyj_mqtt import MQTTClient # 导入自定义的MQTT客户端模块
import base64 # 导入base64模块，用于解码图像数据
import threading # 导入线程模块，用于并行处理任务
import queue # 导入队列模块，用于线程间的数据传递
import time # 导入时间模块，用于控制时间间隔
import cv2 # 导入OpenCV库，用于图像处理
import numpy as np # 导入NumPy库，用于数值计算

speed = 1 #设置传送带速度

# 定义控制传送带的函数
def conveyor_Ctrl():
    while True:
        mqtt_client.control_device('rod_control', 'first_push') # 控制推杆进行第一次推送
        time.sleep(speed) # 等待指定的时间间隔 16
        mqtt_client.control_device('rod_control', 'first_pull') # 控制推杆进行第一次拉回
        time.sleep(0.5) # 等待0.5秒

# 客户端连接服务器的配置参数
ip_broker = '127.0.0.1' # MQTT服务器的IP地址
port_broker = 21883 # MQTT服务器的端口号
topic_sub = 'bb' # 订阅的MQTT主题
topic_pub = 'aa' # 发布的MQTT主题
TimeOutSec = 60 # 连接超时时间（秒）

# 加载预训练的YOLO模型
model = YOLO("./model/last.pt")

# 创建MQTT客户端实例
mqtt_client = MQTTClient(ip_broker, port_broker, topic_sub, topic_pub, TimeOutSec)

# 控制传送带开始运行
mqtt_client.control_device('conveyor', 'run')

# 创建控制传送带的线程
t_conveyor_data = threading.Thread(target=conveyor_Ctrl)
t_conveyor_data.start() # 启动线程

# 创建两个队列，用于存储分类结果和控制信号
cls_queue = queue.Queue()
switch2_queue = queue.Queue()

# 创建弟弟三个队列
switch3_queue = queue.Queue()


# 定义控制第二个推杆拉回的函数
def pullswich1():
    mqtt_client.control_device('rod_control', 'second_pull')

# 定义控制第三个推杆拉回的函数
def pullswich2():
    mqtt_client.control_device('rod_control', 'third_pull')

# 定义控制第四个推杆拉回的函数
def pullswich3():
    mqtt_client.control_device('rod_control', 'fourth_pull')

# 主循环，处理MQTT消息
while True:
    json_msg = mqtt_client.mqtt_queue.get() # 从MQTT队列中获取消息
    if 'image' in json_msg:
        # 将Base64编码的图像数据解码为二进制数据
        image_data = base64.b64decode(json_msg['image'])
        # 将二进制数据转换为numpy数组
        image_array = np.frombuffer(image_data, np.uint8)
        # 将numpy数组转换为OpenCV图像对象
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
         # 使用YOLO模型进行图像预测
        results = model.predict(image, imgsz=640)
        for result in results:
            cls = result.boxes.cls # 获取预测结果中的类别信息
            if cls.numel() != 0: # 如果检测到目标
                cls_queue.put(int(cls[0])) # 将检测到的类别放入队列
                print(cls) # 打印类别信息

    # 处理第一个开关的状态
    if 'first_switch' in json_msg:
        switch = json_msg['first_switch']
        if not switch: # 如果开关状态为关闭
            cls = cls_queue.get() # 从队列中获取类别信息
            if cls is None: # 如果类别信息为空
                pass # 不执行任何操作
            else:
                if cls == 0: # 如果类别为0
                    mqtt_client.control_device('rod_control', 'second_push') # 控制第二个推杆进行推送

                    threading.Timer(0.5, pullswich1).start() # 延迟0.5秒后执行拉回操作
                else:
                    switch2_queue.put(cls) # 将类别信息放入第二个队列

    # 处理第二个开关的状态
    elif 'second_switch' in json_msg:
        switch = json_msg['second_switch']
        if not switch: # 如果开关状态为关闭
            cls = switch2_queue.get() # 从第二个队列中获取类别信息
            if cls is None: # 如果类别信息为空
                pass # 不执行任何操作
            else:
                if cls == 1: # 如果类别为1
                    mqtt_client.control_device('rod_control', 'third_push') # 控制第三个推杆进行推送

                    threading.Timer(0.5, pullswich2).start() # 延迟0.5秒后执行拉回操作
                else:
                    # 如果类别不是2，将类别信息放入第三个栈
                    pass


