import torch
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
from lenet import LeNet

def image_classification(file):
    
    model = LeNet()
# 加载模型参数
    checkpoint = torch.load("./lenet.pth")
    model.load_state_dict(checkpoint['state_dict'])
    # 对上传的图片进行预处理
    image = Image.open(file.name)
    transform = transforms.Compose([transforms.Grayscale(num_output_channels=1),
                                    transforms.Resize((28, 28)),
                                    transforms.ToTensor()])
    image = transform(image).unsqueeze(0)
    # 使用模型进行分类
    with torch.no_grad(): 
        output = model(image)
    # 获取分类结果
    _, predicted = torch.max(output, 1)
    class_index = predicted.item()
    return f"Classification result: {class_index}"



