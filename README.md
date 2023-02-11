# AquaAfter Minigame Cheat Script
## Description
A python script for cheating in AquaAfter Minigame.

There was a crack for Himawari Aqua After by *浦岛水坝汉化组*, and they have made a minigame cheating patch;
Unfortunately the patch is bound to there crack and cannot work with the original version of the game.
If you are familiar with Chinese and willing to play a beautified version of the game, you should check their crack.

This script does not crack the game, but it may help you win the Aries' attack minigame and read the bonus text(no more than 8 lines though).

## The way it works
1. Search for the Window handle of Himawari Aqua After and acquire its position. 
2. Keep making screenshots of the game through Pillow.
3. Check some pixels in the screenshots and figure out whether there is an attack.
4. Simulate mouse click to defend the attack if there is one.

## Usage
Test environment: Windows10 21H2, python 3.10.3

1. Open the game and make sure its window is not minimized.
2. Open the script with any editor you prefer.
3. Uncomment the line 147 or line 148 according to the level. Line 147 is for Aries and line 148 is for Taigo.
4. Run the script by `python aqua_aries.py`. Do not move or resize the game window after this.
5. Switch to the game. Make sure it is at the top of all other windows.
6. Pick a level and start.
7. After the level, always use Ctrl+C to stop the script.

If you are playing level 3 and just passed Aries, you should stop the script, comment line 147 and uncomment line 148, rerun the script, 
then start the fight against taigo. There is no auto-switching codes.

## Notes
- The script is poor in quality and filled with bugs. It will not report errors if there is one. It may work, and it may not. It is highly recommended to adapt the script to your own environment.
- The game should be run in Japanese environment. Consider LocaleEmulater if your Windows is not set to Japanese one.
- The script failed to defend about 5% attacks from Aries, but as the player have 2 lifes...
- The script do not support 3-times attack mode, as there is another yellow-fying filter under the mode. However, the script may work if all the colors got rectified.
- The script works best if the game window is near the upleft corner of your screen, maybe.
- I wrote the script in a few hours just after I finished Himawari and Himawari Aqua After, and I have no experience in writing cheat scripts. Please tell me if you have some better ideas.
- Himawari and its Fan disc is a good vn, but...
