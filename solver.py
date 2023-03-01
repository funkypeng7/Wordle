
def FindPossibleSolutions(wordlist : list[str], discoveredCorrectIndexes : list[tuple[int, str]], discoveredIncorrectIndexes : list[tuple[int, str]], discoveredIncorrectLetters : list[str]):
    # Remove duplicates
    discoveredCorrectIndexes = list(dict.fromkeys(discoveredCorrectIndexes))
    discoveredIncorrectIndexes = list(dict.fromkeys(discoveredIncorrectIndexes))
    discoveredIncorrectLetters = list(dict.fromkeys(discoveredIncorrectLetters))

    def valid(word):
        for index, letter in discoveredCorrectIndexes: # Check correct letter correct place
            if(word[index] != letter):
                return False
        
        for index, letter in discoveredIncorrectIndexes: # Confirm word contains letters that are known to be in that word
            if(not letter in word):
                return False
            if(word[index] == letter):
                return False

        for letter in discoveredIncorrectLetters: # Remove word containing letters that are know to be incorrect
            if(letter in word):
                return False

        return True

    return list(filter(valid, wordlist))