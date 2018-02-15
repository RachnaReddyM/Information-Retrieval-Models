from collections import defaultdict
import re

# Path where the BM25 Top ranked results are present
BM25_Result_Path = "D:\IR\p\BM25_Ranking.txt"
# Path to the Cleaned Corpus
corpus_path = "D:\IR\p\corpus"
# Path to the processed query file
query_path = "D:\IR\p\processed.queries.txt"
# List of stop words, During highlighting unigrams, Ideally there are more useful words than the list of words
# provided below, highlighting these terms might not be really useful as snippets
# Ex. the ... ... Computer, useful snippet would highlight term computer if it is the 'the' and 'Computer' are only
# query terms present in the file
stop_list = ["the","of","to","and","i","in","for"]
queriesdict ={}
query_doc_dict = defaultdict(list)

#Read Query from the query file (processed query)
def get_queries(filename):
    f = open(filename, 'r+')
    content = f.read()
    qcontent = content.split("\n")
    for q in qcontent:
        qstring = q.split(" ")
        query = " ".join(qstring[1:])
        queriesdict[qstring[0]] = query

# Get top ranked Results for each query 64 * 100 files
def get_toprank_doc(filename):
    f = open(filename, 'r+')
    lines = f.readlines()
    lines = [line.strip() for line in lines]
    for each_doc in lines:
        str = each_doc.split(" ")
        query_doc_dict[str[0]].append(str[2])

# Check if three query words appear together in the document (Sliding the window of 3 query words together)
def three_word_snippet(query_terms,file_name):
    f = open(corpus_path + "\\" + file_name +".txt",'r+')
    content = f.read()
    # Get 3 words from query (window sliding with 3 query words)
    for word in range(len(query_terms) - 2):
        split_trigram = query_terms[word:word+3]
        trigram = " ".join(split_trigram)
        # Check if the word appers in the document
        if content.find(trigram) != -1 and bool(re.findall('\\b'+trigram + '\\b', content)):
            index = content.index(trigram)
            # Set True if Found
            trigram_found = True
            # Get words before query terms
            starting_index = max(content.index(trigram)- 50, 0)
            # IF char at starting index is a word you have to go back till you find a space so whole word is presnt
            if starting_index != 0:
                while starting_index > 0:
                    if content[(starting_index - 1):starting_index] not in [" ", "\n"]:
                        starting_index -= 1
                    else:
                        break
            # Get ending index (words after query terms)
            ending_index = min(content.index(trigram) +  len(trigram) + 50, len(content))
            if ending_index != len(content):
                while ending_index < len(content):
                    if content[ending_index:(ending_index + 1)] not in [" ", "\n"]:
                        ending_index += 1
                    else:
                        break
            # Get words before highlighted term
            before_keyword = content[starting_index:content.index(trigram)]
            # Get highlighted term
            keyword = content[content.index(trigram):(content.index(trigram) + len(trigram))]
            # Highlight the query term
            keyword = '<mark>{}</mark>'.format(keyword)
            # Get words after query termss
            after_keyword = content[(content.index(trigram)+len(trigram)):ending_index]
            # Join all to get snippet
            snippet = before_keyword + keyword + after_keyword
            return trigram_found,snippet
    return False,0

# Check if two query words appear together in the document (Sliding the window of 2 query words together)
def two_word_snippet(query_terms,file_name):
    f = open(corpus_path + "\\" + file_name+".txt",'r+')
    content = f.read()
    # Get 3 words from query (window sliding with 3 query words)
    for word in range(len(query_terms) - 1):
        split_bigram = query_terms[word:word+2]
        bigram = " ".join(split_bigram)
        # Check if the word appers in the document
        if content.find(bigram) != -1 and bool(re.findall('\\b'+bigram + '\\b', content)):
            matched_word = re.findall('\\b'+ bigram+ '\\b', content)
            word_start = re.search('\\b'+ bigram+ '\\b', content)
            # GET INDEX OF MATCHED WORD
            index = word_start.start()
            # IF found set found to true
            bigram_found = True
            # Get starting index of the sentance
            starting_index = max(index - 50, 0)
            if starting_index != 0:
            #Traceback untill you get space to get full word
                while starting_index > 0:
                    if content[(starting_index - 1):starting_index] not in [" ", "\n"]:
                        starting_index -= 1
                    else:
                        break
            # Get ending index of the sentence
            ending_index = min(index + len(matched_word[0]) + 50, len(content))
            if ending_index != len(content):
                while ending_index < len(content):
                    if content[(starting_index - 1):starting_index].isalnum():
                        ending_index += 1
                    else:
                        break
            # Words before highlighted query term
            before_keyword = content[starting_index:index]
            # Get highlighed terms
            keyword = content[index:(index + len(matched_word[0]))]
            # Highlightt the query term
            keyword = '<mark>{}</mark>'.format(keyword)
            # Get after the highlighted query term
            after_keyword = content[(index + len(matched_word[0])):ending_index]
            # Join all to form snippet
            snippet = before_keyword + keyword + after_keyword
            return bigram_found, snippet
    return False,0

# Check if query words appear together in the document
def one_word_snippet(query_terms,file_name):
    f = open(corpus_path + "\\" + file_name+".txt",'r+')
    content = f.read()
    # CHECK for each query term
    for unigram in range(len(query_terms)):
        # Ignoring stop words ,
        # List of stop words, During highlighting unigrams, Ideally there are more useful words than the list of words
        # provided below, highlighting these terms might not be really useful as snippets
        # Ex. the ... ... Computer, useful snippet would highlight term computer if it is the 'the' and 'Computer' are only
        # query terms present in the file
        if query_terms[unigram] not in stop_list:
            if content.find(query_terms[unigram]) != -1 and bool(re.findall('\\b'+query_terms[unigram] + '\\b', content)):
                matched_word = re.findall('\\b'+ query_terms[unigram]+ '\\b', content)
                word_start = re.search('\\b'+ query_terms[unigram]+ '\\b', content)
                # Get the starting index
                index = word_start.start()
                # Set found to true
                unigram_found = True
                starting_index = max(index - 50, 0)
                #Trace back till you get complete word
                if starting_index != 0:
                    while starting_index > 0:
                        if content[(starting_index - 1):starting_index].isalnum():
                            starting_index -= 1
                        else:
                            break
                # Get ending index of the word
                ending_index = min(index + len(matched_word[0]) + 50, len(content))
                if ending_index != len(content):
                    while ending_index < len(content):
                        if content[(starting_index - 1):starting_index].isalnum():
                            ending_index += 1
                        else:
                            break
                # Words before the highlighted term
                before_keyword = content[starting_index:index]
                # The query term
                keyword = content[index:(index + len(matched_word[0]))]
                # Highlightng the query term
                keyword = '<mark>{}</mark>'.format(keyword)
                # Words after the highlighted term
                after_keyword = content[(index + len(matched_word[0])):ending_index]
                # Combine all to form snippet
                snippet = before_keyword + keyword + after_keyword
                return unigram_found, snippet
    return False,0

# Generates the snippet , Checks initially if more than 1 query term appears together
# IF yes the snippet is generated if the query terms do not co-appear than generte snippet
# for the query term.
def generate_snippet(query,file_name):
    query_terms = query.split()
    trigram_exist,snippet_sentence = three_word_snippet(query_terms,file_name)
    if trigram_exist:
        return snippet_sentence
    bigram_exist, snippet_sentence = two_word_snippet(query_terms, file_name)
    if bigram_exist:
        return  snippet_sentence
    unigram_exist, snippet_sentence = one_word_snippet(query_terms, file_name)
    if unigram_exist:
        return snippet_sentence
    else:
        return "No Useful Snippet Found"


# CREATE an HTML file named Snippet_Output.html and write individual snippet in it.
def main():
    f = open("Snippet_Output.html", "w+")
    f.write("<!DOCTYPE html>")
    get_queries(query_path)
    get_toprank_doc(BM25_Result_Path)
    for qid, query in queriesdict.iteritems():
        f.write("{Query id = " + qid + " }<br />")
        for file_name in query_doc_dict[qid]:
            f.write("{Doc Name = " + file_name + " }<br />")
            f.write(" {Snippet} <br />")
            sentence = generate_snippet(query,file_name)
            f.write(sentence +"<br />")
            f.write(" {\Snippet} <br />")
            f.write("{\Doc Name = " + file_name + " }<br />")
            f.write("<br \>")
            print sentence
        f.write("{/Query}<br />")
    f.close()


main()