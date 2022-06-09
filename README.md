###### tags: `計算機組織`
# 期末專題
- [期末PPT](https://docs.google.com/presentation/d/1Um9bDFIl3elsNQSZhFx5m80lhi1oShYgHDFMpHMJ0q8/edit?usp=sharing) 
## 範例資源
- [範例教學網站](https://www.hackster.io/hackershack/smart-doorbell-video-intercom-system-e5aa61)
- [範例 github](https://github.com/HackerShackOfficial/Smart-Doorbell)
- [範例影片](https://www.youtube.com/watch?v=NteJ33ETxmA&ab_channel=DroneBotWorkshop)
## Enable the Microphone
- 進入 聲音控制畫面 `alsamixer` 
    ![](https://i.imgur.com/yTRnVDy.png)
- 調整 收音設定 `f4`: capture 
    - 調整至 100
    ![](https://i.imgur.com/RTsTWpH.png)
    - 按下 `esc` 離開
- 測試收音 :point_right: 錄音
    - `arecord --device=hw:1,0 --format S16_LE --rate 44100 -c1 test.wav -V mono`
    - 錄音畫面
    ![](https://i.imgur.com/5TOxNma.gif)
        > 可以看到###在變動代表有收到音
- 結束錄音`ctrl+C`
- 查看音檔(音檔在 /home/pi: 本地) : `ls` 
    - ![](https://i.imgur.com/mJLFu4G.png)
- 打開音檔 `aplay test.wav`

### 錄音& 播音
> [教學](http://shyuanliang.blogspot.com/2012/08/aplay-arecord-amixer.html)
- 找device number:
    `arecord -l`
    ![](https://i.imgur.com/CKuzSC7.png)
    > card: 2
    > device: 0

- 錄音
    - `arecord --device=hw:2,0 --format S16_LE --rate 44100 -c1 test.wav -V mono`
    > [color=red]要記得改!!!! card,device number : 2,0
- 播音
    `aplay --device=hw:1,0 test.wav`


>【Device number】
> MICROPHONE: 2
> speaker: 1
## Pi camera
- 安裝 python pip
    ```python=
    sudo apt install python3-pip
    ```
- 安裝picamara 套件
    ```python=
    sudo pip3 install picamera
    ```
- enable picamara
    ```python=
    sudo raspi-config
    ```
    * enter interface option
    * enter Camera to enable Yes


拍照和錄影都是加在`if(BUTTON_STATUS==True):`後
- 拍照
```python=
    #拍照
    camera.annotate_text=dt.datetime.now().strftime('%Y/%m/%d %H:%M:%S')#加入時間戳
    time.sleep(2)#暖機時間
    camera.capture('testpic.jpg')#拍
    camera.close()
```
- 錄影
```python=
    #錄影
    time.sleep(2)#暖機
    camera.start_recording('video.h264')#錄
    sleep(3)#camera.wait_recording#錄3秒
    camera.stop_recording#停
    camera.close()
```
- 目前全部
```python=
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

```
## telegram bot 

- [API](https://docs.python-telegram-bot.org/en/stable/telegram.message.html)

- 安裝telegram bot 相關套件
    -  讀token: 
    ```python=
    sudo pip3 install python-dotenv
    ```
    -  操作 Telegram Bot: 
    ```python=
    sudo pip3 install python-telegram-bot
    ```
- 引入套件
    ```python=
    import telegram
    from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
    ```
- 引入token:  `.env`
```python=
# from tkinter import NO
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN")
updater = Updater(TOKEN)
```

