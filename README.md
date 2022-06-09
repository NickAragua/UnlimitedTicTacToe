# UnlimitedTicTacToe
A python implementation of a border-less version of the game TicTacToe

Uses wxPython for graphics

Start up using FrontEnd.py
Left click to place an X or O, whichever one is the current player
Right click to make an automatic AI move for the current player
Left click and drag to move the board around

Victory is highlighted when first player places five markers in a row

Pro tips:
- Try to set yourself up so that you can place multiple "three in a row" with one move
- If you see an opponent having "three in a row" with no blocked ends, block one of the ends
- If you see an opponent having two "threes in a row" with no blocked ends, you've very likely lost
- If you see an opponent having "four in a row" with no blocked ends, you've already lost and should concede
