from PIL import ImageGrab
import win32gui, win32con, win32api
import time
from pathlib import Path

# Coordiantes and Colors
aries_point = (500, 400)          # Aries' hoppeta while talking
life1_point = (950, 70)           # First life
life2_point = (880, 70)           # Second life
life_color = (238, 203, 206)      # The color of full life slot
right_point = (650, 400)          # A point at right
left_point = (250, 400)           # A point at left
death_color = (205, 185, 199)     # The color of empty life slot
aries_color_1 = (252, 223, 212)   # Aries' hoppeta (common)
aries_color_2 = (141, 125, 129)   # Aries' hoppeta (in space)
aries_kami_iro = (142, 142, 151)  # Aries' hair    (in space)

left_hoshizora_point = (150, 125)   # hoshizora point(left)
right_hoshizora_point = (850, 125)  # hoshizora point(right)
original_utyuu = (0, 0, 0)          # The color of hoshizora in space
MODE_COMMON = 1         # We're fighting level 0 or 2
MODE_SPACE = 2          # We're fighting level 3
DEFENSE_LEFT = 0
DEFENSE_RIGHT = 1
COUNT = 0

# calculate the diff between 2 rgb tuples.
def diff_pixel(base, target):
    diff = sum((abs(base[0] - target[0]), abs(base[1] - target[1]), abs(base[2] - target[2])))
    return diff

# find the window of Aqua Afted.
def locate_aqua():
    offset = 1.25
    handle = win32gui.FindWindow(None, 'ひまわり アクアアフター')
    rect = win32gui.GetWindowRect(handle)
    # Note: Empirically, there is an 1.25x resize between the Rect from Windows and the bbox from pillow.
    # If this is not true on your computer, feel free to modify or remove the varible 'offset'.
    return (rect[0] * offset, rect[1] * offset, rect[2] * offset, rect[3] * offset)

# defend against Aries or Taigo.
def defend(defense, aqua_yukisaki):
    global COUNT
    DEFENSES = ((win32con.MOUSEEVENTF_LEFTDOWN, win32con.MOUSEEVENTF_LEFTUP),
    (win32con.MOUSEEVENTF_RIGHTDOWN, win32con.MOUSEEVENTF_RIGHTUP))
    win32api.mouse_event(DEFENSES[defense][0], 
    int(aqua_yukisaki[0]) + 20, int(aqua_yukisaki[1]) + 20, 0, 0)
    # If we're fighting level 0 we should defend longer
    # But alright we can certainly fight through the tutorial so...
    time.sleep(0.5)
    win32api.mouse_event(DEFENSES[defense][1],
    int(aqua_yukisaki[0]) + 20, int(aqua_yukisaki[1]) + 20, 0, 0)
    COUNT += 1
    print('hidari!' if defense == DEFENSE_LEFT else 'migi!')

# Whether the game has started.
def hajimatta(image):
    pixel = image.getpixel(life2_point)
    return diff_pixel(life_color, pixel) < 25

# Whether the player got killed by Aries.
def owatta(image):
    pixel = image.getpixel(life2_point)
    return diff_pixel(death_color, pixel) < 25

# Try to figure out whether Aries attacks and from which side the attack comes.
# Btw, according to the 'Mugentekisyutsu' game mode, Aries 'extracts' rather than 'attacks'...
def mikiru(image, mode, aqua_yukisaki, debug=False):
    # If we are in space (level 3) there will be a darkening filter over the game.
    # So we should judge here and decide if we should switch to another set of colors.
    aries_color = aries_color_1 if mode == MODE_COMMON else aries_color_2
    pixel_left = image.getpixel(left_point)
    pixel_right = image.getpixel(right_point)
    diff_left = diff_pixel(pixel_left, aries_color)
    diff_right = diff_pixel(pixel_right, aries_color)
    if diff_left < 45 or (diff_left < 50 and diff_right > 80):
        # If we are in level 3, the code always mistake Aries' hair as her hoppeta and give the wrong result
        # So here is a special judge for Aries' hair.
        if mode == MODE_SPACE and diff_pixel(pixel_left, aries_kami_iro) < diff_left and diff_right < 80:
            defend(DEFENSE_RIGHT, aqua_yukisaki)
        else:
            defend(DEFENSE_LEFT, aqua_yukisaki)
        if debug:
            image.save(Path().resolve() / f'_aqua_debug_{COUNT}.png')
            print(f'{COUNT}.png is saved under mode {mode}.')
        return True 
    if diff_right < 45 or (diff_right < 50 and diff_left > 80):
        if mode == MODE_SPACE and diff_pixel(pixel_right, aries_kami_iro) < diff_right and diff_left < 80:
            defend(DEFENSE_LEFT, aqua_yukisaki)
        else:
            defend(DEFENSE_RIGHT, aqua_yukisaki)
        if debug:
            image.save(Path().resolve() / f'_aqua_debug_{COUNT}.png')
            print(f'{COUNT}.png is saved under mode {mode}.')
        return True 
    # If Aries is waiting for chance, we do not need to defend.
    return False

# A common solution for level 0, 2 and 3 (except for airport and taigo fight)
# In level 1(Airport) the code will mistake the sunset as Aries' hoppeta.
# But as level 1 is surely simple, let's just ignore that.
def workload(aqua_yukisaki, debug=False):
    mode = MODE_COMMON
    while True:
        time.sleep(0.5)
        image = ImageGrab.grab(bbox = aqua_yukisaki)
        if hajimatta(image):
            print('hajimatta!')
            # Are we in level 3?
            hoshizora_pixel = ImageGrab.grab(bbox = aqua_yukisaki).getpixel(left_hoshizora_point)
            if diff_pixel(hoshizora_pixel, original_utyuu) < 20:
                mode = MODE_SPACE
            else:
                mode = MODE_COMMON
            # As long as we have not suffer from 'extraction'
            while not owatta(image):
                # We should try to defend as we can
                while not mikiru(image, mode, aqua_yukisaki, debug):
                    image = ImageGrab.grab(bbox = aqua_yukisaki)
                time.sleep(0.5)
                image = ImageGrab.grab(bbox = aqua_yukisaki)
            # There should be some exit code if we won the fight
            # But I just got too lazy and failed to write it down
            # Anyway, Ctrl-C is your friend if you want to stop this script.

# Fight against taigo.
# The method is simple: if the space background is no longer dark, then there is taigo.
def fight_taigo(aqua_yukisaki):
    while True:
        image = ImageGrab.grab(bbox=aqua_yukisaki)
        pixel_left = image.getpixel(left_hoshizora_point)
        pixel_right = image.getpixel(right_hoshizora_point)
        if diff_pixel(pixel_left, original_utyuu) > 15:
            defend(DEFENSE_LEFT, aqua_yukisaki)
            continue
        if diff_pixel(pixel_right, original_utyuu) > 15:
            defend(DEFENSE_RIGHT, aqua_yukisaki)

# Take a quick shot of the game. Used for debugging.
def shot(aqua_yukisaki):
    image = ImageGrab.grab(bbox=aqua_yukisaki)
    image.show()
    image.save(Path().resolve() / 'debug.png')

if __name__ == '__main__':
    aqua_yukisaki = locate_aqua()
    # workload(aqua_yukisaki, debug=True)
    # fight_taigo(aqua_yukisaki)
    # shot(aqua_yukisaki)
    
