import threading
from email.mime import audio
# from tkinter import NO
from dotenv import load_dotenv
import os, threading
from time import sleep

import time
from picamera import PiCamera
from datetime import datetime
import RPi.GPIO as GPIO
from picamera import PiCamera,Color
from subprocess import call, Popen, PIPE

from doorbell import VideoChat
import uuid



GPIO.setmode(GPIO.BOARD)
BUTTON_PIN=7
GPIO.setup(BUTTON_PIN,GPIO.IN)

import telegram
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters

def button(update: Update, context: CallbackContext) -> None :
    username = update.effective_user.username
    query = update.callback_query
    update.callback_query.message.reply_text('Hi')

def msg(update: Update, context: CallbackContext) :
    username = update.effective_user.username
    msg = update.message.text
    update.message.reply_text("!")

def record(update: Update, context: CallbackContext) :
    global VIDEO_PATH,VIDEO_PATH_mp4,count
    update.message.reply_text('幫您錄個影呦~ OVO')
    count = time_now(1)
    # camera.resolution = (1000, 1000)
    camera.start_preview()
    camera.annotate_background = Color('red')
    camera.annotate_text = "I'm comming ><"
    camera.rotation = 180
    VIDEO_PATH = ('/home/pi/Desktop/video/video%s.h264'% count)
    VIDEO_PATH_mp4 = ('/home/pi/Desktop/video/video%s.mp4'% count)
    camera.start_recording(VIDEO_PATH)
    time.sleep(2)
    camera.stop_recording()
    camera.stop_preview()
    convert(VIDEO_PATH, VIDEO_PATH_mp4)
    update.message.reply_text('Video From Telegram Bot : '+ count)
    update.message.reply_video(open(VIDEO_PATH_mp4, 'rb'))
    print("video recorded")

    # covert video format
def convert(VIDEO_PATH, VIDEO_PATH_mp4):
    # Record a 15 seconds video.
    print("Rasp_Pi => Video Recorded! \r\n")
    # Convert the h264 format to the mp4 format.
    command = "MP4Box -add " + VIDEO_PATH + " " + VIDEO_PATH_mp4
    call([command], shell=True)
    print("\r\nRasp_Pi => Video Converted! \r\n")

def time_now(type):
    # 1:檔名
    # 0: 時間字串
    if(type == 1):
        result = datetime.now().strftime("%Y%m%d%H%M%S%p")
    else:
        result = datetime.now().strftime("%Y-%m-%d %H:%M:%S %p")
    print(result)
    return result


def takePic(update: Update, context: CallbackContext) -> None :
    # print('U:',Update, ' U:',CallbackContext)
    # print('u:',update, ' c:',context)
    global detecting_thread,camera
    update.message.reply_text('找安找安')
    camera.start_preview()
    try:
        for i, filename in enumerate(
                camera.capture_continuous('image{counter:01d}.jpg')):
            print(filename)
            time.sleep(1)
            if i == 1:
                break
    finally:
        camera.stop_preview()

    for i in range (1,2):
            photo = 'image'+ str(i) + '.jpg'
            update.message.reply_photo(open(photo, 'rb'))
    # detecting_thread = None
# 設置指令名字，def 指令要做的事，可以從聊天室按指令執行
def start(update: Update, context: CallbackContext) -> None :
    global detecting_thread
    keyboard = [
        [KeyboardButton(text='/record')],
        [KeyboardButton(text='/takePic')],
        [KeyboardButton(text='/start')]
    ]
    update.message.reply_text('我是看門小精靈 OVO ', reply_markup=ReplyKeyboardMarkup(keyboard=keyboard))
    # BUTTON_STATUS = GPIO.input(BUTTON_PIN)
    # print("BTN STATUS : ",BUTTON_STATUS)
    detecting_thread = None
    detecting_thread = threading.Thread(target=Btn,args = (update, context))
    detecting_thread.start()


user_status = dict()
def Btn(update: Update, context: CallbackContext):
    global detecting_thread,video_chat,DOORBELL_SCREEN_ACTIVE_S
    while(True):
        BUTTON_STATUS = GPIO.input(BUTTON_PIN)
        detecting_thread = None
        while(BUTTON_STATUS == 0): #按鈕
            print("1st BTN STATUS : ",BUTTON_STATUS)
            update.message.reply_text('有人敲門優 OVO')
            update.message.reply_text(str(video_chat.get_chat_url()))
            video_chat.start()
            takePic(update, context)
            BUTTON_STATUS = 1
            print("2nd BTN STATUS : ",BUTTON_STATUS)
            time.sleep(DOORBELL_SCREEN_ACTIVE_S)
            video_chat.end()


# global 偵測 
detecting_thread = None
JITSI_ID = "HouseDoor"
chat_id = JITSI_ID if JITSI_ID else str(uuid.uuid4())
video_chat = VideoChat(chat_id)
DOORBELL_SCREEN_ACTIVE_S = 60


if __name__ == "__main__" :
    try :
        load_dotenv()
        TOKEN = os.getenv("TOKEN")
        updater = Updater(TOKEN)
        camera = PiCamera()

        updater.dispatcher.add_handler(CommandHandler('start', start))
        updater.dispatcher.add_handler(CommandHandler('takePic', takePic))
        updater.dispatcher.add_handler(CommandHandler('record', record))
        updater.dispatcher.add_handler(CallbackQueryHandler(button))
        updater.dispatcher.add_handler(MessageHandler(~Filters.command, msg))

        updater.start_polling()
        print('bot start listening...')
        updater.idle()
        
    except KeyboardInterrupt:
        detecting_thread = None
        GPIO.cleanup()