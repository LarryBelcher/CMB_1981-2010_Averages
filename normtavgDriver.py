#!/usr/bin/python

import matplotlib as mpl
mpl.use('Agg')
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os, datetime, sys, subprocess
import numpy as np



def int2str(mm):
	if(mm == '00'): ms = 'No Data'
	if(mm == '01'): ms = 'January'
	if(mm == '02'): ms = 'February'
	if(mm == '03'): ms = 'March'
	if(mm == '04'): ms = 'April'
	if(mm == '05'): ms = 'May'
	if(mm == '06'): ms = 'June'
	if(mm == '07'): ms = 'July'
	if(mm == '08'): ms = 'August'
	if(mm == '09'): ms = 'September'
	if(mm == '10'): ms = 'October'
	if(mm == '11'): ms = 'November'
	if(mm == '12'): ms = 'December'
	return ms


mm = sys.argv[1]   #(expects format like: 01)
monthstr = int2str(mm)
labeldate = monthstr


imgsize = sys.argv[2]   #(expects 620, 1000, DIY, HD, or HDSD)

figdpi = 72


p1 = subprocess.Popen("python normtavgMap.py "+mm+" "+imgsize, shell=True)
p1.wait()


p2 = subprocess.Popen("python normtavgColorbar.py "+mm+" "+imgsize, shell=True)
p2.wait()


if not os.path.isdir('./Images'):
	cmd = 'mkdir ./Images'
	subprocess.call(cmd,shell=True)
if not os.path.isdir('./Images/Temperature/'+imgsize):
	cmd = 'mkdir ./Images/Temperature/'+imgsize.lower()
	subprocess.call(cmd,shell=True)



if(imgsize == '620' or imgsize == '1000'):
	im1 = Image.open("temporary_map.png")
	im2 = Image.open("temporary_cbar.png")
	im3 = Image.new('RGBA', size = (im1.size[0], im1.size[1]+im2.size[1]))
	im3.paste(im2, (0,im1.size[1]))
	im3.paste(im1, (0,0))
	img_path = './Images/Temperature/'+imgsize+'/'
	imgw = str(im3.size[0])
	imgh = str(im3.size[1])
	img_name = 'averagetemp-normals-cmb--'+imgw+'x'+imgh+'--0000-'+mm+'-00.png'
	pngfile = img_path+img_name
	print "Saving "+pngfile
	im3.save(pngfile)


if(imgsize == 'DIY'):
	im1 = "./temporary_map.png"
	imgs = Image.open(im1)
	imgw = str(imgs.size[0])
	imgh = str(imgs.size[1])
	img_path = './Images/Temperature/'+imgsize.lower()+'/'
	img_name = 'averagetemp-normals-cmb--'+imgw+'x'+imgh+'--0000-'+mm+'-00.png'
	cmd = 'mv '+im1+' '+img_name
	subprocess.call(cmd,shell=True)
	im2 = "./temporary_cbar.eps"
	cbar_name = 'averagetemp-normals-cmb--0000-'+mm+'-00_colorbar.eps'
	cmd = 'mv '+im2+' '+cbar_name
	subprocess.call(cmd,shell=True)
	cmd1 = 'zip averagetemp-normals-cmb--'+imgw+'x'+imgh+'--0000-'+mm+'-00.zip '+img_name+' '+cbar_name+' noaa_logo.eps '
	subprocess.call(cmd1,shell=True)
	cmd2 = 'mv averagetemp-normals-cmb--'+imgw+'x'+imgh+'--0000-'+mm+'-00.zip '+img_path
	subprocess.call(cmd2,shell=True)
	cmd3 = 'rm '+img_name+' '+cbar_name
	subprocess.call(cmd3,shell=True)

	
if(imgsize == 'HD'):
	hdim = Image.new("RGB", (1920,1080), color='#FFFFFF')
	imgw = '1920'
	imgh = '1080'
	
	im1 = Image.open("temporary_map.png")
	bbox = (0,0,1534,736)
	im1 = im1.crop(bbox)
	osize = im1.size
	new_size = (osize[0]+2,osize[1]+2)
	im1new = Image.new("RGB", new_size)
	im1new.paste(im1, ((new_size[0]-osize[0])/2, (new_size[1]-osize[1])/2))
		
	hdim.paste(im1new, (192,108))
	
	draw = ImageDraw.Draw(hdim)
	fntpath = '/usr/local/share/fonts/truetype/msttcorefonts/Trebuchet_MS.ttf'
	
	fnt1 = ImageFont.truetype(fntpath, 18)
	if(mm == '00'): xpos = 1632
	if(mm == '01'): xpos = 1630
	if(mm == '02'): xpos = 1627
	if(mm == '03'): xpos = 1639
	if(mm == '04'): xpos = 1644
	if(mm == '05'): xpos = 1648
	if(mm == '06'): xpos = 1642
	if(mm == '07'): xpos = 1646
	if(mm == '08'): xpos = 1638
	if(mm == '09'): xpos = 1619	
	if(mm == '10'): xpos = 1633
	if(mm == '11' or mm == '12'): xpos = 1623	
	draw.text((xpos,815), labeldate, (0,0,0), font=fnt1)
	
	
	#Add the colorbar
	cbar_orig = Image.open('temporary_cbar.png')
	bbox = (1,1,972,43)
	cbar_orig = cbar_orig.crop(bbox)
	old_size = cbar_orig.size
	new_size = (old_size[0]+2,old_size[1]+2)
	cbar_im = Image.new("RGB", new_size)
	cbar_im.paste(cbar_orig, ((new_size[0]-old_size[0])/2,
                      (new_size[1]-old_size[1])/2))
	hdim.paste(cbar_im, (474,866))


	fnt4 = ImageFont.truetype(fntpath, 47)
	text2 = "cool"
	draw.text((515,905), text2, (0,0,0), font=fnt4)
	text3 = "warm"
	draw.text((1290,905), text3, (0,0,0), font=fnt4)
	fnt2 = ImageFont.truetype(fntpath, 16)
	ttext = "Normal temperature ( F)"
	draw.text((213,815), ttext, (0,0,0), font=fnt2)
	fnt2a = ImageFont.truetype(fntpath, 8)
	draw.text((368,815), "o", (0,0,0), font=fnt2a)
	
	
	draw.polygon([(500,946), (485,936), (500,926)], fill="black", outline="black")
	draw.polygon([(1420,946), (1435,936), (1420,926)], fill="black", outline="black")
	
	img_path = './Images/Temperature/'+imgsize.lower()+'/'
	img_name = 'averagetemp-normals-cmb--'+imgw+'x'+imgh+'hd--0000-'+mm+'-00.png'
	pngfile = img_path+img_name
	print "Saving "+pngfile
	hdim.save(pngfile)


if(imgsize == 'HDSD'):
	hdim = Image.new("RGB", (1920,1080), color='#FFFFFF')
	imgw = '1920'
	imgh = '1080'
	
	im1 = Image.open("temporary_map.png")
	bbox = (0,0,1150,700)
	im1 = im1.crop(bbox)
	osize = im1.size
	new_size = (osize[0]+2,osize[1]+2)
	im1new = Image.new("RGB", new_size)
	im1new.paste(im1, ((new_size[0]-osize[0])/2, (new_size[1]-osize[1])/2))
		
	hdim.paste(im1new, (384,108))
	
	draw = ImageDraw.Draw(hdim)
	fntpath = '/usr/local/share/fonts/truetype/msttcorefonts/Trebuchet_MS.ttf'
	fnt1 = ImageFont.truetype(fntpath, 18)
	if(mm == '00'): xpos = 1440
	if(mm == '01'): xpos = 1440
	if(mm == '02'): xpos = 1436
	if(mm == '03'): xpos = 1448
	if(mm == '04'): xpos = 1453
	if(mm == '05'): xpos = 1457
	if(mm == '06'): xpos = 1453
	if(mm == '07'): xpos = 1455
	if(mm == '08'): xpos = 1446
	if(mm == '09'): xpos = 1428
	if(mm == '10'): xpos = 1440
	if(mm == '11' or mm == '12'): xpos = 1432
	draw.text((xpos,781), labeldate, (0,0,0), font=fnt1)
	
	fnt2 = ImageFont.truetype(fntpath, 14)
	ttext = "Normal temperature ( F)"
	draw.text((405,785), ttext, (0,0,0), font=fnt2)
	fnt2a = ImageFont.truetype(fntpath, 8)
	draw.text((541,784), "o", (0,0,0), font=fnt2a)
	
	#Add the colorbar
	cbar_orig = Image.open('temporary_cbar.png')
	bbox = (1,1,972,43)
	cbar_orig = cbar_orig.crop(bbox)
	old_size = cbar_orig.size
	new_size = (old_size[0]+2,old_size[1]+2)
	cbar_im = Image.new("RGB", new_size)
	cbar_im.paste(cbar_orig, ((new_size[0]-old_size[0])/2,
                      (new_size[1]-old_size[1])/2))
	hdim.paste(cbar_im, (474,830))
		
	fnt4 = ImageFont.truetype(fntpath, 47)
	text2 = "cool"
	draw.text((515,870), text2, (0,0,0), font=fnt4)
	text3 = "warm"
	draw.text((1290,870), text3, (0,0,0), font=fnt4)
	
	
	
	
	draw.polygon([(500,911), (485,901), (500,891)], fill="black", outline="black")
	draw.polygon([(1420,911), (1435,901), (1420,891)], fill="black", outline="black")
	
	img_path = './Images/Temperature/'+imgsize.lower()+'/'
	img_name = 'averagetemp-normals-cmb--'+imgw+'x'+imgh+'hdsd--0000-'+mm+'-00.png'
	pngfile = img_path+img_name
	print "Saving "+pngfile
	hdim.save(pngfile)