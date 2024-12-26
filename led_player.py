#!/usr/bin/env python3
#
# Author: Andrey Konovalov <andreyknvl@gmail.com>
# Update: EPCDIY  <epcdiy@qq.com>
#

import array
import binascii
import sys
import pygame
import time
import numpy as np

import usb.core
import usb.util


VENDOR_ID = 0x5986
PRODUCT_ID = 0x02d2

dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

if dev is None:
	raise ValueError('Device not found')

def log(write, bRequest, wValue, wIndex, msg, e):
	print('%s, request = 0x%02x, value = 0x%02x, index = 0x%02x' % \
		('write' if write else 'read', bRequest, wValue, wIndex))
	if not(e):
		if write:
			print(' => success: %d' % (msg,))
		else:
			print(' => success: %d' % (len(msg),))
			print('   ', binascii.hexlify(msg))
	if e:
		print(' => %s' % (str(e),))

def request_write(bRequest, wValue, wIndex, data):
	bmRequestType = usb.util.CTRL_TYPE_VENDOR | \
			usb.util.CTRL_RECIPIENT_DEVICE | \
			usb.util.CTRL_OUT
	try:
		msg = dev.ctrl_transfer(bmRequestType=bmRequestType, bRequest=bRequest,
					wValue=wValue, wIndex=wIndex,
					data_or_wLength=data)
		#log(True, bRequest, wValue, wIndex, msg, None)
	except usb.core.USBError as e:
		log(True, bRequest, wValue, wIndex, None, e)
		raise

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def arbitrary_write(addr, value):
	request_write(0x42, value, addr, '')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# 设置摩斯电码的音频频率和时长
dot_duration = 0.108 # 点的持续时间
dash_duration = dot_duration * 3  # 划的持续时间
pause_duration = dot_duration  # 点与点之间的间隔
letter_pause_duration = dot_duration * 2  # 字母之间的间隔
word_pause_duration = dot_duration * 2  # 单词之间的间隔
every_duration=dot_duration*0.5
# 初始化pygame的混音器
pygame.mixer.init()

# 创建音频的音符（点和划）
def create_sound(duration, frequency=1000):
    sample_rate = 44100  # 采样率
    amplitude = 4096  # 音量
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)  # 生成正弦波
    wave = np.array([wave, wave])  # 将一维数组转换为二维数组（立体声）
    wave = wave.T  # 转置，以符合 pygame 的音频格式
    wave = np.ascontiguousarray(wave)  # 确保数组是C-contiguous类型
    sound = pygame.sndarray.make_sound(wave.astype(np.int16))  # 转换为pygame音频格式
    return sound

# 播放摩斯电码
def play_morse_code(code):
    for symbol in code:
        print(symbol, end='', flush=True)
        if symbol == '.':
            sound = create_sound(dot_duration)
            arbitrary_write(0x80, 0x02)
            sound.play()      
            time.sleep(dot_duration)
            arbitrary_write(0x80, 0x00)
            time.sleep(every_duration)
        elif symbol == '-':
            sound = create_sound(dash_duration)
            arbitrary_write(0x80, 0x02)
            sound.play()
            time.sleep(dash_duration)
            arbitrary_write(0x80, 0x00)
            time.sleep(every_duration)
        elif symbol == ' ':
            time.sleep(pause_duration)
        elif symbol == '/':  # 单词之间
            time.sleep(word_pause_duration)

# 输入摩斯电码文本
morse_text = "./.--./-.-./-../../-.--/-.../../.-/-./.-../../.-/-./--."
# 播放摩斯电码
play_morse_code(morse_text)

