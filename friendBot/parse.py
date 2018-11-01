import pickle
import parsefunctions

endOfLineID = 'eol123'


listOfMessages = parsefunctions.listOfMessages('The Latin Taxi - yeet.txt')

corpus = parsefunctions.gen_corpus(listOfMessages, endOfLineID)

bigrams = parsefunctions.gen_bigrams(corpus, endOfLineID)

wordDictBigramFreq = wordSequenceFreq(bigrams)

#save the bigram frequencies as serialised object
with open('lexicon.pkl', 'wb') as f:
    pickle.dump(wordDictBigramFreq, f)