def listOfMessages(textfile):
    """Returns a list of messages contained in textfile.
        A message is defined by being on a new line.
        Also removes timestamps and sender information."""
    clean = []

    with open(textfile, encoding='utf-8') as f:
        lines = f.read().splitlines()

    for i in lines:
        cleanedLine = i.strip()
        if cleanedLine and cleanedLine[0] != '[':#removes lines containing message timestamp and sender
            clean.append(cleanedLine)
    
    return clean

def gen_corpus(messagesList, eolID, textfile='cleanText.txt'):
    """Converts a list of messages (separated by newlines)
     into a list of words (separated by blanks) (i.e. generates a corpus).
     Also removes URLs, Tonic bot commands and discord user mentions from the corpus."""

    corpus=[]

    with open(textfile, 'w', encoding='utf-8') as f:
        eolModifier = ' ' + eolID + '\n'
        f.write(eolModifier.join(messagesList))#Saves a .txt file with each message in messagesList on a new line and adds end of line id

    textData = open(textfile, encoding='utf-8').read()
    stringlst = textData.split()#Splits entire text into strings of words (defined as being separated by blanks), appended to a list

    for i in range(len(stringlst)):#check for http links, ! tonic commands and @ mentions and remove from corpus 
        if 'http' in stringlst[i] or stringlst[i].startswith(('@','!')):
            corpus.append(stringlst[i])
    
    return corpus

def gen_bigrams(corpus, eolID):
    #creates iterateable object containing 2-grams of words in corpus
    for i in range(len(corpus)-1):
        if corpus[i] != eolID:#ignores end of line identifier as first word
            yield (corpus[i], corpus[i+1])

def wordSequenceFreq(bigrams):
    """Counts frequency of 2-word sequences using bigrams,
        and returns them in the form of a one-to-many dictionary (with duplicate values)
        using the first word in the sequence as key."""
    
    word_dict = {}
    for w_1, w_2 in bigrams:
        if w_1 in word_dict.keys():
            word_dict[w_1].append(w_2)
        else:
            word_dict[w_1] = [w_2]
    
    return word_dict