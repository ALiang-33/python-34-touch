import json
import paho.mqtt.client as mqtt
import queue


class MQTTClient():
    """
    用于表征Mqtt客户端的类
    :auth: 敦敦
    """

    def __init__(self, ip_broker, port_broker, topic_sub, topic_pub, time_out_secs):
        """
        :param ip_broker: broker的IP地址
        :param port_broker: 连接服务的端口
        :param topic_sub: 订阅话题
        :param topic_pub: 发布话题
        :param time_out_secs: 连接超时的时间
        """

        self.mqtt_clt = mqtt.Client()

        self.mqtt_clt.on_message = self.on_message       # 设置Mqtt客户端回调on_message为本类成员方法on_message

        self.msg = {}  # 信息字典
        self.topic_sub = topic_sub  # 设置订阅话题
        self.topic_pub = topic_pub  # 设置发布话题

        self.mqtt_queue = queue.Queue()
        self.mqtt_clt.connect(ip_broker, port_broker, time_out_secs)        # 链接Mqtt Broker
        self.mqtt_clt.subscribe(self.topic_sub, qos=0)      # 相关话题

        self.mqtt_clt.loop_start()      # 开启结束循环


    def __del__(self):
        # 结束接受循坏
        self.mqtt_clt.loop_forever()

        # 断开链接
        self.mqtt_clt.disconnect()

    def on_message(self, client, userdata, message):
        """
        :param client: 回调返回的客户端实例
        :param userdata: Client()或user_data_set()中设置的私有用户数据
        :param message: MQTTMessage实例,包含topic,payload,qos,retain
        :return: 接收消息的回调,提取消息中的相关内容
        """
        # pass
        self.mqtt_queue.put(json.loads(message.payload.decode()))
        # self.mqtt_queue.put(message.payload())

    def send_json_msg(self, msg):
        """
        :param msg: json 字段
        :return: 在指定的话题上发布信息
        """
        self.mqtt_clt.publish(self.topic_pub, payload="{}".format(msg))

    def control_device(self, str_key, str_value):
        """
        :param str_key: 键的字符串
        :param str_value: 值的字符串
        :return: 控制设备
        """
        self.send_json_msg(json.dumps(
            {
                str_key: str_value
            }
        ))
