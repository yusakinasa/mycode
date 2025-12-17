import torch
from torchvision import transforms, models
from PIL import Image
import torch.nn as nn

def infer(img_path):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    # 1️⃣ 加载 VGG16 网络
    model = models.vgg16(weights=None)  # 不使用预训练权重
    model.classifier[6] = nn.Linear(4096, 2)  # 修改最后一层输出为2类
    model.load_state_dict(torch.load("checkpoints/vgg16_best.pth", map_location=device))
    model = model.to(device)
    model.eval()  # 切换到评估模式

    # 2️⃣ 图像预处理
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],  # VGG16 标准归一化
                             [0.229, 0.224, 0.225])
    ])

    img = Image.open(img_path).convert('RGB')
    img = transform(img).unsqueeze(0).to(device)  # 增加 batch 维度

    # 3️⃣ 前向推理
    with torch.no_grad():
        out = model(img)
        pred = out.argmax(1).item()

    label = "cat" if pred == 0 else "dog"
    print(f"预测结果：{label}")

if __name__ == '__main__':
    img_name = input("请输入名称: ")
    infer(f"campus/{img_name}.png")
