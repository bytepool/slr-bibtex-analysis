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
    """
    Strip unwanted characters from the given string. Slow, but gives the desired result.
    """
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
    """
    Strip all non alphanumeric characters, except space. 
    This may be fast, but does not give the desired output, the regexp needs more tuning. 
    Use strip_unwanted_chars instead. 
    """
    pattern = re.compile(r'([^\s\w]|_)+')
    return pattern.sub('', s)
    
def format_authors(authors_string):
    """
    Format the given author string in a uniform way. 
    """
    new_authors_string = ""
    if " and " in authors_string:
        authors = authors_string.split(" and ")
    else:
        authors = authors_string.split(", ")
        
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
    fill_length = 20 - (int(len(header) / 2.))
    header_len = len(header) + 2
    
    line_filler = fill_length * "-"
    head_filler = fill_length * " "
    
    line = "+" + line_filler + (header_len * "-") + line_filler + "+"
    print(line)
    print("| " + head_filler + header + head_filler + " |")
    print(line)
    print()


def sort_dict_by_value(d, reverse=True):
    """
    Output a sorted tuple of two-tuples (key, value) of the given dictionary, 
      where the second entry (value) is the item to be sorted. 
    """
    tmp = [(d[key], key) for key in d]
    #tmp = [(key, d[key]) for key in d]
    tmp.sort()
    if reverse:
        tmp.reverse()
    res_tuple = [(b, a) for (a, b) in tmp]
    return res_tuple

def sort_dict_by_key(d, reverse=True):
    """
    Output a sorted tuple of two-tuples (key, value) of the given dictionary, 
      where the first entry (key) is the item to be sorted. 
    """
    tmp = [(key, d[key]) for key in d]
    tmp.sort()
    if reverse:
        tmp.reverse()
    return tmp

def print_tuples(tuples):
    """
    Print a list of two-tuples. 

    For example, for the tuples ((a, b), (c, d)) the output will be:
    a: b
    c: d
    """
    l = [str(k) for k, v in tuples]
    max_len = len(max(l, key=len)) + 1
    #if max_len > 50:
    #    max_len = 50
        
    for k, v in tuples:
        spaces = (" " * (max_len - len(str(k))))
        if type(v) is int:
            print("%s:%s%5d" % (k, spaces, v))
        elif type(v) is str:
            print("%s:%s%s" % (k, spaces, v))
        else:
            print("Type in tuple '%s' not recognized, skipping." % t)

    print()

    
def idenfity_duplicate_entries(entries):
    """
    Try to identify duplicate entries based on ID, year, authors and title. 
    TODO: Add year check for both (ID and title). 
    Consider string distance for title (scale distance with length) and authors. 
    """

def remove_duplicate_entries(entries):
    """
    Try to identify and remove duplicate entries based on ID, year, authors and title. 
    Since entries are removed automatically, the identification must have a very high degree
    of certainty. 
    TODO: improve certainty by adding year checks for both ID and title. 
    """
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

    wordtuples = sort_dict_by_value(worddict)
    print_tuples(wordtuples)

def print_author_list(entries):
    """Print a list of all authors in the bibfile."""
    author_list = []
    author_dict = {}
    for entry in entries:
        if "author" in entry.keys():
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

    print_pretty_header("AUTHORS")
    print("There are %d unique authors.\n" % len(author_dict.keys()))
    sorted_tuples = sort_dict_by_key(author_dict, reverse=False)
    print_tuples(sorted_tuples)
    
    #for author in author_dict.keys():
    #    spaces = (" " * (40 - len(author)))
    #    print("%s%s co-authored %d papers." % (author, spaces, author_dict[author]))


def print_publication_venues(entries):
    """Print a list of all publication venues in the bibfile."""
    d = {}
    for entry in entries:
        if "journal" in entry.keys():
            venue = entry["journal"]
        elif "booktitle" in entry.keys():
            venue = entry["booktitle"]
        else:
            venue = ""
            
        venue = venue.replace("\n", " ")
        if venue in d.keys():
            d[venue] = d[venue] + 1
        else:
            d[venue] = 1

    print_pretty_header("PUBLICATION VENUES")
    print("There are %d unique publication venues.\n" % len(d.keys()))
    sorted_tuples = sort_dict_by_value(d)
    print_tuples(sorted_tuples)
    
    
def print_entry_summary(entries, entry_type, sort_by_value=True):
    """Print a list of all entries of the given entry type in the bibfile."""
    d = {}
    for entry in entries:
        if entry_type in entry.keys():
            s = entry[entry_type]
        else:
            s = ""
            
        s = s.replace("\n", " ")
        if s in d.keys():
            d[s] = d[s] + 1
        else:
            d[s] = 1

    header = entry_type + "s"
    print_pretty_header(header.upper())
    print("There are %d unique %s.\n" % (len(d.keys()), header))
    if sort_by_value:
        sorted_tuples = sort_dict_by_value(d)
    else:
        sorted_tuples = sort_dict_by_key(d)
    print_tuples(sorted_tuples)
    
    
def __main__():

    parser = bibtexparser.bparser.BibTexParser()
    parser.ignore_nonstandard_types = False
    #parser.homogenise_fields = False
    #parser.common_strings = False

    with open(full_path) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file, parser)

    entries = bib_database.entries

    if not entries:
        Print("No bibtex entries found in %s. Aborting!" % full_path, file=sys.stderr)
        exit(ERR_NO_ENTRIES)

    print("\nAnalysing %s...\n" % full_path)

    #entries = remove_duplicate_entries(entries)
    
    print_nr_of_entries(entries)
    print_title_term_frequencies(entries)
    print_abstract_term_frequencies(entries)
    print_author_list(entries)
    print_publication_venues(entries)
    print_entry_summary(entries, "publisher")
    print_entry_summary(entries, "organization")
    print_entry_summary(entries, "year")
    print_entry_summary(entries, "ENTRYTYPE")
    
    
if __name__ == "__main__":
    __main__()

