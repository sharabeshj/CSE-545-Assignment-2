"""
    Please implement an exhaustive search algorithm to attack a simpler version of the Vigenère cipher
    built at question 3 (key length can be 1-3, and cipher text must use upper case letters). Use your
    implemented attack to infer the key for the following plaintext and cipher text pairs
"""

import itertools, re
from dependencies import vigenereCipher, pyperclip, freqAnalysis, detectEnglish

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
NUM_MOST_FREQ_LETTERS = 4
MAX_KEY_LENGTH = 3
NONLETTERS_PATTERN = re.compile('[^A-Z]')

def findRepeatSequencesSpacings(message):
    message = NONLETTERS_PATTERN.sub("", str(message).upper())
    seqSpacings = {}
    for seqLen in range(3,6):
        for seqStart in range(len(message) - seqLen):
            seq = message[seqStart:seqStart+seqLen]

            for i in range(seqStart+seqLen, len(message)-seqLen):
                if message[i:i+seqLen] == seq:
                    if seq not in seqSpacings:
                        seqSpacings[seq] = []
                    
                    seqSpacings[seq].append(i-seqStart)
    
    return seqSpacings

def getUsefulFactors(num):
    if num < 2:
        return []
    
    factors = []

    for i in range(2, MAX_KEY_LENGTH+1):
        if num % i == 0:
            factors.append(i)
            factors.append(int(num/i))
        
        if 1 in factors:
            factors.remove(1)
        return list(set(factors))

def getMostCommonFactors(seqFactors):
    factorCounts = {}

    for seq in seqFactors:
        factorList = seqFactors[seq]
        for factor in factorList:
            if factor not in factorCounts:
                factorCounts[factor] = 0
            factorCounts[factor] += 1
    factorsByCount = []
    for factor in factorCounts:
        if factor <= MAX_KEY_LENGTH:
            factorsByCount.append((factor, factorCounts[factor]))
    
    factorsByCount.sort(key= lambda x: x[1], reverse=True)

    return factorsByCount

def kasiskiExamination(cipherText):
    repeatedSeqSpacings = findRepeatSequencesSpacings(cipherText)

    seqFactors = {}
    for seq in repeatedSeqSpacings:
        seqFactors[seq] = []
        for spacing in repeatedSeqSpacings[seq]:
            seqFactors[seq].extend(getUsefulFactors(spacing))

    factorsByCount = getMostCommonFactors(seqFactors)

    allLikelyKeyLengths = []
    for twoIntTuple in factorsByCount:
        allLikelyKeyLengths.append(twoIntTuple[0])

    return allLikelyKeyLengths


def getNthSubkeysLetter(n, keyLength, message):
    message = NONLETTERS_PATTERN.sub("", message)
    
    i = n-1
    letters = []
    while i < len(message):
        letters.append(message[i])
        i += keyLength
    return "".join(letters)

def attemptHackWithKeyLength(cipherText, mostLikelyKeyLength):
    cipherTextUp = str(cipherText).upper()
    allFreqScores = []

    for nth in range(1, mostLikelyKeyLength+1):
        nthLetters = getNthSubkeysLetter(nth, mostLikelyKeyLength, cipherTextUp)

        freqScores = []
        for possibleKey in LETTERS:
            decryptedText = vigenereCipher.decryptMessage(possibleKey, nthLetters)
            keyAndFreqMatchTuple = (possibleKey, freqAnalysis.englishFreqMatchScore(decryptedText))
            freqScores.append(keyAndFreqMatchTuple)
        
        freqScores.sort(key=lambda x: x[1], reverse=True)

        allFreqScores.append(freqScores[:NUM_MOST_FREQ_LETTERS])

    for i in range(len(allFreqScores)):
        print('Possible letters for letter %s of the key: ' % (i + 1), end='')
        for freqScore in allFreqScores[i]:
            print('%s ' % freqScore[0], end='')
        print()
    
    for indexes in itertools.product(range(NUM_MOST_FREQ_LETTERS), repeat=mostLikelyKeyLength):
        possibleKey = ""
        for i in range(mostLikelyKeyLength):
            possibleKey += allFreqScores[i][indexes[i]][0]

            print('Attempting with key: %s' % (possibleKey))

        decryptedText = vigenereCipher.decryptMessage(possibleKey, cipherTextUp)

        if detectEnglish.isEnglish(decryptedText):
            origCase = []
            for i in range(len(cipherText)):
                if str(cipherText[i]).isupper():
                    origCase.append(decryptedText[i].upper())
                else:
                    origCase.append(decryptedText[i].lower())
            decryptedText = "".join(origCase)
        
            print('Possible encryption hack with key %s:' % (possibleKey))
            print(decryptedText[:200])
            print()
            print('Enter D for done, or just press Enter to continue hacking:')
            res = input(">")

            if res.strip().upper().startswith("D"):
                return decryptedText
    
    return None
            
        

def hackVigenere(cipherText):
    allLikelyKeyLengths = kasiskiExamination(cipherText)
    keyLengthStr = ""
    for keyLength in allLikelyKeyLengths:
        keyLengthStr += "%s" %(keyLength)
        print('Kasiski Examination results say the most likely key lengths are: ' + keyLengthStr + '\n')
    hackedMessage = None
    for keyLength in allLikelyKeyLengths:
        print('Attempting hack with key length %s (%s possible keys)...' % (keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
        hackedMessage = attemptHackWithKeyLength(cipherText, keyLength)
        if hackedMessage != None:
            break
    
    if hackedMessage == None:
        print('Unable to hack message with likely key length(s). Brute-forcing key length...')
        for keyLength in range(1, MAX_KEY_LENGTH+1):
            if keyLength not in allLikelyKeyLengths:
                print('Attempting hack with key length %s (%s possible keys)...' % (keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
            hackedMessage = attemptHackWithKeyLength(cipherText, keyLength)
            if hackedMessage != None:
                break
    return hackedMessage


def main():
    cipherText = "EUCDRHEVNEWYYQCZHLWLNC"
    hackedMessage = hackVigenere(cipherText)

    if hackedMessage != None:
        print('Copying hacked message to clipboard:')
        print(hackedMessage)
        pyperclip.copy(hackedMessage)
    else:
        print('Failed to hack encryption')
    

if __name__ == "__main__":
    main()