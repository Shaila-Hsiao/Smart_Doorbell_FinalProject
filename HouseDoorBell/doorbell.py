#############
# User Parameters
#############



# Doorbell pin
DOORBELL_PIN = 26

# 電話會撥多久
# Number of seconds to keep the call active
DOORBELL_SCREEN_ACTIVE_S = 60

# 會議ID
# 如果等於NONE 自動產生隨機id
# ID of the JITSI meeting room
JITSI_ID = None  # If None, the program generates a random UUID
# JITSI_ID = "hackershackdoorbellexample"


# 設置鈴聲特效
# Path to the SFX file
RING_SFX_PATH = None  # If None, no sound effect plays
# RING_SFX_PATH = "/home/pi/ring.wav"

#############
# Program
#############

import time
import os
import signal
import subprocess
import smtplib
import uuid

# from email.MIMEMultipart import MIMEMultipart
# from email.MIMEText import MIMEText
# from email.MIMEImage import MIMEImage

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO. This is probably because you need superuser. Try running again with 'sudo'.")

#  開啟顯示(HDMI)
def show_screen():
    os.system("tvservice -p")
    os.system("xset dpms force on")

#  關閉顯示輸出
def hide_screen():
    os.system("tvservice -o")



# 按一下按鈕後
def ring_doorbell(pin):
    # 撥放音效
    # SoundEffect(RING_SFX_PATH).play()

    # meet ID 如果 = none，則 隨機產生ID 
    chat_id = JITSI_ID if JITSI_ID else str(uuid.uuid4())
    # 將ID交給 video_chat 處理 
    video_chat = VideoChat(chat_id)
    
    # 開啟顯示
    show_screen()

    video_chat.start()
    # 如果依定時間內沒有接電話的話，就掛斷
    time.sleep(DOORBELL_SCREEN_ACTIVE_S)
    video_chat.end()
    #  掛斷後關閉顯示
    hide_screen()




# meet 視訊聊天
class VideoChat:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self._process = None
    # 取得meet url
    def get_chat_url(self):
        return "http://meet.jit.si/%s" % self.chat_id
    # 開啟meet
    def start(self):
        if not self._process and self.chat_id:
            self._process = subprocess.Popen(["chromium-browser", "-kiosk", self.get_chat_url()])
        else:
            print("Can't start video chat -- already started or missing chat id")
    # 結束meet 
    def end(self):
        if self._process:
            os.kill(self._process.pid, signal.SIGTERM)



# 門鈴
class Doorbell:
    # Pin
    def __init__(self, doorbell_button_pin):
        self._doorbell_button_pin = doorbell_button_pin
    # 啟動
    def run(self):
        try:
            print("Starting Doorbell...")
            #  關閉顯示輸出
            hide_screen()
            self._setup_gpio()
            print("Waiting for doorbell rings...")
            # 等待別人按門鈴
            self._wait_forever()

        except KeyboardInterrupt:
            print("Safely shutting down...")

        finally:
            self._cleanup()

    def _wait_forever(self):
        while True:
            time.sleep(0.1)
    # 偵測 ring_doorbell
    def _setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._doorbell_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self._doorbell_button_pin, GPIO.RISING, callback=ring_doorbell, bouncetime=2000)

    def _cleanup(self):
        GPIO.cleanup(self._doorbell_button_pin)
        show_screen()


if __name__ == "__main__":
    doorbell = Doorbell(DOORBELL_PIN)
    doorbell.run()