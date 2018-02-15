from bs4 import BeautifulSoup
import re
import os
import operator
from collections import OrderedDict
from string import maketrans
Do_Case_Folding = True
Remove_Punctuation = True

#corpus.py parses the raw html documents and the given set of queries in a text document.

#Dictionay Holds Key as QueryId and Value as QueryText
#Example : Dictionary (1 : the query to be run in the retrieval system)
dict_id_queryText = {}

#Writing the cleaned Corpus into file
def write_Cleaned_Corpus(name,consider_special_punctuation,dest_path):
    filename = name.split(".html")
    name = filename[0] + ".txt"
    #print(cleaned_name)
    f = open (dest_path + '\\' + name, 'w')
    f.write(consider_special_punctuation)
    f.close()

#Removing Space and multiple new line char
def remove_multiple_space(raw_content):
    content_with_single_space = re.sub("\s\s+", " ", raw_content)
    content_with_no_lines = re.sub("\n", " ",content_with_single_space)
    return content_with_no_lines

#Strip the incoming String of special characters and
#Other unimportant punctuation
def remove_punctuation(remove_citation_from_content):
    incoming_exception = "!\"#$%&()*+/;<=>?@[\]^_`{|}~?"
    cleaned_str = "                             "
    transform = maketrans(incoming_exception, cleaned_str)
    content_without_punctuation = remove_citation_from_content.translate(transform)
    return content_without_punctuation

#Strip the incoming String punctuation like . , and '
def remove_special_punctuation(lower_case_content):
    removeexp = r"(?<=\D)[.,':]|[.,':](?=\D)"
    cleaned_str = (re.sub(removeexp,' ',lower_case_content))
    return cleaned_str

#Convert the incoming string to lower case
def convert_to_lower(punctuation_removed):
    return punctuation_removed.lower()

#Removing Citations if Present ex. [1],<1>,{1}
def remove_citation(content_with_formula_removed):
    remove_citation = (re.sub('\[[0-9.,]*\]', '', content_with_formula_removed))
    return remove_citation

def clean_query(initial_query):

    #Convert from utf-8 to string
    initial_query = str(initial_query.encode('ascii','ignore').decode('ascii'))

    # Remove Citations if present
    remove_citation_from_query  = remove_citation(initial_query)

    #Remove all Punctuations other than "." "," and "-" " ' "
    punctuation_removed = remove_punctuation(remove_citation_from_query)

    # Remove Punctuation like "." "," and " ' "
    #Preserve these puncuation to consider the fact that they might appear
    #Between numbers Strip if they appear between query text
    consider_special_punctuation = remove_special_punctuation(punctuation_removed)

    # convert the Query Text to lower case
    lower_case_content = convert_to_lower(consider_special_punctuation)

    # Remove extra spaces and new line and remove new line char
    content_with_no_space = str(remove_multiple_space(lower_case_content))

    return content_with_no_space


def extract_Query(filename_Path,dest_path_query):
    text_content = []

    infile = open(filename_Path, "r")
    contents = infile.read()

    # Soup to parse the query document
    soup = BeautifulSoup(contents, 'lxml')
    tags_to_consider = ['doc']

    #GET Query and Query_ID in a List
    for body_content in soup.find_all(tags_to_consider):
        text_content.append(body_content.text.strip())

    #Each list entry(id query) into a key,value pair in dictionary
    #Dictionary (Queryid, QueryText)
    for entry in text_content:
        check = entry.split(" ",1)
        # Clean Query Processes the query text in the same way as the processing done
        #during indexing the documents
        dict_id_queryText[int(str(check[0].encode('ascii', 'ignore').decode('ascii')))] = clean_query(check[1])

    query_string=""
    f=open(dest_path_query,"w+")
    
    

    for k in (sorted (dict_id_queryText.iterkeys())):
        query_string+=str(k)+" "+dict_id_queryText[k]+"\n"
    f.write(query_string.strip())
    f.close()


def generate_clean_corpus(filename,name,dest_path):
    text_content = []
    raw_content = " "

    # Soup to parse the document
    soup = BeautifulSoup(open (filename), "html.parser")

    #List of tags to consider while parsing
    tags_to_consider = ['pre']

    # GET all useful content from page using specified tag
    for body_content in soup.find_all(tags_to_consider):
            text_content.append(body_content.text)

    #Convert the content into one String
    for entry in text_content:
        raw_content = " ".join(text_content)

    #Remove Citations
    remove_citation_from_content = remove_citation(raw_content)

    #Convert from utf-8 to string
    str_with_punctuation = str(remove_citation_from_content.encode('ascii','ignore').decode('ascii'))

    #Remove all Punctuations other than "." "," and "-" " ' "
    punctuation_removed = remove_punctuation(str_with_punctuation)

    #convert to lower case
    if Do_Case_Folding:
        lower_case_content = convert_to_lower(punctuation_removed)

    #Retain , and . if it is in between number else remove
    if Remove_Punctuation:
        consider_special_punctuation = remove_special_punctuation(lower_case_content)

    # Remove extra spaces and new line and remove new line char
    content_with_no_space = str(remove_multiple_space(consider_special_punctuation))

    #Crate the cleaned Corpus in the specified destination path
    write_Cleaned_Corpus(name,content_with_no_space,dest_path)


def main():
    #Obtain and Process Raw Queries
    source_path_raw_copus = raw_input("Please enter the full path where the raw documents are present,\n"
                            "For which parsing needs to be done \n"
                            "Example : Z:\Information Retrival\Assignments\Info\Final Project\CACM Corpus \n")
    dest_path_cleaned_corpus = raw_input("Please enter the full path where you would want to store the cleaned corpus,\n"
                          "Example : Z:\Information Retrival\Assignments\Info\Final Project\Cleaned CACM Corpus \n")


    #Obtain and Process Queries
    source_path_query = raw_input("Please enter the full path where the query terms are present,\n"
                            "Z:\Information Retrival\Assignments\Info\Final Project\Query_File\Cacm.Query.txt\n")
    dest_path_query = raw_input("Please enter the full path where the processed query terms to be stored,\n"
                            "Z:\Information Retrival\Assignments\Info\Final Project\Query_File\Cacm.Query.txt\n")
    extract_Query(source_path_query,dest_path_query)


    folder = os.listdir(source_path_raw_copus)

    #Loop for all the Files in the folder
    for file in folder:
        generate_clean_corpus(source_path_raw_copus + '\\' + file, file, dest_path_cleaned_corpus)
    print("The Cleaned Corpus is present in location \n"
          + dest_path_cleaned_corpus)

main()