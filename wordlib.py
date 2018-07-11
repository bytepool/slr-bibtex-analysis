"""
 Almost all code in this little library is  taken from: 
 William J. Turkel and Adam Crymble, "Counting Word Frequencies with Python," The Programming Historian 1 (2012), https://programminghistorian.org/en/lessons/counting-frequencies.
 which is licenced under Creative Commons 4.0.
"""

def createWordList(inputstring):
    """ 
    Create a word list from the input string. 
    """
    return inputstring.split(" ")


def removeStopwords(wordlist, stopwords):
    """
    Given a list of words, remove any that are
    in a list of stop words.
    """
    return [w for w in wordlist if w not in stopwords]

def wordListToFreqDict(wordlist):
    """ 
    Given a list of words, return a dictionary of word-frequency pairs.
    Copyright (c) 2012 - 2018 William J. Turkel and Adam Crymble
    """
    wordfreq = [wordlist.count(p) for p in wordlist]
    return dict(zip(wordlist,wordfreq))


def sortFreqDict(freqdict):
    """
    Sort a dictionary of word-frequency pairs in order of descending frequency.
    Copyright (c) 2012 - 2018 William J. Turkel and Adam Crymble
    """
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux

# from http://ir.dcs.gla.ac.uk/resources/linguistic_utils/stop_words
stopwords = ["a", "about", "above", "across", "after", "afterwards", "again", 
                 "against", "all", "almost", "alone", "along", "already", "also", "although", 
                 "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", 
                 "another", "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are", 
                 "around", "as", "at", "back", "be", "became", "because", "become", "becomes", 
                 "becoming", "been", "before", "beforehand", "behind", "being", "below", 
                 "beside", "besides", "between", "beyond", "bill", "both", "bottom", "but", "by", 
                 "call", "can", "cannot", "cant", "co", "computer", "con", "could", "couldnt", 
                 "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", 
                 "each", "eg", "eight", "either", "eleven", "else", "elsewhere", "empty", 
                 "enough", "etc", "even", "ever", "every", "everyone", "everything", 
                 "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", 
                 "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", 
                 "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", 
                 "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", 
                 "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "i", 
                 "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", 
                 "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", 
                 "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", 
                 "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", 
                 "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", 
                 "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", 
                 "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", 
                 "ours", "ourselves", "out", "over", "own", "part", "per", "perhaps", "please", 
                 "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", 
                 "serious", "several", "she", "should", "show", "side", "since", "sincere", 
                 "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", 
                 "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", 
                 "that", "the", "their", "them", "themselves", "then", "thence", "there", 
                 "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", 
                 "thick", "thin", "third", "this", "those", "though", "three", "through", 
                 "throughout", "thru", "thus", "to", "together", "too", "top", "toward", 
                 "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", 
                 "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", 
                 "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", 
                 "whereupon", "wherever", "whether", "which", "while", "whither", "who", 
                 "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", 
                 "would", "yet", "you", "your", "yours", "yourself", "yourselves"]
