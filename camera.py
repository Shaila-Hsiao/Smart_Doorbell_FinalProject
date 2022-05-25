import RPi.GPIO as GPIO
import picamera
import time
import datetime as dt

GPIO.setmode(GPIO.BOARD)
BUTTON_PIN=37
GPIO.setup(BUTTON_PIN,GPIO.IN)

while True:
    BUTTON_STATUS=GPIO.input(BUTTON_PIN)
    if(BUTTON_STATUS==True):#按鈕
        camera=picamera.PiCamera()
        #拍照
        #camera.annotate_text=dt.datetime.now().strftime('%Y/%m/%d %H:%M:%S')#加入時間戳
        #time.sleep(2)#暖機時間
        #camera.capture('testpic.jpg')#拍
        #camera.close()
        
        #錄影
        time.sleep(2)#暖機
        camera.start_recording('video.h264')#錄
        sleep(3)#camera.wait_recording#錄3秒
        camera.stop_recording#停
        camera.close()