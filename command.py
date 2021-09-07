# -*- coding: utf-8 -*-

import cv2
import serial
from time import sleep
from camera import Camera
from keys import Button, press, pressRep
from notify import send_capture

def reset(ser):
    print('リセットします.')
    press(ser, Button.HOME, 0.1, 1.0)
    press(ser, Button.X, 0.1, 1.0)
    press(ser, Button.A, 0.1, 1.0)
    press(ser, Button.A, 0.1, 1.0)
    press(ser, Button.A, 0.1, 15.0)
    press(ser, Button.A, 0.1, 2.0)
    for _ in range(5):
        press(ser, Button.A, 0.1, 1.0)
    pressRep(ser, Button.B, 50, interval=0.5, wait=1.0)

def command(camera, ser):
    ikisaki = 3 # Change Here
    press(ser, Button.B, 0.1, 0.6)
    count = 1
    ball = 0
    lap = 1
    a = 1
    wincount = 0
    while True:
        print("ダイマックスアドベンチャー開始")
        press(ser, Button.A, 0.1, 1.5) # 話しかける
        press(ser, Button.A, 0.1, 0.5)
        press(ser, Button.A, 0.1, 1.8) # 居場所の記録を～
        press(ser, Button.A, 0.1, 1.5)
        press(ser, Button.A, 0.1, 1.5) #どのポケモンを目指しますか
        pressRep(ser, Button.DOWN , ikisaki -1, interval= 0.5, wait= 1.0)
        press(ser, Button.A, 0.1, 2.0)
        press(ser, Button.A, 0.1, 1.0) # レポート
        press(ser, Button.A, 0.1, 5.5) # はい
        press(ser, Button.DOWN, 0.05, 0.4)
        press(ser, Button.A, 0.1, 2.0) # ひとりで挑戦
        press(ser, Button.A, 0.1, 19) # ポケモン選択
        print("道を選ぶ")
        for r in range(0, 30):
            press(ser, Button.A, 0.1, 0.1)
        match= 0
        taiki = 0 # 待機の回数　一定回数以上連続したら止める
        while match< 6:
            match+= 1
            combat = 1 # 戦闘終了判定
            koukan = 0 # ポケモン交換
            tarn = 1 # ターン数カウント
            daimatarn = 0 # ダイマ切れたら技選択
            waza = 1 # 技選び
            wazaLog = 1 # 選択した技を記録
            nomalwazaflag = 1 # 通常時の技選択
            daimawazaflag = 0 # ダイマ後の技選択
            wazaflag = 0 # 技の再選択
            wazacount1 = 0 # 効果抜群
            wazacount2 = 0 # 効果あり
            wazacount3 = 0 # いまひとつ
            wazacount4 = 0 # 変化技
            print("戦闘開始")
            daima = 1 # ダイマックス判定
            while combat == 1:
                for r in range(0, 15):
                    press(ser, Button.B, 0.1, 0.1) # 待機

                if camera.isContainTemplate('RaidTatakau.png', 0.9): # たたかうコマンド
                    print("たたかう")
                    if taiki == 1: # pp切れ
                        print("pp切れ")
                        koukan = 1
                        wazaLog += 1
                        #wazaflag =1

                    print("{}ターン目{}戦目{}周目".format(tarn, match, lap))
                    taiki = 0
                    tarn += 1
                    press(ser, Button.A, 0.1, 1.0)
                    # ダイマが切れたとき 技再選択
                    if daima == 0 and daimatarn + 3 == tarn:
                        print("ダイマ終了")
                        wazaflag = 1


                    if wazaflag == 1 and wazaLog != 1: # 技再選択
                        print("技再選択")
                        if camera.isContainTemplate('DaiMax.png', 0.95):
                            press(ser, Button.RIGHT, 0.05, 0.05)
                        wazaflag = 0

                        for h in range(1,wazaLog):
                            press(ser, Button.DOWN, 0.1, 0.5)
                        waza = 1
                        press(ser, Button.Y, 0.1, 0.5)
                        while waza < 6:
                            if not camera.isContainTemplate('HenkaWaza.png', 0.9):#攻撃技を探す
                                waza = 6
                                wazaflag = 0
                            else:
                                press(ser, Button.DOWN, 0.05, 0.4)
                                wazaLog += 1
                                waza += 1

                    if daima == 1:
                        print("ダイマ判定")
                        if camera.isContainTemplate('DaiMax.png', 0.95):
                            print("ダイマックス")
                            # 効果抜群の技を選択、記録
                            press(ser, Button.LEFT, 0.1, 0.4) # ダイマックス
                            press(ser, Button.A, 0.1, 0.8)
                            daima = 0
                            daimatarn = tarn
                            daimawazaflag = 1
                            nomalwazaflag = 0
                            wazaflag = 0
                        else:
                            print("ダイマなし")
                        # ダイマ前後、倒されたとき、技再選択
                    if daimawazaflag == 1:
                        print("ダイマ技選択")
                        if a != 7:
                            wazaLog = 1
                    while daimawazaflag == 1 and camera.isContainTemplate('KoukabatugunSearch.png', 0.8) and wazacount1 <4 : # 効果抜群
                        if camera.isContainTemplate('Koukabatugun.png', 1.0, False):
                            print("効果抜群")
                            press(ser, Button.A, 0.1, 0.3)
                            daimawazaflag = 0
                        else:
                            press(ser, Button.DOWN, 0.1, 0.8)
                            wazaLog += 1
                            wazacount1 += 1
                    while daimawazaflag == 1 and camera.isContainTemplate('KoukaariSearch.png', 0.8) and wazacount2 <4 : # 効果あり
                        if camera.isContainTemplate('Koukaari.png', 1.0, False):
                            print("効果あり")
                            press(ser, Button.A, 0.1, 0.3)
                            daimawazaflag = 0
                        else:
                            press(ser, Button.DOWN, 0.1, 0.8)
                            wazaLog += 1
                            wazacount2 += 1
                    while daimawazaflag == 1 and camera.isContainTemplate('imahitotuSearch.png', 0.8) and wazacount3 <4 : # 変化技
                        if camera.isContainTemplate('imahitotu.png', 1.0, False):
                            print("いまひとつ")
                            press(ser, Button.A, 0.1, 0.3)
                            daimawazaflag = 0
                        else:
                            press(ser, Button.DOWN, 0.1, 0.8)
                            wazaLog += 1
                            wazacount3 += 1
                    while daimawazaflag == 1 and camera.isContainTemplate('HenkaSearch.png', 0.8) and wazacount4 <4 : # 変化技
                        if camera.isContainTemplate('Henka.png', 1.0, False):
                            print("変化技")
                            press(ser, Button.A, 0.1, 0.3)
                            daimawazaflag = 0
                        else:
                            press(ser, Button.DOWN, 0.1, 0.8)
                            wazaLog += 1
                            wazacount4 += 1
                    #全部当てはまらないとき
                    while daimawazaflag == 1:
                        print("効果なし")
                        wazaLog = 1
                        daimawazaflag = 0
                    if nomalwazaflag == 1: # 通常時　攻撃技選択
                        nomalwazaflag = 0
                        print("技を選ぶ")
                        press(ser, Button.Y, 0.1, 0.5) # わざ説明

                        a = 1
                        while a < 5:
                            wazaLog = a
                            a += 1
                            if not camera.isContainTemplate('HenkaWaza.png', 0.95):#攻撃技を探す
                                r = 1
                                while r < 19:
                                    if camera.isContainTemplate('type'+str(r)+'_2.png', 0.95):#技のタイプを認識
                                        if camera.isContainTemplate('type'+str(r)+'.png', 0.92, False):#相性を確認
                                            print("効果抜群")
                                            a = 7
                                            wazaflag = 0
                                        else:#効果抜群ではない
                                            press(ser, Button.DOWN, 0.05, 0.4)
                                            wazaLog += 1
                                        r = 19
                                    r += 1
                            else:#攻撃技ではない
                                press(ser, Button.DOWN, 0.05, 0.4)
                        if a != 7:
                            print("効果抜群なし")
                            wazaLog = 1
                            if not camera.isContainTemplate('HenkaWaza.png', 0.95):#攻撃技を探す
                                waza = 6
                                wazaflag = 0
                            else:
                                press(ser, Button.DOWN, 0.05, 0.4)
                                wazaLog += 1
                                waza += 1



                    press(ser, Button.A, 0.1, 0.9) # わざを選択
                    press(ser, Button.A, 0.1, 2.0) # 対象を選択
                    press(ser, Button.DOWN, 0.05, 0.4)
                    press(ser, Button.A, 0.1, 2.0) # 対象を選択
                    for r in range(0, 10):
                        press(ser, Button.B, 0.1, 0.1) # B連打

                elif camera.isContainTemplate('Ouen.png', 0.9): # おうえんコマンド
                    print("おうえん")
                    taiki = 0
                    print("{}ターン目{}戦目{}周目".format(tarn, match, lap))
                    press(ser, Button.A, 0.1, 0.5)
                    wazaflag = 1
                    tarn += 1
                    # ダイマ終わり
                    if daima == 0:
                        daimatarn = 0

                elif camera.isContainTemplate('Tukamaeru.png', 0.95): # つかまえるコマンド
                    print("つかまえる{}体目".format(match))
                    taiki = 0
                    combat = 2# 勝利
                    ball += 1 # ボール消費数カウント
                    press(ser, Button.A, 0.1, 0.9)
                    press(ser, Button.A, 0.1, 0.5)
                    if match== 4: # ボス捕獲
                        wincount += 1
                        match+= 1
                        print("ボス捕獲")
                    else:
                        print(match, "体目捕獲")
                        sleep(24.0)
                        if match== 2 or koukan == 1: # 手持ちを入れ替えますか
                            press(ser, Button.A, 0.1, 5.5)
                            wazaLog = 1
                            nomalwazaflag = 1 # 通常時の技選択
                            daimawazaflag = 0 # ダイマ後の技選択
                            wazaflag = 0 # 技の再選択
                            koukan = 0
                        else:
                            press(ser, Button.B, 0.1, 3.5)
                            wazaflag = 1
                        for r in range(0, 40):
                            press(ser, Button.A, 0.1, 0.1) # 道を選ぶ

                elif camera.isContainTemplate('Motikaeri.png', 0.95): # ポケモンを捕まえた！
                    print("ポケモン選択")
                    if camera.isContainTemplate('Motikaeri2.png', 0.9): #ポケモンを連れて帰らなくてよろしいですか
                        press(ser, Button.B, 0.1, 2.0)
                    press(ser, Button.UP, 0.1, 1.5)
                    press(ser, Button.A, 0.1, 1.0)
                    press(ser, Button.DOWN, 0.1, 1.0)
                    press(ser, Button.A, 0.1, 3.5)
                    for count in range(0, 4):
                        if camera.isContainTemplate('ShineMark.png', 1.01): # 色違いマーク確認
                            print("色違い")
                            camera.readFrame()
                            send_capture(camera, '色違い')
                            if count == 0 and match> 4: # ボスが色違いの時
                                print(lap, "周、ボスを倒した回数", wincount, "回")
                                return True
                            press(ser, Button.B, 0.1, 2.8) # ポケモンを連れて帰る
                            press(ser, Button.A, 0.1, 0.8)
                            press(ser, Button.A, 0.1, 0.8)
                            press(ser, Button.A, 0.1, 0.8)
                        elif count < 3:
                            print("通常色")
                            press(ser, Button.UP, 0.1, 1.0)
                    print("通常色")
                    press(ser, Button.B, 0.1, 2.5)
                    press(ser, Button.B, 0.1, 0.5)
                    print("行先を残しますか")
                    r = 1
                    while not camera.isContainTemplate('suana.png', 0.7) and not camera.isContainTemplate('suana3.png', 0.7) and r <= 40:
                        press(ser, Button.A, 0.1, 0.5)
                        r += 1
                    if r >= 40:
                        print("巣穴の前に戻る")
                        pressRep(ser, Button.B ,40 ,interval = 0.3, wait = 0.3)
                    pressRep(ser, Button.B ,10) # 終わり
                    print("一周終了")

                    match= 7
                    combat = 0

                taiki += 1
                if taiki == 28 or tarn == 30:
                    print("どこかで止まりました")
                    send_capture(camera, 'ERROR')
                    reset(ser)
                    return False
                print("待機中", taiki)
        # ダイベンチャー終了
        if ball > 800 : # ボール消費数チェック
            print("ボール切れ")
            return True
        print("{}周、ボスを倒した回数{}回".format(lap, wincount))
        lap += 1

def commands(camera, ser):
    while not command(camera, ser):
        pass