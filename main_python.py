from random import randint, choice
from pygame import init, display, font, event, mouse, MOUSEBUTTONDOWN, transform, image, QUIT
from debug_utility import *
from time import sleep
from threading import Thread
import pickle
import os
import sys
testing = True
distance = 0
# Initialization
init()
screen = display.set_mode((800, 600))
display.set_caption("Adventure-like")
font = font.Font(None, 36)
screen.fill(BLACK)


background = image.load(r"C:\Users\33905\Pictures\Cave.png")
background2 = image.load(r"C:\Users\33905\Pictures\Cave and wall.png")
player_image = image.load(r"C:\Users\33905\Pictures\Base.png")
background = transform.scale(background, (800, 600))
background2 = transform.scale(background2, (800, 600))
player_image = transform.scale(player_image, (150, 150))


def save_game_state(filename: str, state: dict) -> None:
    """Save game state to a file using pickle."""
    with open(filename, 'wb') as file:
        try:
            pickle.dump(state, file, pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            print(f"Error saving game state: {e}")

def load_game_state(filename: str) -> dict:
    """Load game state from a file using pickle."""
    with open(filename, 'rb') as file:
        return pickle.load(file)

def stop_bgmusic():
    """Run this before stopping the bgmusic thread"""
    global running_music
    running_music = False
    mixer.music.stop()

def getmpos(x_min: int, x_max: int, y_min: int, y_max: int) -> tuple[int, int]:
    """Return the mouse position if it is within the given range."""
    global x, y
    while True:
        sleep(0.009)
        for events in event.get():
            if events.type == MOUSEBUTTONDOWN:
                x, y = mouse.get_pos()
                if x_min <= x <= x_max and y_min <= y <= y_max:
                    return x, y
        
def writescr(intxt: str, xwrite: int, ywrite: int) -> None:
    """Writes text to the screen, first letter is at xwrite and ywrite"""
    global caption, screen
    text_surface = font.render(intxt, True, WHITE) # type: ignore
    screen.blit(text_surface, (xwrite, ywrite))
    display.flip()

def changescr(intxt: str) -> None:
    """Clears the screen then writes text to the screen."""
    global caption, screen, background, inbattle, player_image, monster_image
    screen.fill(BLACK)
    if not inbattle:
        screen.blit(background, (0, 0))
    if inbattle:
        screen.blit(background2, (0, 0))
        screen.blit(player_image, (150, 100))
        screen.blit(monster_image, (550, 90))
    text_surface = font.render(intxt, True, WHITE)  # type: ignore
    screen.blit(text_surface, (50, 300))
    display.flip()
    sleep(2)

def clearscr() -> None:
        """Run this before a writescr call"""
        screen.fill(BLACK)
        if not inbattle:
            screen.blit(background, (0, 0))
        if inbattle:
            screen.blit(background2, (0, 0))
            screen.blit(player_image, (150, 90))
            screen.blit(monster_image, (550, 100))

def anamatebattle() -> None:
    global inbattle
    if inbattle:
        num = randint(1, 4)
        while num > 0:
            num -= 1
            for i in range(50, 200, 25):
                monsterpos = randint(-100, 200)
                playerpos = randint(0, 400)
                screen.blit(background2, (0, 0))
                screen.blit(monster_image, (monsterpos + 400, 100))
                screen.blit(player_image, (playerpos, 100))
                display.flip()
                sleep(0.2)

def shop() -> None:
    """
    Open a shop where the player can buy items with gold. The player can click on an item to buy it or click quit to exit the shop.
    The player's current inventory and gold are displayed at the top of the screen.
    """
    #TODO Stop shop from looping
    global gold, fightinv, distance
    shopping = True
    options = {"sword": 10, "shield": 10, "potion": 10, "leather armor": 10}
    changescr("You enter a small shop")
    while shopping:
        changescr("Click on an item to buy it, click quit to exit.")
        writescr("sword", 50, 400)
        writescr("shield", 150, 400)
        writescr("potion", 250, 400)
        writescr("leather armor", 350, 400)
        writescr("quit", 520, 400)
        x, y = getmpos(0, 600, 400, 500)
        
        if 50 <= x < 150:
            buy = "sword"
        elif 150 <= x < 250:
            buy = "shield"
        elif 250 <= x < 350:
            buy = "potion"
        elif 350 <= x < 450:
            buy = "leather armor"
        elif 522 <= x:
            buy = "quit"
        else:
            continue
        screen.fill(BLACK)
        
        if buy == "quit":
            shopping = False
            changescr("You exit the shop")
            break
        elif buy in options and gold >= options[buy]:
            fight_inv.append(buy)
            gold -= options[buy]
            changescr(f"Your inventory contains: {', '.join(fight_inv)}")
        else:
            changescr("Invalid choice or insufficient funds.")
def quitgame_thread() -> None:
    for events in event.get():
        if events.type == QUIT:
            quit()
            sys.exit()

def explore(place: list[str]) -> None:
    """
    This function allows the player to explore a place. The player can find a random item in a container or nothing at all.
    """
    global gold, fight_inv, distance
    if not place:  # Check if the list is empty
        raise ValueError("The list 'place' cannot be empty.")
    placechoice: str = choice(place)
    changescr(f"You enter a {placechoice} cave")
    random_event_choice: int = randint(1, 2)
    container: str = choice(contlist)
    container_place: str = choice(place_contlist)
    if random_event_choice == 1:
        changescr(f"A {container} is visable {container_place}")
        changescr(f"Do you open the {container}?")
        writescr("[Open]", 50, 400)
        sleep(0.5)
        writescr("[Exit]", 215, 400)
        try:
            x, y = getmpos(25, 400, 300, 450)
        except TypeError:
            raise TypeError("The function 'getmpos' returned a null value.")
        
        if x <= 215:
            random_container_content: int = randint(1, 4)
            if random_container_content == 4:
                containerloot: str = choice(dropslist)
                changescr(f"You find a {containerloot} in the {container}")
                fight_inv.append(containerloot)
            elif random_container_content == 1:
                gold_amount: int = randint(10, 20)
                changescr(f"You find {gold_amount} gold in the {container}")
                gold += gold_amount
            else:
                changescr(f"You find nothing in the {container}")
        else:
            changescr("You don't open the container")
    if random_event_choice == 2:
        changescr("There is nothing remarkable in the cave")
        changescr("You journy on....")

def battle(player_health: int, player_attack: int, enemy_health: int, enemy_attack: int, player_mod: int, enemy_mod: int, monsters: list[str], drops: list[str]) -> None:
    """
    This is the main battle function, it takes in the player's health, attack, the enemy's health, attack, and mods, and the monster's type and the place the battle takes place.

    :param player_health: The player's current health
    :param player_attack: The player's current attack
    :param enemy_health: The enemy's current health
    :param enemy_attack: The enemy's current attack
    :param player_mod: The player's current modifier
    :param enemy_mod: The enemy's current modifier
    :param monster_list: A list of possible monsters
    :param drops: A list of items the monster_list could drop
    """
    global base_health, scale, enemy_fight_inv, heath_inv, fight_inv, x, y, inbattle, monster_image, distance
    inbattle = True
    er = 0
    enemy_attack_mod = 0
    monster_list: str = choice(monsters)
    if monster_list == "Snake":
        monster_image = image.load(r"C:\Users\33905\Pictures\Snake.png")
        monster_image = transform.scale(monster_image, (200, 200))
    elif monster_list == "Tiger":
        monster_image = image.load(r"C:\Users\33905\Pictures\Tiger.png")
        monster_image = transform.scale(monster_image, (200, 200))
    elif monster_list == "Witch":
        monster_image = image.load(r"C:\Users\33905\Pictures\Witch.png")
        monster_image = transform.scale(monster_image, (200, 200))
    elif monster_list == "Golem":
        monster_image = image.load(r"C:\Users\33905\Pictures\Stone golem.png")
        monster_image = transform.scale(monster_image, (200, 200))
    elif monster_list == "Troll":
        monster_image = image.load(r"C:\Users\33905\Pictures\Troll.png")
        monster_image = transform.scale(monster_image, (200, 200))
    elif monster_list == "Goblin":
        monster_image = image.load(r"C:\Users\33905\Pictures\Goblin.png")
        monster_image = transform.scale(monster_image, (200, 200))
    else:
        pass

    # Changes the scale
    scale += 10
    enemy_health = enemy_health + scale
    # Checks if you are dead
    run = False
    if base_health > 0:
        run = True
    else:
        pass
    # Adds a _ to the monster_list
    if scale >= 50:
        r = choice(drops)
        enemy_fight_inv.append(r)
    else:
        pass
        
    if run == True:
        if enemy_health > 50 + scale:
            changescr(f"A unsually strong {monster_list} appears!")
            changescr(f"The {monster_list} attacks!")
        if enemy_health <= 50 + scale:
            changescr(f"A weak {monster_list} appears!")
            changescr(f"The {monster_list} attacks!")
        # Check player mods
        # Sword
        if "sword" in fight_inv:
            player_attack = player_attack + 5
            changescr("You have a sword, you gain +5 attack")
            swdmg = randint(1, 2)
            if swdmg == 1:
                changescr("The sword seems fragile and will smash soon")
                fight_inv.remove("sword")
        # Shield
        if "shield" in fight_inv:
            enemy_attack = enemy_attack - 5
            changescr("You have a shield, the enemy has -5 attack")
            sdmg = randint(1, 2)
            if sdmg == 1:
                changescr("The shield seems fragile and will smash soon")
                fight_inv.remove("shield")
        # Potion    
        if "potion" in fight_inv:
            changescr("You have a potion, you drink it and gain +3 chance to hit")
            player_mod = player_mod + 3
            fight_inv.remove("potion")
        # Armor
        if "leather armor" in fight_inv:
            enemy_attack = enemy_attack - 3
            changescr("You have leather armor, you gain +3 armor")
            armordmg = randint(1, 2)
            if armordmg == 1:
                changescr("The armor is too damaged to be used again")
                fight_inv.remove("leather armor")
        else:
            pass

        # Check enemy mods
        if "sword" in enemy_fight_inv:
            enemy_attack = enemy_attack + 5
            changescr(f"The {monster_list} has a sword, it gains +5 attack")
        if "shield" in enemy_fight_inv:
            player_attack = player_attack - 5
            changescr(f"The {monster_list} has a shield, you lose 5 attack")
        if "potion" in enemy_fight_inv:
            changescr(f"The {monster_list} has a potion, it drinks it and gains +3 chance to hit")
            enemy_mod = enemy_mod + 3
        enemy_fight_inv = []

        # Find out who wins the fight
        while run == True:
            clearscr()
            writescr("Either [Parry]", 50, 300)
            writescr("Or [Dodge]", 215, 300)
            getmpos(25, 400, 200, 400)
            sleep(1)
            eroll = True
            if x > 215:
                ran2 = randint(1, 2)
                if ran2 == 1:
                    changescr(f"You dodge, the {monster_list} has a lower chance to hit")
                    enemy_mod -= 2
                elif ran2 == 2:
                    changescr("You do not dodge in time")
            elif x <= 215:
                ran = randint(1, 4)
                if ran == 1:
                    playsoundeffect(r"C:\Users\33905\Music\sword clash.mp3")
                    changescr("You parry the attack")
                    enemy_attack_mod += 5
                    eroll = False
                elif ran == 2:
                    changescr("You stumble leaving you weak")
                    enemy_attack_mod += 5
                else:
                    changescr("You miss the parry by a hair")
            anamatebattle()
            if eroll != False:
                er: int = randint(1,20) + enemy_mod
                if er < 0:
                    er = 0
                if er >= 10:
                    player_health -= enemy_attack + enemy_attack_mod
                    enemy_attack_mod = 0
                    changescr(f"The {monster_list} rolls a {er} and does {enemy_attack} damage")
                else:
                    changescr(f"The {monster_list} rolls a {er} and misses you")
            else:
                pass

            pr = randint(1,20) + player_mod
            if pr >= 10:
                if er < 0: # type: ignore
                    er = 0
                enemy_health -= player_attack
                changescr(f"You roll a {pr} and do {player_attack} damage")
            else:
                changescr(f"You roll a {pr} and miss the {monster_list}")
            if enemy_health <= 0:
                enemy_health = 0
            if player_health <= 0:
                player_health = 0

            # Inform the player about stats
            clearscr()            
            writescr(f"----| The {monster_list} has {enemy_health} health left |----", 50, 200)
            writescr(f"----| You have {player_health} health left |----", 50, 300)
            sleep(2)
            if enemy_health != 0:
                changescr(f"The {monster_list} attacks you again")
            if player_health == 0:
                changescr(f"The Player died. The, {monster_list} is the winner")
                run = False
                base_health = player_health
            elif enemy_health == 0:
                playsoundeffect(r"C:\Users\33905\Music\grunt.mp3")
                changescr(f"The Player wins! The {monster_list} is dead")
                # Healing for next round
                heath_inv.append("Health charm")
                fight_inv.append(choice(drops))
                if "Health charm" in heath_inv:
                    base_health = player_health
                    clearscr()
                    writescr("You find a health charm on the ground,", 50, 300)
                    writescr("when you pick it up you feel your body healing as the charm melts away...", 50, 400)
                    sleep(2)
                    base_health += 60
                    changescr(f"You feel restored, your health is {base_health}")
                    heath_inv.remove("Health charm")
                else:
                    pass
                run = False
            else:
                pass
    else:
        pass
    inbattle = False

def mainloop() -> None:
    """
    Main game loop that handles game initialization, loading, and running the game.
    It allows the player to choose a class or load a saved game state. The loop 
    continues until the player's health reaches zero.
    """
    global gold, fight_inv, heath_inv, base_health, base_attack, scale
    try:            
            # Check if there is a saved game available
        if os.path.exists("savefile.pkl"):
            changescr("Do you want to load a saved game?")
            writescr("Yes", 50, 400)
            sleep(0.5)
            writescr("No", 215, 400)
            getmpos(25, 400, 300, 500)

            # Start a new game
            if x > 215:
                changescr("You choose to start a new game")
                changescr("What class do you want to be?")
                writescr("Warrior", 50, 400)
                sleep(0.5)
                writescr("Tank", 215, 400)
                getmpos(25, 400, 300, 500)

                # Choose Tank class
                if x > 215:
                    changescr("You choose to be a tank")
                    base_health = tank.base_health
                    base_attack = tank.base_attack

                # Choose Warrior class
                elif x <= 215:
                    changescr("You choose to be a warrior")
                    base_health = warrior.base_health
                    base_attack = warrior.base_attack

            # Load the saved game
            elif x <= 215:
                changescr("You choose to load a saved game")
                saved_game = load_game_state("savefile.pkl")
                gold = saved_game["gold"]
                fight_inv = saved_game["fight_inv"]
                heath_inv = saved_game["heath_inv"]
                base_health = saved_game["base_health"]
                base_attack = saved_game["base_attack"]
                scale = saved_game["scale"]
        
        # For testing purposes ONLY 
        if testing:       
            changescr("Is this a test??")
            writescr("No", 50, 400)
            sleep(0.5)
            writescr("Battle", 150, 400)
            sleep(0.5)
            writescr("Shop", 250, 400)
            sleep(0.5)
            writescr("Explore", 350, 400)
            getmpos(25, 450, 350, 500)
            if x > 150 and x <= 240:
                battle(base_health, 10, randomnum, 10, 0, 0, monsterlist, dropslist)
            elif x > 250 and x <= 340:
                shop()
            elif x > 350 and x <= 440:
                explore(placelist)
            elif x < 100:
                pass

        # Main game loop
        while base_health != 0:
            # Save game state each iteration
            game_state = {
                "gold": gold,
                "fight_inv": fight_inv,
                "heath_inv": heath_inv,
                "base_health": base_health,
                "base_attack": base_attack,
                "scale": scale,
            }
            save_game_state("savefile.pkl", game_state)

            # Explore and initiate battles
            exploreloop = True
            while exploreloop:
                if randint(1, 2) == 2:
                    explore(placelist)
                else:
                    exploreloop = False

            if base_health % 2 == 1:
                shop()

            battle(base_health, 10, randomnum, 10, 0, 0, monsterlist, dropslist)
            
        # End the game
        changescr("This is the end of the game, thank you for playing.")
        quit()
    except Exception as e:
        print(f"Error in mainloop: {e}")

if __name__ == "__main__":
    # Start the music thread
    music_thread = Thread(target=bgmusic, daemon=True)  # Daemon thread ends with the program
    quit_thread = Thread(target=quitgame_thread, daemon=True)
    music_thread.start()
    quit_thread.start()

    try:
        mainloop()  # Run your game loop here
    finally:
        stop_bgmusic()
        music_thread.join()
