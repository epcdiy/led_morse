
import pygame
import time
import numpy as np

# 设置摩斯电码与字符的映射
morse_code = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F', '--.': 'G',
    '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N',
    '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T', '..-': 'U',
    '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y', '--..': 'Z', '-----': '0', '.----': '1',
    '..---': '2', '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7',
    '---..': '8', '----.': '9', '/': ' ',  # '/' 表示空格
}

# 设置摩斯电码的音频频率和时长
dot_duration = 0.108 # 点的持续时间
dash_duration = dot_duration * 3  # 划的持续时间
pause_duration = dot_duration  # 点与点之间的间隔
letter_pause_duration = dot_duration * 3  # 字母之间的间隔
word_pause_duration = dot_duration * 7  # 单词之间的间隔

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
        print(symbol)
        if symbol == '.':
            sound = create_sound(dot_duration)
            sound.play()
            time.sleep(dot_duration)
        elif symbol == '-':
            sound = create_sound(dash_duration)
            sound.play()
            time.sleep(dash_duration)
        elif symbol == ' ':
            time.sleep(pause_duration)
        elif symbol == '/':  # 单词之间
            time.sleep(word_pause_duration)

# 将摩斯电码转换为字符的函数
def text_to_morse(text):
    morse = ''
    for char in text:
        if char.upper() in morse_code:
            if morse:
                morse += ' '  # 字母之间有间隔
            morse += ' '.join([key for key, value in morse_code.items() if value == char.upper()])
        elif char == ' ':
            morse += ' / '  # 单词之间有间隔
    return morse

# 输入摩斯电码文本
morse_text = "--./..-/.-/-./--../..../..-/-.../../.-/-./.-../../.-/-./--./-.--/../.---/../.-/-./.../.-/-./.-../../.-/-."#text_to_morse('GUAN ZHU BIAN LIANG YI JIAN SAN LIAN')
#print(morse_text)
# 播放摩斯电码
play_morse_code(morse_text)
