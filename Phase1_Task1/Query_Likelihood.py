import math
import operator

# dictionary to store the queries (key- Query ID and value- query)
queriesdict = {}

# dictionary to store the inverted index 
# (key- tokens and value- dictionary(key- docID and value- term frequency))
inverted_index = {}

# list to hold the ranked documents
results=[]

# dictionary to store the document length (key- docID and value- document's length)
dls={}

# dictionary to store the term frequencies of each token in the entire corpus
dict_unigram_tf = {}

#lambda value used in QueryLikelyhood formula
lam = 0.35

# method to read the term frequencies from the file and 
# store it in dict_unigram_tf dictionary
def create_unigram_tf_dict(termFrequency):
    string_entry=[]
    f = open(termFrequency,'r+')
    lines = f.readlines()
    for line in lines:
        string_entry.append(line.strip())

    for line in string_entry:
        temp = line.split("-->")
        dict_unigram_tf.update({temp[0]:int(temp[1])})



# method to calculate the no. of documents in the corpus and 
# the total no. of tokens in the corpus
def get_avdl_doclen(docPath):
    totalcount = 0
    f = open(docPath,'r+')
    content = f.read()
    contents = content.split("\n")
    global N
    N=len(contents)
    for c in contents:
        d = c.split("-->")
        dls[d[0]]=d[1]
        totalcount += float(d[1])
    global avdl
    avdl=totalcount/N
    return totalcount


# method to read the queries from the text file and 
# store it in a dictionary with Query ID and Query
def get_queries(filename):
    f = open(filename,'r+')
    content = f.read()
    qcontent = content.split("\n")
    # print qcontent
    for q in qcontent:
        qstring = q.split(" ")
        query = " ".join(qstring[1:])
        queriesdict[qstring[0]] = query


# method to read the inverted index from a file and
# store in it a dictionary with token as the key and 
# doc ID and term frequency in another dictionary as value

def get_index(indexPath):
    f = open(indexPath,'r+')
    content = f.read()
    contents = content.split("\n")
    for c in contents:
        index = c.split("-->")
        docs = index[1].split(",")

        inlist = {}

        i = 0

        while i <= len(docs) - 1:
            inlist[docs[i][1:]] = docs[i + 1][:-1]
            i = i + 2

        inverted_index[index[0]] = inlist


# method to write the ranked results to a file
def write_to_file(QLresults):
    f = open(QLresults, "w+")
    rstring="".join(results)
    f.write(rstring.strip())
    f.close()

# method to generate the results string with query ID, doc ID, ranking etc.
def form_the_file(qid,docs):
    i=1
    s=""
    for k,v in docs[:100]:
        s+=qid+" "+"Q0"+" "+str(k)+" "+str(i)+" "+str(v)+" "+"QueryLikeliHood_Unigram_Casefolding"+"\n"
        i+=1
    results.append(s)


# method to get relenvant documents for each query by 
# calculating the QueryLikelihood score of each document
def searching(QLresults):

    # for every query
    for k, v in queriesdict.iteritems():
        scoredict = {}
        qtermdict = {}
        qterms = v.split()

        # for each query term
        for q in qterms:
            #if qtermdict.has_key(q):
            try:
                qtermdict[q] = qtermdict[q] + 1
            except KeyError:
                qtermdict[q] = 1

        for q,qfi in qtermdict.iteritems():

            if q in inverted_index:
                cqi = int(dict_unigram_tf[q])
                doc = []
                for docID in dls:
                    if docID in inverted_index[q]:
                        fi = inverted_index[q][docID]
                    else:
                        fi = 0

                    # method call to the tfidf scoring fucntion
                    score=QL(docID,fi,cqi)
                    score=score*qfi
                    #if scoredict.has_key(docID):
                    try:
                        scoredict[docID] = scoredict[docID] + score
                    except KeyError:
                        scoredict[docID] = score
        # sorted list of tuples based on the ranking of each document for each query
        sort_dict = sorted(scoredict.iteritems(), key=operator.itemgetter(1),reverse=True)
        form_the_file(k,sort_dict)
    write_to_file(QLresults)


# method to calculate the document score using the QueryLikelihood formula

def QL(dID,fi,cqi):

    dl = dls[dID]

    exp1 = ((1 - lam) * (float(fi) / float(dl)))
    exp2 = lam * (float(cqi) / float(C))
    exp3 = exp1 + exp2
    if exp3 != 0:
        score = math.log(exp3)
    else:
        score = 0

    return score
       


def _main():

    # path to the processed queries(parsed queries)
    queryPath = raw_input("Please enter the full path where the processed queries are present,\n"
                           "Example : Z:\Information Retrival\Assignments\Info\Final Project\processed.query.txt \n")
    
    # path to the inverted index
    indexPath = raw_input("Please enter the full path where the inverted index is present,\n"
                         "Example : Z:\Information Retrival\Assignments\Info\Final Project\index_unigrams.txt \n")



    # path to the unigram tokens(document ID and the no. of unigrams it contains) file
    docPath = raw_input("Please enter the full path where the unigram tokens are present,\n"
                           "Z:\Information Retrival\Assignments\Info\Final Project\unigram_tokens.txt\n")

    # path to the unigrams term frequencies(unigram token and the term frequency of it in the corpus)
    termFrequency= raw_input("Please enter the full path, along with text file name, where the unigram term frequencies are stored for each term in corpus ,\n"
                           "Z:\Information Retrival\Assignments\Info\Final Project\unigram_TF.txt\n")

    # path where the results are to be written to
    QLresults= raw_input("Please enter the full path, along with text file name, where the results need to be stored,\n"
                           "Z:\Information Retrival\Assignments\Info\Final Project\Query_Likelihood.txt\n")




    global C 
    C = get_avdl_doclen(docPath)
    create_unigram_tf_dict(termFrequency)
    get_queries(queryPath)
    get_index(indexPath)
    searching(QLresults)


_main()