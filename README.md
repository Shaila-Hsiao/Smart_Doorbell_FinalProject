# Smart_Doorbell_FinalProject
## Enable the Microphone
- 進入 聲音控制畫面 `alsamixer` 
    </br>![image](https://i.imgur.com/yTRnVDy.png)
- 調整 收音設定 `f4`: capture 
    - 調整至 100
    </br>![image](https://i.imgur.com/RTsTWpH.png)
    - 按下 `esc` 離開
- 測試收音 :point_right: 錄音
    - `arecord --device=hw:1,0 --format S16_LE --rate 44100 -c1 test.wav -V mono`
    - 錄音畫面
    </br>![image](https://i.imgur.com/5TOxNma.gif)
        > 可以看到###在變動代表有收到音
- 結束錄音`ctrl+C`
- 查看音檔(音檔在 /home/pi: 本地) : `ls` 
   </br>![image](https://i.imgur.com/mJLFu4G.png)
- 打開音檔 `aplay test.wav`
