# 2017.01.16 18:55:13 中国标准时间
#Embedded file name: F:\YinHuSDK\tools\U8SDKTool-Win-P34\scripts\image_utils.py
from PIL import Image, ImageEnhance

def appendIconMark(imgIcon, imgMark, position):
    if imgIcon.mode != 'RGBA':
        imgIcon = imgIcon.convert('RGBA')
    markLayer = Image.new('RGBA', imgIcon.size, (0, 0, 0, 0))
    markLayer.paste(imgMark, position)
    return Image.composite(markLayer, imgIcon, markLayer)

# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2017.01.16 18:55:13 中国标准时间
