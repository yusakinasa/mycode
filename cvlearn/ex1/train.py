import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, random_split
from torch.utils.tensorboard import SummaryWriter
import os

def train():
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # =========================
    # 1. 数据预处理
    # =========================
    train_dir = "data/train"

    # 数据增强和预处理
    train_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
    ])

    val_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
    ])

    # 1. 读取整个训练集
    full_dataset = datasets.ImageFolder(train_dir, transform=train_transform)

    # 2. 划分 80% train / 20% val
    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])

    # 3. 修改 val_dataset 的 transform
    # random_split 会保持原 dataset 的 transform，替换为 val_transform
    val_dataset.dataset.transform = val_transform

    # 4. DataLoader
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, num_workers=4)

    # =========================
    # 2. 加载 VGG16 预训练模型
    # =========================
    model = models.vgg16(weights=models.VGG16_Weights.DEFAULT)

    # 冻结特征提取层
    for param in model.features.parameters():
        param.requires_grad = False

    # 替换分类器最后一层（1000 → 2）
    model.classifier[6] = nn.Linear(4096, 2)

    model = model.to(device)

    # =========================
    # 3. 损失函数 & 优化器
    # =========================
    criterion = nn.CrossEntropyLoss()

    optimizer = optim.Adam(
        model.classifier.parameters(),  # 只优化 classifier
        lr=1e-4
    )

    # =========================
    # 4. TensorBoard
    # =========================
    writer = SummaryWriter(log_dir="logs/vgg16")

    best_acc = 0.0
    num_epochs = 20
    total_train_step =0

    # =========================
    # 5. 训练循环
    # =========================
    for epoch in range(num_epochs):
        print("-----------第{}轮开始-------------".format(epoch + 1))
        model.train()
        running_loss = 0.0
        running_correct = 0

        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)

            loss.backward()
            optimizer.step()
            total_train_step += 1
            if total_train_step % 100 == 0:
                print("训练次数:{} ，loss :{}".format(total_train_step, loss.item()))  # item是tensor的值


            running_loss += loss.item() * images.size(0)
            running_correct += (outputs.argmax(1) == labels).sum().item()

        train_loss = running_loss / len(train_dataset)
        train_acc = running_correct / len(train_dataset)

        writer.add_scalar("Loss/train", train_loss, epoch)
        writer.add_scalar("Acc/train", train_acc, epoch)

        # =========================
        # 6. 验证阶段
        # =========================
        model.eval()
        correct = 0

        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                correct += (outputs.argmax(1) == labels).sum().item()

        val_acc = correct / len(val_dataset)
        writer.add_scalar("Acc/val", val_acc, epoch)

        print(
            f"Epoch [{epoch+1}/{num_epochs}] "
            f"Train Loss: {train_loss:.4f} "
            f"Train Acc: {train_acc:.4f} "
            f"Val Acc: {val_acc:.4f}"
        )

        # =========================
        # 7. 保存最优模型
        # =========================
        if val_acc > best_acc:
            best_acc = val_acc
            os.makedirs("checkpoints", exist_ok=True)
            torch.save(model.state_dict(), "checkpoints/vgg16_best.pth")

        if val_acc >= 0.95:
            print("✅ 验证准确率已超过 95%，提前结束训练")
            break

    writer.close()
    print(f"Best Validation Accuracy: {best_acc:.4f}")

if __name__ == "__main__":
    train()
