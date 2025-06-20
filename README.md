# python-34-touch
# Python实现3D场景通信控制与数据回传

## 项目简介

本项目实现了基于Python的3D场景通信控制与数据回传功能。主要目标是通过网络通信对3D场景进行实时控制，并将关键数据从场景回传给控制端，实现远程监控与交互。适用于虚拟现实、数字孪生、远程设备控制等应用场景。

## 功能特性

- 支持TCP/UDP/WebSocket等多种网络通信协议
- 可对3D场景中的对象进行实时控制（如移动、旋转、缩放等）
- 场景数据、状态和传感器信息实时回传
- 支持多端连接与通信
- 易于扩展和集成到主流3D引擎（如Unity、Unreal、Blender等）

## 主要模块

- `hqyj_mqtt.py`：网络通信模块，用于链接Mqtt客户端的类;包括3D场景控制逻辑，实现对对象的操作指令解析与执行
- `dataloader.py`：数据采集与回传模块，主要应用在3D场景控制逻辑中生成训练模型用的测试集
- `yolo_train.py`：测试集，基于yolov8的训练模型，对图像进行预测
- `getdata.py' : 测试集，测试将图片和标签复制到相应的daset目录中
- `mqtt*Demo`：示例脚本，展示典型的控制与回传流程
- `main.py': 主程序，运行应用并实现3d通行

## 环境依赖

- Python >= 3.8.1
- 常用依赖库（根据具体实现有所不同）：  
  - `paho-mqtt`
  - `numpy`
  - `ultralytics.YOLO`
  - `threading`
  - `opencv-python`  
  - 3D引擎相关Python包（如有）

安装依赖
```bash
pip install -r requirements.txt
```

## 使用说明

1. 启动通信服务端（或客户端）：

   ```bash
   python main.py
   ```

2. 运行3D场景并载入控制脚本

3. 控制端发送控制指令，3D场景端解析并执行

4. 3D场景端采集并回传状态数据

5. 控制端接收并处理回传数据

> 具体示例和详细步骤请参考`examples/`目录下的脚本和说明。

## 示例

```python
# 控制端示例
def __init__(self, ip_broker, port_broker, topic_sub, topic_pub, time_out_secs):
        self.mqtt_clt = mqtt.Client()

        self.mqtt_clt.on_message = self.on_message       # 设置Mqtt客户端回调on_message为本类成员方法on_message

        self.msg = {}  # 信息字典
        self.topic_sub = topic_sub  # 设置订阅话题
        self.topic_pub = topic_pub  # 设置发布话题

        self.mqtt_queue = queue.Queue()
        self.mqtt_clt.connect(ip_broker, port_broker, time_out_secs)        # 链接Mqtt Broker
        self.mqtt_clt.subscribe(self.topic_sub, qos=0)      # 相关话题

        self.mqtt_clt.loop_start()      # 开启结束循环
```

## 目录结构

```
.
├── getdata.py
├── dataloader.py
├── getdata.py
├── yolo_train.py
├── main.py
├── mqtt*Demo.py
├── requirements.txt
└── README.md
```

## 贡献与反馈

欢迎提交Issue或Pull Request进行建议与贡献。

## 许可协议

本项目采用 MIT License 进行开源，详见 [LICENSE](LICENSE) 文件。

