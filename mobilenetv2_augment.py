import torch, torch.nn as nn, torch.optim as optim
import nets
from dataloader import dataloader
from train_model import train_model
from evaluate import evaluate
from utils import ImgAugmenter
import PIL

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
# use_gpu = torch.cuda.is_available()
# if use_gpu:
#     print("Using CUDA")

normalize = transforms.Normalize(mean=[0.6855248, 0.68901044, 0.6142709], std=[0.32218322, 0.27970782, 0.3134101])

preprocess = {
    'train': transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        normalize
    ]),
    'test': transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        normalize
    ])
} 

augmented = {
    'train': transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        ImgAugmenter(),
        lambda x: PIL.Image.fromarray(x),
        transforms.ColorJitter(hue=.05, saturation=.05),
        transforms.RandomHorizontalFlip(),
        transforms.RandomAffine(15),
        transforms.RandomRotation(20, resample=PIL.Image.BILINEAR),
        transforms.ToTensor(),
        normalize
    ]),
    'test': transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        normalize
    ])
}

train_loader, train_size, valid_loader, valid_size, test_loader = dataloader(colab=True, 
                                                                             batch_size=64, 
                                                                             transform=preprocess)
dataloader = {'train': train_loader, 'val': valid_loader}


criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(mobilenet.parameters(), lr=1e-4)

# train_model(mobilenet, criterion, optimizer, dataloader, train_size, valid_size, model_name='mobilenetv2_augment', num_epochs=100)
evaluate(mobilenet, test_loader, model_name='mobilenetv2_augment.pt')