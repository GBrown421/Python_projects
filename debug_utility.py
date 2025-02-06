from typing import List, Tuple

from random import randint
from pygame import init, mixer, image, transform, display, font

WHITE: Tuple[int, int, int] = (255, 255, 255)
BLACK: Tuple[int, int, int] = (0, 0, 0)
contlist: List[str] = ["chest", "pot", "vase", "jar", "crate"]
place_contlist: List[str] = ["in a niche in the wall", "in a pit in the ground", "buried under a pile of rock and slate"]
monsterlist: List[str] = ["Snake", "Goblin", "Troll", "Tiger", "Witch", "Dragon", "Golem"]
placelist: List[str] = ["overgrowen", "hot", "dark", "normal", "mined-out", "ancient", "gloomy", "small",]
dropslist: List[str] = ["sword", "shield", "potion", "leather armor"]
buylist: List[str] = ["sword", "shield", "potion", "leather armor"]
monster_image = image.load(r"C:\Users\33905\Pictures\Dragon.png")
monster_image = transform.scale(monster_image, (150, 100))

heath_inv: List[str] = []
enemy_fight_inv: List[str] = []
fight_inv: List[str] = []

base_health: int = 1
base_attack: int = 1
scale: int = -10
gold: int = 100
caption: int = 1
checknum: int = 1
x: int = 1
y: int = 1
randomnum: int = randint(1, 11) * 10

inbattle: bool = False
running_music: bool = True
class initater:
    init()
    screen = display.set_mode((800, 600))
    display.set_caption("Adventure-like")
    font = font.Font(None, 36)
    screen.fill(BLACK)


class warrior:
    base_attack: int = 15
    base_health: int = 100

class tank:
    base_attack: int = 10
    base_health: int = 150
    


def debug() -> None:
    global checknum
    print("Debug check", checknum)
    checknum += 1

def playsound(pathtofile: str) -> None:
    if not mixer.get_init():
        mixer.init()
    mixer.music.load(pathtofile)
    mixer.music.play(1, 0, 0)
    while mixer.music.get_busy():
        continue

def playsoundeffect(pathtofile: str) -> None:
    """
    Plays a sound effect on a separate channel without interfering with the background music.
    """
    # Ensure mixer is initialized (only once globally in your program)
    if not mixer.get_init():
        mixer.init()

    # Load and play the sound effect on a separate channel
    sound = mixer.Sound(pathtofile)
    sound.play()

def bgmusic() -> None:
    """Play music in the background in a loop."""
    global running_music
    init()
    tracks = [
        r"C:\Users\33905\Music.mp3",
        r"C:\Users\33905\Music.mp3",
        r"C:\Users\33905\Music.mp3"
    ]
    mixer.music.load(tracks[0])
    mixer.music.play()
    current_track = 1
    while running_music:
        if not mixer.music.get_busy():
            mixer.music.load(tracks[current_track])
            mixer.music.play()
            current_track = (current_track + 1)  % len(tracks)
