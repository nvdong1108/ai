import cv2
import numpy as np
from gtts import gTTS
from PIL import Image


img = Image.open('avata.jpg')

text = 'Xin chao, toi la AI Cat'
tts = gTTS(text=text, lang='vi')
tts.save('am_thanh.mp3')


fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = 30
size = (img.width, img.height)
video = cv2.VideoWriter('video.mp4', fourcc, fps, size)

for i in range(100):
    frame = cv2.imread('avata.jpg')
    video.write(frame)

video.release()