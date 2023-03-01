import random
import time
from colorama import Fore, Style, init
from pynput import keyboard
import msvcrt
import atexit


import util
from board import PrintBoard
from solver import FindPossibleSolutions

from validGuesses import VALID_GUESSES
from wordlist import WORDLIST

# CONSTS
WORD_LENGTH = 5
MAX_GUESSES = 5
CORRECT_WORD = random.choice(WORDLIST)

# Vars
currentGuesses : list[str] = []
discoveredCorrectIndexes : list[tuple[int, str]] = []
discoveredIncorrectIndexes : list[tuple[int, str]] = [] 
discoveredIncorrectLetters : list[str] = []

### Initialize game
init()
random.seed(time.time())

def exit_handler():
    print(f"\033[17;1H", end="")
atexit.register(exit_handler)


guess = ""
prevCurrentTyping = ""
currentTyping = ""
enterPressed = False
def on_press(key):
  global currentTyping, enterPressed
  try: # Normal key press
    if(key.char.isalpha() and len(currentTyping) < 5):
      currentTyping += key.char
  except AttributeError:
    if(key == keyboard.Key.esc):
      currentTyping = ""
    elif(key == keyboard.Key.backspace):
      if(len(currentTyping) > 0):
        currentTyping = currentTyping[:-1]
    elif(key == keyboard.Key.enter):
      enterPressed = True
      while msvcrt.kbhit():
        msvcrt.getch()


# Collect events until released
with keyboard.Listener(on_press=on_press) as listener:
  ### Start playing game
  while True:
    util.ClearScreen()    
    PrintBoard(currentGuesses, CORRECT_WORD, discoveredCorrectIndexes, discoveredIncorrectIndexes, discoveredIncorrectLetters, currentTyping)
    while True: # Get guess input
      if(prevCurrentTyping != currentTyping):
        prevCurrentTyping = currentTyping
        util.ClearScreen()
        PrintBoard(currentGuesses, CORRECT_WORD, discoveredCorrectIndexes, discoveredIncorrectIndexes, discoveredIncorrectLetters, currentTyping)
      elif(enterPressed):
        enterPressed = False
        guess = currentTyping
        currentTyping = ""
        if(len(guess) == WORD_LENGTH and guess.isalpha() and guess in VALID_GUESSES): # If valid guess move on to displaying the result
          currentGuesses.append(guess)
          break
        
        prevCurrentTyping = ""
        if(guess == "h"):
          errorLine = FindPossibleSolutions(VALID_GUESSES, discoveredCorrectIndexes, discoveredIncorrectIndexes, discoveredIncorrectLetters)
        elif(len(guess) == WORD_LENGTH and guess.isalpha()): # If valid guess but not in wordlist
          errorLine = f"{Fore.RED}'{guess}' is not a real word.{Style.RESET_ALL}"
        else: # Else invalid guess
          errorLine = f"{Fore.RED}'{guess}' is not a valid guess.{Style.RESET_ALL}"
        util.ClearScreen()
        PrintBoard(currentGuesses, CORRECT_WORD, discoveredCorrectIndexes, discoveredIncorrectIndexes, discoveredIncorrectLetters, currentTyping, errorLine = errorLine)
      
      time.sleep(0.1)    

    # Determine if win or lose or continue if neither
    if(guess == CORRECT_WORD):
      util.ClearScreen()
      PrintBoard(currentGuesses, CORRECT_WORD, discoveredCorrectIndexes, discoveredIncorrectIndexes, discoveredIncorrectLetters, state ="Win",
        errorLine = f"{Fore.GREEN}Your guess is the correct answer! You win!!!{Style.RESET_ALL}")
      break
    elif(len(currentGuesses) >= MAX_GUESSES):
      util.ClearScreen()
      PrintBoard(currentGuesses, CORRECT_WORD, discoveredCorrectIndexes, discoveredIncorrectIndexes, discoveredIncorrectLetters, state ="Lose",
        errorLine = f"{Fore.RED}Unfortunately you are of of guesses. The correct answer was {Fore.GREEN}{CORRECT_WORD}{Fore.RED}. Better luck next time!{Style.RESET_ALL}")
      break

while msvcrt.kbhit():
  msvcrt.getch()
exit_handler()
