from colorama import Fore, Style
import os

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
def PrintBoard(currentGuesses : list[str], correctWord : str, discoveredCorrectIndexes : list[tuple[int, str]] = [], discoveredIncorrectIndexes : list[tuple[int, str]] = [], discoveredIncorrectLetters : list[str] = [], typingGuess : str = "", state : str = "Play", errorLine : str = ""):
    correctLetters : list[str] = list(correctWord)
    discoveredCorrectPlaces : list[str] = []
    discoveredCorrectLetters : list[str] = []

    discoveredCorrectIndexes[:] = []
    discoveredIncorrectIndexes[:] = []
    discoveredIncorrectLetters[:] = []
    
    titleColour = Style.RESET_ALL
    if(state == "Win"):
        titleColour = Fore.GREEN
    elif(state == "Lose"):
        titleColour = Fore.RED
    # Print guesses
    print(f'''{titleColour} __      __                .___.__          
/  \    /  \___________  __| _/|  |   ____  
\   \/\/   /  _ \_  __ \/ __ | |  | _/ __ \ 
 \        (  <_> )  | \/ /_/ | |  |_\  ___/ 
  \__/\  / \____/|__|  \____ | |____/\___  >
       \/                   \/           \/ {Style.RESET_ALL}
    ''')
    for word in currentGuesses:
        toPrint = "                    "
        for index, letter in enumerate(word):
            if(letter == correctWord[index]): # Correct letter in correct place - Green
                toPrint += Fore.GREEN
                discoveredCorrectIndexes.append((index, letter))
                discoveredCorrectPlaces.append(letter)
            elif(letter in correctLetters): # Correct letter in incorrect place - Yellow
                toPrint += Fore.YELLOW
                discoveredIncorrectIndexes.append((index, letter))
                discoveredCorrectLetters.append(letter)
            else:
                toPrint += Fore.RED
                discoveredIncorrectLetters.append(letter)
            toPrint += letter + Style.RESET_ALL # Add letter to string
        print(toPrint)
    
    if(len(currentGuesses) < 5):
        print(f"                    {Fore.BLUE}{typingGuess}{Style.RESET_ALL}{'x'*(5 - len(typingGuess))}")
        for _ in range(4-len(currentGuesses)):
            print(f"                    xxxxx")

    # Print remaining letters
    toPrint = "         "
    for letter in ALPHABET:
        if(letter in discoveredCorrectPlaces):
            toPrint += Fore.GREEN
        elif(letter in discoveredCorrectLetters):
            toPrint += Fore.YELLOW
        elif(letter in discoveredIncorrectLetters):
            toPrint += Fore.RED
        toPrint += letter + Style.RESET_ALL
    print(toPrint + "\n")

    if(errorLine != ""):
        print(errorLine)

    x = 21+len(typingGuess)
    if(len(typingGuess) == 5): x -= 1
    y = 8+len(currentGuesses)
    print(f"\033[{y};{x}H", end="")

    

if(__name__ == '__main__'):
    PrintBoard(["tests", "teirs"], "tells",typingGuess = "te")
    import time
    time.sleep(2)