# 将data转为yolo格式的dataset目录格式
import os
# from ultralytics import YOLO
# 创建dataset目录
os.makedirs('dataset',exist_ok=True)
# 创建标签目录
os.makedirs('./dataset/labels',exist_ok=True)
# 创建照片目录
os.makedirs('./dataset/images',exist_ok=True)

# 创建标签目录验证集、训练集、测试集
os.makedirs('./dataset/labels/valid',exist_ok=True)
os.makedirs('./dataset/labels/train',exist_ok=True)
os.makedirs('./dataset/labels/test',exist_ok=True)

# 创建img目录验证集、训练集、测试集
os.makedirs('./dataset/images/valid',exist_ok=True)
os.makedirs('./dataset/images/train',exist_ok=True)
os.makedirs('./dataset/images/test',exist_ok=True)


# 定义每个数据集比例
train_ratio = 0.85
valid_ratio = 0.1
test_ratio = 0.05

# 获取目录的内容
files = os.listdir('./dataset/half-ripe/')

print(files)
jpg_files = []
for f in files:
    if f.endswith('.jpg'):
        jpg_files.append(f)


import random
# 打乱列表
random.shuffle(jpg_files)
# img数量
num_img = len(jpg_files)
num_train = num_img*train_ratio
num_valid = num_img*valid_ratio


print('img数量：',num_img)
print(jpg_files)

# 将文件复制到相应目录
""" 
 shutil.copy(原始路径，新路径) 
原始路径： ./data/data/xxx.jpg 
"""
import shutil

for i in range(num_img):
    # 获取原始图片和原始标签的路径
    image_path = os.path.join('./dataset/half-ripe',jpg_files[i])
    label_path = os.path.join('./dataset/half-ripe',jpg_files[i].replace('.jpg','.txt'))
    print(image_path)
    print(label_path)

    if i <num_train:
        dst_name = 'train'
        shutil.copy2(image_path, os.path.join('./dataset/images/train/', 'half-ripe'+ jpg_files[i]))
        shutil.copy2(label_path, os.path.join('./dataset/labels/train/', 'half-ripe'+ jpg_files[i].replace('.jpg','.txt')))
    elif i < num_train + num_valid:
        dst_name = 'valid'
        shutil.copy2(image_path, os.path.join('./dataset/images/valid/', 'half-ripe'+ jpg_files[i]))
        shutil.copy2(label_path, os.path.join('./dataset/labels/valid/', 'half-ripe'+ jpg_files[i].replace('.jpg','.txt')))
    else:
        dst_name = 'test'
        shutil.copy2(image_path, os.path.join('./dataset/images/test/', 'half-ripe'+ jpg_files[i]))
        shutil.copy2(label_path, os.path.join('./dataset/labels/test/', 'half-ripe'+ jpg_files[i].replace('.jpg','.txt')))
    # 将图片和标签复制到相应的daset目录中
    # 复制图片
    #shutil.copy(image_path,os.path.join('./dataset/images/',dst_name))
    # 复制标签
    #shutil.copy(label_path, os.path.join('./dataset/labels/', dst_name))