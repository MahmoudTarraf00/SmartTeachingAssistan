import os
from PIL import Image
import torch
from torch.utils.data import Dataset
from torchvision import transforms

class StudentDataset(Dataset):
    def __init__(self, data_dir, transform=None):
    
        self.data_dir = data_dir
        self.transform = transform
        self.image_paths = []
        self.labels = []
        
        self.classes = sorted(os.listdir(data_dir)) if os.path.exists(data_dir) else []
        self.class_to_idx = {class_name: idx for idx, class_name in enumerate(self.classes)}
        
        if os.path.exists(data_dir):
            for class_name in self.classes:
                class_dir = os.path.join(data_dir, class_name)
                if os.path.isdir(class_dir):
                    for img_name in os.listdir(class_dir):
                        if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                            self.image_paths.append(os.path.join(class_dir, img_name))
                            self.labels.append(self.class_to_idx[class_name])

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        image = Image.open(img_path).convert('RGB')
        label = self.labels[idx]
        
        if self.transform:
            image = self.transform(image)
            
        return image, label

def get_transforms():
    return transforms.Compose([
        transforms.Resize((64, 64)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])
