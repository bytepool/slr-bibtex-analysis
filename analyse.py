#!/usr/bin/env python3
"""
   Script to analyse bibtex files. 

   Before any real data extraction can begin, the bibtex file must be checked for duplicates.
  
   Process a single bibtex file (can contain the results of a single query, or all results combined)
   We extract:
    - number of entries
    - "word cloud" (term frequency, or better tf-idf) for all titles
    - "word cloud" (term frequency, or better tf-idf) for all abstracts
  
   Each of the following requires a corresponding list, uniformly formatted and without duplicates
   (authors, publication venue)
    - number of papers per author
    - number of papers per publication venue
  
   Each of the following requires a corresponding list, uniformly formatted and without duplicates,
   _and_ external correlation of the data, since organisation and country are not in the bibtex file.
   This must be correlated with the author information. 
    - number of papers per organisation
    - number of people per organisation
    - number of papers per country
    - number of people per country
    
   Also consider to feed author names back into search queries, to find possibly related work. 
  
   Write the output to a simple csv file?
  
   Possible csv header:
   Query; DOI: Author; PublicationType; PublicationVenue; PublicationYear; Title; Abstract; WordCount;
  
   Pub. Type: can be Journal or Conference
   Query:     is the query string which lead to this result
   DOI:       is document object identifier (unique for every scientific publication (see crossref.com)
"""

import bibtexparser
import wordlib
import os
import sys
import re
import string

# in the future files should be read from the "bibdata" folder
#data_dir = "bibdata"
data_dir = "bibtests"
#file_name = "1-entry.bib"
file_name = "query1.bib"
full_path = os.path.join(data_dir, file_name)

JOURNAL = "Journal"
CONFERENCE = "Conference"

# error codes for return values
ERR_NO_ENTRIES = 1


class Entry():
    """Datastructure for a bibtex entry. """
    def __init__(self, query_string="", authors=None, pub_type="", year=0, title="", abstract="", word_count=0, doi=""):
        self.query_string = query_string
        self.doi = doi
        self.authors = authors
        self.type = pub_type
        self.year = year
        self.title = title
        self.abstract = abstract
        self.word_count = word_count

    # Query; DOI: Authors; PublicationType; PublicationVenue; PublicationYear; Title; Abstract; WordCount;

def strip_unwanted_chars(s):
    """Strip unwanted characters from the given string. Might be slow, but gives the desired result."""
    s = s.replace("\n", " ")
    s = s.replace("{", "")
    s = s.replace("}", "")
    
    s = s.replace(")", "")
    s = s.replace("(", "")
    s = s.replace("[", "")
    s = s.replace("]", "")
    s = s.replace(":", "")
    s = s.replace("\"", "")
    s = s.replace(".", "")
    s = s.replace("?", "")
    s = s.replace("!", "")
    s = s.replace(",", "")
    return s

def strip_non_alphanum(s):
    """Strip all non alphanumeric characters, except space. This may be fast, but does not quite give the right output. The regexp might need more tuning, so use strip_unwanted_chars instead."""
    pattern = re.compile(r'([^\s\w]|_)+')
    return pattern.sub('', s)
    

def term_frequency(terms):
    """
    Calculate the relative frequency of all the terms in the given word list. 
    """
    return 0


def format_authors(authors_string):
    """
    Format the given author string in a uniform way. 
    """
    new_authors_string = ""
    authors = authors_string.split(" and ")

    for author in authors:
        if "," in author:
            #print("DEBUG: aut:", author)

            last_name, first_name = author.split(",")
            #print("DEBUG: ln, fn:", last_name, first_name)
            
            last_name = last_name.strip(" ")
            first_name = first_name.strip(" ")
            
            new_authors_string += "%s %s, " % (first_name, last_name)
        else:
            new_authors_string += author + ", "

    return new_authors_string[:-2]

def print_pretty_header(header):
    print("+" + ((len(header) + 2) * "-") + "+")
    print("| " + header + " |")
    print("+" + ((len(header) + 2) * "-") + "+") 

def print_nr_of_entries(entries):
    """ Prints the number of entries found in the parsed bibfile. """
    print_pretty_header("ENTRIES")
    print("There are %d entries in bibfile %s.\n" % (len(entries), file_name[:-4]))

def print_title_term_frequencies(entries):
    """
    Prints the term frequencies of all the titles. 
    """
    titles = ""
    for entry in entries:
        titles += entry['title'] + " "

    print_pretty_header("WORD FREQUENCIES - TITLES")
    print_term_frequencies(titles)
    
def print_abstract_term_frequencies(entries):
    """
    Prints the term frequencies of all the titles. 
    """
    abstracts = ""
    for entry in entries:
        if "abstract" in entry.keys():
            abstracts += entry['abstract'] + " "

    print_pretty_header("WORD FREQUENCIES - ABSTRACTS")
    print_term_frequencies(abstracts)

    
def print_term_frequencies(term_string):
    """
    Prints the term frequencies of all the words in the given string. 
    """
    lower_term_string = term_string.lower()
    term_string = strip_unwanted_chars(lower_term_string)
    #term_string2 = strip_non_alphanum(lower_term_string)
    #print(":DEBUG:\n\n\n" + term_string + "\n\n\n:DEBUG:")
    #print(":DEBUG:\n\n\n" + term_string2 + "\n\n\n:DEBUG:")

    wordlist = wordlib.createWordList(term_string)
    wordlist = wordlib.removeStopwords(wordlist, wordlib.stopwords)
    worddict = wordlib.wordListToFreqDict(wordlist)
    wordtuples = wordlib.sortFreqDict(worddict)

    for t in wordtuples:
        if t[1] is not "":
            print("%s: %d" % (t[1], t[0]))
    #print(worddict)
    print()


def print_author_list(entries):
    """Print a list of all authors in the bibfile."""
    author_list = []
    author_dict = {}
    for entry in entries:
        authors = entry["author"]
        authors = authors.replace("\n", " ")
        authors = format_authors(authors)
        author_list.append(authors)

    # author_list now contains properly formatted author strings for each paper
    # now extract individual authors from each entry, and put in a dict
    #print (author_list)

    for authors in author_list:
        l = authors.split(',')
        for author in l:
            author = author.strip()
            author = author.replace(".", "")
            if author in author_dict.keys():
                author_dict[author] = author_dict[author] + 1
            else:
                author_dict[author] = 1

    print("There are %d unique authors.\n" % len(author_dict.keys()))
    for author in author_dict.keys():
        print("%s co-authored %d papers." % (author, author_dict[author]))
    #print(author_dict)

def remove_duplicate_entries(entries):
    """Try to identify and remove duplicate entries based on ID and title."""
    #print("Len before dup removal:", len(entries))
    new = []
    seen_id = set()
    seen_title = set()
    
    for entry in entries:
        if (entry["ID"] not in seen_id) and (entry["title"] not in seen_title):
            seen_id.add(entry["ID"])
            seen_title.add(entry["title"])
            new.append(entry)
    #print("Len after dup removal:", len(new))
    return new
    
def __main__():

    with open(full_path) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    entries = bib_database.entries

    if not entries:
        print("No bibtex entries found in %s. Aborting!" % full_path, file=sys.stderr)
        exit(ERR_NO_ENTRIES)

    print("\nAnalysing %s...\n" % full_path)

    entries = remove_duplicate_entries(entries)
    print_nr_of_entries(entries)
    #print_title_term_frequencies(entries)
    #print_abstract_term_frequencies(entries)
    print_author_list(entries)

if __name__ == "__main__":
    __main__()



