# -*- coding: UTF-8 -*- 
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import re

import win32api,win32con,win32gui
import re,os
import time

import wordslist;
allwords = wordslist.wordslist.split("\n\n");
pages = len(allwords)
studypage = 2
words = allwords[studypage]

font1="YuGothB.ttc" # 字体文件路径
font2="simhei.ttf" # 字体文件路径
linespace = 5

def CreateTextImage(listindex, device, size, dest, text, bkcolor, textColor, fontsize, textColor2, fontsize2, textPos):
    fonta = ImageFont.truetype(font1.strip(), fontsize) #音标要用这个，否则乱码：simsun.ttc
    fontb = ImageFont.truetype(font2.strip(), fontsize2)
    back = fontsize / 2
    image = Image.new('RGB', size, bkcolor)
    draw = ImageDraw.Draw(image)
    #图片文件序号
    draw.text((size[0]-400, size[1]-50), time.strftime('%Y-%m-%d',time.localtime(time.time())) + " List%03d"%(listindex+1), font=fontb, fill=textColor)
    lines = text.split('\n')
    px = textPos[0]
    py = textPos[1]
    wordcnt = len(lines)
    for i in range(wordcnt):
        if len(lines[i])==0:continue
        #ss = lines[i].split(']', )
        try:
            p = lines[i].index(']');
        except:
            print("====except====", lines[i], "\n");continue
        if p < 0: continue
        s1 = lines[i][:p+1].strip()
        s2 = lines[i][p+1:].strip()
        textColor =((textColor[0] + 30)%255, (textColor[1] + 90)%255, (textColor[2] + 150)%255)
        textColor2 = ((textColor2[0] + 10)%255, (textColor2[1] + 10)%255, (textColor2[2] + 10)%255)
        s1 = re.sub("[\t \n\r]", "", s1)
        s2 = re.sub("[\t \n\r]", "", s2)
        # 英文只占半个字符宽
        if device == 1: #1:PC,直，一行；
            py = py + fontsize + linespace
            draw.text((textPos[0], py), s1, font=fonta, fill=textColor)
            draw.text((textPos[0]+len(s1)*fontsize/2.0 + fontsize/2, py+(fontsize-fontsize2)/2), s2, font=fontb, fill=textColor2, align="right")
        elif device==2: #2:PC,斜着，一行；
            py = py + fontsize + linespace
            if i < wordcnt/2:px = textPos[0] - back * i
            else:px = textPos[0] + back * (i-wordcnt)
            draw.text((px, py), s1, font=fonta, fill=textColor)
            draw.text((px+len(s1)*fontsize/2.0 + fontsize, py+(fontsize-fontsize2)/2), s2, font=fontb, fill=textColor2, align="right")
        elif device ==3: #：手机，直，两行；
            py = py + fontsize + fontsize2 + linespace
            draw.text((textPos[0], py), s1, font=fonta, fill=textColor)
            draw.text((textPos[0]+fontsize/2, py+fontsize), s2, font=fontb, fill=textColor2, align="right")
        else:
            pass
##    draw.text(textPos, text, font=fonta, fill=textColor)
    #image = image.resize((int(size[0]/2), int(size[1]/2)))
    image.save(dest)
    #image.show()
    image.close()

bkcolor = 0xC7EDCC #护眼色C7EDCC
bkcolor = ((bkcolor & 0xff0000) >> 16, (bkcolor & 0xff00) >> 8, bkcolor & 0xff)
textColor1 = 0x008B45
textColor1 = ((textColor1 & 0xff0000) >> 16, (textColor1 & 0xff00) >> 8, textColor1 & 0xff)
textColor2 = 0xaa00aa
textColor2 = ((textColor2 & 0xff0000) >> 16, (textColor2 & 0xff00) >> 8, textColor2 & 0xff)

#以下代码，图片适配电脑屏幕，请把生成目标文件夹修改为你自己的路径
destPath="F:/图片/Make/PC2/"
# 把0改为1就可以运行
if 0:
    device = 1 #1:PC,直，一行；2：PC,斜着，一行，两行；3：手机，直，两行
    device = 2
    fontsize = 46
    fontsize2 = 28
    #textPos = (800, 10)
    textPos = (220, 10)
    screenSize = ((int)(1920), (int)(1080))
    for i in range(len(allwords)):
        if len(allwords[i].strip())<2:continue
        destPath = "pc_words_list_%03d.jpg" % (i+1)
        CreateTextImage(i, device, screenSize, destPath, allwords[i].strip(), bkcolor, textColor1, fontsize, textColor2, fontsize2, textPos)

#以下代码，图片适配手机屏幕，请修改屏幕尺寸，请把生成目标文件夹修改为你自己的路径
destPath="F:/图片/Make/Phone/"
# 把0改为1就可以运行
if 0:
    device = 3
    fontsize = 50
    fontsize2 = 36
    textPos = (200, 20)
    screenSize = ((int)(1080), (int)(1920))
    for i in range(len(allwords)):
        if len(allwords[i].strip())<2:continue
        destPath = "phone_words_list_%03d.jpg" % (i+1)
        CreateTextImage(i, device, screenSize, destPath, allwords[i].strip(), bkcolor, textColor1, fontsize, textColor2, fontsize2, textPos)
        #break

