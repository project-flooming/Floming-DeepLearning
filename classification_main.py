import argparse

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

from dataset.classificatoin_dataset import ClassificationDataset
from models.shufflenetv2 import ShuffleNetV2
from models.mobilenetv3 import MobileNetV3
from train.classification_train import train_step

def get_args_parser():
    parser = argparse.ArgumentParser(description='Set Pix2Pix training', add_help=False)
    parser.add_argument('--path', defaults='/dataset/', type=str,
                        help='Path of data')
    parser.add_argument('--img_size', default='256', type=int,
                        help='Input size of Pix2Pix model')
    parser.add_argument('--device', default='cuda' if torch.cuda.is_availabel() else 'cpu', type=str,
                        help='Set device')
    parser.add_argument('--epoch', default=100, type=int)
    parser.add_argument('--batch_size', default=16, type=int)
    return parser

def main(args):
    device = torch.device(args.device)

    path = args.path

    train_loader = DataLoader(
        ClassificationDataset(path=args.path, subset='train', img_size=args.img_size, transforms_=True),
        batch_size=args.batch_size,
        shuffle=True,
        drop_last=True,
    )

    valid_loader = DataLoader(
        ClassificationDataset(path=args.path, subset='valid', img_size=args.img_size, transforms_=True),
        batch_size=args.batch_size,
        shuffle=True,
        drop_last=True,
    )


    model = ShuffleNetV2().to(device)

    history = train_step(
        model,
        train_data=train_loader,
        validation_data=valid_loader,
        n_epochs=args.epoch,
        learning_rate_scheduler=args.lr_scheduler,
        check_point=args.check_point,
        early_stop=args.early_stop,
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Classification Model Training', parents=[get_args_parser()])
    args = parser.parse_args()
    main(args)