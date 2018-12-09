import argparse
import time

from os.path import basename, normpath

import torch
from PIL import Image
from torch.autograd import Variable
from torchvision.transforms import ToTensor, ToPILImage

from model import Generator

parser = argparse.ArgumentParser(description='SR single image')
parser.add_argument('--lr', type=str, help='test image path')
parser.add_argument('--m', default='cp/netG_GAN_gpu.pth', type=str, help='model')
opt = parser.parse_args()

lr = opt.lr
pth = opt.m
with torch.no_grad():
	model = Generator().eval()
	if torch.cuda.is_available():
		model.cuda()
	model.load_state_dict(torch.load(pth))

	image = Image.open(lr)

	image = Variable(ToTensor()(image)).unsqueeze(0)
	
	if torch.cuda.is_available():
		image = image.cuda()

	out = model(image)
	out_img = ToPILImage()(out[0].data.cpu())
	out_img.save('generated/' + basename(normpath(lr)))