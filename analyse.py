#!/usr/bin/env python3

# Process a single bibtex file (can contain the results of a single query, or all results combined)
# We extract:
#  - number of entries
#  - word cloud for all titles
#  - word cloud for all abstracts
#  - number of papers per author
#  - number of papers per publication venue

#  - number of papers per organisation
#  - number of people per organisation
#  - number of papers per country
#  - number of people per country
#  
# This implies a second DB with author affiliations
# Also consider to feed author names back into query search. 
#
# Write the output to a simple csv file. 

# csv header:
# Query; DOI: Author; PublicationType; PublicationVenue; PublicationYear; Title; Abstract; WordCount;

# Pub. Type can be Journal or Conference. 
# Query is the query string which lead to this result. 
# DOI is document object identifier:
#   should be unique for every scientific publication (see crossref.com). 

import bibtexparser

JOURNAL = "Journal"
CONFERENCE = "Conference"


def preprocess(entry):
    """Simple function to remove unwanted characters and strings from entries"""
    entry = entry.replace("\n", " ")
    entry = entry.replace("{", "")
    entry = entry.replace("}", "")
    return entry

def process_authors(authors_string):
    new_authors_string = ""
    authors = authors_string.split("and")
    #print (authors)
    for author in authors:
        if "," in author:
            last_name, first_name = author.split(",")
            
            last_name = last_name.strip(" ")
            first_name = first_name.strip(" ")
            
            new_authors_string += "%s %s, " % (first_name, last_name)
        else:
            new_authors_string += author
            
    return new_authors_string[:-2]

def __main__():

    with open('query1.bib') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    
    #print(bib_database.entries[0])
    
    for entry in bib_database.entries:
        title = preprocess(entry["title"])
        authors = preprocess(entry["author"])

        authors = process_authors(authors)
        
        print("Title: %s\nAuthors: %s" % (title, authors))

        if "abstract" in entry.keys():
            print("Abstract:\n%s\n" % (entry["abstract"]))
        else:
            print()

if __name__ == "__main__":
    __main__()




class Article():
    """Datastructure for an article. """
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

