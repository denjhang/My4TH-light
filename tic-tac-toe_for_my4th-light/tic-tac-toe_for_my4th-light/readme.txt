
This archive contains the files that you need to build your own
Tic Tac Toe game for your My4TH light computer board.

The project is based on two of Adafruit's PCF8575 breakout boards:
  https://www.adafruit.com/product/5611

The file tictactoe-screens.txt contains the Forth programme for the game.
Use the my4th transfer tool to upload it onto the My4TH light board with
this command:

$ my4th write /dev/ttyUSB0 10 tictactoe-screens.txt

The game will be stored in the EEPROM blocks 10 to 20.
On the My4TH light board you have to enter

10 20 thru

to compile the programme. When the compilation is finished, enter

run 

to start the game. But I suggest saving it as a binary image
in the EEPROM first:

25 save-image

If you want to play the game again (e.g. after a reset), you can simply
load and run the binary file, which is much faster than recompiling the game:

25 run-image


Have fun!

dennis_k@freenet.de
http://mynor.org/my4th
