#!/usr/bin/env python3

import bibtexparser


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

