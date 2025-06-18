# 该代码的功能是通过MQTT协议接收采集到的图像数据，并将接收到的图像保存到指定的文件夹中
import os # 用于操作文件,目录
from hqyj_mqtt import MQTTClient
import threading # 线程
import base64 # 转码
import numpy as np
import cv2       # opencv-python


RAW_DATA_FOLDER = './dataset/raw' # 不熟
RIPE_DATA_FOLDER = './dataset/ripe' # 成熟
HALF_DATA_FOLDER = './dataset/half-ripe' #半生不熟
PICTURE_DATA_FOLDER = './dataset/picture'#全部图片



# 获取图片数据类
class GetData:
    # 构造函数
    def __init__(self, ip_broker, port, sub, pub, time_out, folder_path):
        # 实例化客户端
        self.mqtt_client = MQTTClient(ip_broker, port, sub, pub, time_out)
        # 文件夹路径
        self.folder_path = folder_path
        # 创建文件夹
        self.make_dir(self.folder_path)
        # 启动一个线程来接收数据
        self.t_recv_data = threading.Thread(target=self.recv_data)
        self.t_recv_data.start()

    # 接收3D图片数据
    def recv_data(self):
        i = 0
        while True:
            # 获取3D场景传输的数据
            image_base64 = self.mqtt_client.mqtt_queue.get()
            # 如果获取的是图像数据
            if 'image' in image_base64:
                # 将 Base64 编码的字符串解码为原始二进制数据。
                print(image_base64)
                image_data = base64.b64decode(image_base64['image'])
                # 将二进制数据转换为一个 np.uint8 类型的 NumPy 数组。
                image_array = np.frombuffer(image_data, np.uint8)
                # 将 NumPy 数组解码为 OpenCV 图像对象
                image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                cv2.imwrite(self.folder_path + '/' + f'img_{i+1}.jpg', image)
                print(f'图片_{i+1}已保存')
                i += 1

    # 检查指定的文件夹是否存在，如果不存在则创建它
    @staticmethod
    def make_dir(folder_path):
        if not os.path.exists(folder_path):
            print(f'{folder_path}不存在')
            os.makedirs(folder_path)
            print(f'{folder_path}已创建')
        else:
            print(f'{folder_path}已存在，无需创建')


get_data = GetData('127.0.0.1', 21883, 'bb', 'aa', 60, HALF_DATA_FOLDER)