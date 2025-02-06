from time import sleep
from pygame import mixer
import keyboard
mixer.init()

def playsound(pathtofile: str) -> None:
    mixer.music.stop()
    mixer.music.load(pathtofile)
    mixer.music.play(1, 0, 0)
while True:
    if keyboard.is_pressed('t'):
        if keyboard.is_pressed('1'):
            playsound(r"C:\Users\33905\Music\Sound\LOUD.mp3")
        if keyboard.is_pressed('2'):
            playsound(r"C:\Users\33905\Music\Sound\109_-_twilight_palace.mp3")
        if keyboard.is_pressed('3'):
            playsound(r"C:\Users\33905\Music\Sound\029_-_hyrule_field_(night).mp3")
        if keyboard.is_pressed('4'):
            playsound(r"C:\Users\33905\Music\Sound\Vine boom.mp3")
        if keyboard.is_pressed('5'):
            playsound(r"C:\Users\33905\Music\Sound\grunt-1-85280.mp3")
        if keyboard.is_pressed('6'):
            playsound(r"C:\Users\33905\Music\Sound\Boom.mp3")
        if keyboard.is_pressed('7'):
            playsound(r"C:\Users\33905\Music\Sound\sword-clash-241729 (2).mp3")
        if keyboard.is_pressed('8'):
            playsound(r"C:\Users\33905\Music\Sound\Phonk.mp3")
        if keyboard.is_pressed('9'):
            playsound(r"C:\Users\33905\Music\Sound\Suprise.mp3")
        if keyboard.is_pressed('0'):
            playsound(r"C:\Users\33905\Music\Sound\Airhorn.mp3")
        if keyboard.is_pressed('q'):
            mixer.music.stop()
        sleep(0.05)