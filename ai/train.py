import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from ml.model import FaceCNN
from ml.dataset import StudentDataset, get_transforms

def train_model():
    data_dir = "dataset"
    epochs = 15
    batch_size = 4
    learning_rate = 0.001
    
    dataset = StudentDataset(data_dir=data_dir, transform=get_transforms())
    num_classes = len(dataset.classes)
    
    if num_classes == 0:
        print(" لا يوجد اي طالب مسجل بعد")
        return

    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    
    model = FaceCNN(num_classes=num_classes)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    print(" بدء تدريب النموذج على")
    model.train()
    
    for epoch in range(epochs):
        running_loss = 0.0
        for images, labels in dataloader:
            optimizer.zero_grad()          
            outputs = model(images)             
            loss = criterion(outputs, labels)  
            loss.backward()                     
            optimizer.step()                  
            
            running_loss += loss.item()
            
        print(f"Epoch [{epoch+1}/{epochs}] - Loss: {running_loss/len(dataloader):.4f}")
        
    torch.save({
        'model_state_dict': model.state_dict(),
        'class_to_idx': dataset.class_to_idx,
        'classes': dataset.classes
    }, 'face_model.pth')
    
    print("تم تدريب النموذج بنجاح")

if __name__ == '__main__':
    train_model()
