from ultralytics import YOLO

model = YOLO("./yolov8n.pt")  # 加载预训练模型（建议用于训练）

if __name__ == '__main__':
    # 单GPU训练
    model.train(data="./dataset/mydata.yaml",epochs=5)  # 训练模型
    # 多GPU训练
    #results = model.train(data="coco8.yaml", epochs=5, imgsz=640, device=[0, 1])
    metrics = model.val()  # 在验证集上评估模型性能
    results = model("./dataset/images/test/ripeimg_2.jpg")  # 对图像进行预测
    # Process results list
    for result in results:
      result.show()  # display to screen
