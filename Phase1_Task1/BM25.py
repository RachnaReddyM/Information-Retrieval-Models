import math
import operator

# dictionary to store the queries (key- Query ID and value- query)
queriesdict = {}

# dictionary to store the inverted index 
# (key- tokens and value- dictionary(key- docID and value- term frequency))
inverted_index = {}

# list to hold the ranked documents
results=[]

#dictionary to store the document length (key- docID and value- document's length)
dls={}


# method to get the no. of documents in the corpus and 
# the average document length of the corpus
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
def write_to_file(BM25results):
    f = open(BM25results, "w+")
    rstring="".join(results)
    f.write(rstring.strip())
    f.close()

# method to generate the results string with query ID, doc ID, ranking etc.
def form_the_file(qid,docs):
    i=1
    s=""
    for k,v in docs[:100]:
        s+=qid+" "+"Q0"+" "+str(k)+" "+str(i)+" "+str(v)+" "+"BM25_Unigram_Casefolding"+"\n"
        i+=1
    results.append(s)


# method to get relenvant documents for each query by 
# calculating the tfidf score of each document
def searching(BM25results):

    # for every query
    for k, v in queriesdict.iteritems():
        scoredict = {}
        qtermdict = {}
        qterms = v.split()

        # for each query term
        for q in qterms:

            try:
                qtermdict[q] = qtermdict[q] + 1
            except KeyError:
                qtermdict[q] = 1

        for q,qfi in qtermdict.iteritems():
            if q in inverted_index:
                doc = []
                for docID in inverted_index[q]:
                    fi = inverted_index[q][docID]
                    score=0.0
                    score=BM25(docID, len(inverted_index[q]), fi,qfi)
                    #if scoredict.has_key(docID):
                    try:
                        scoredict[docID] = scoredict[docID] + score
                    except KeyError:
                        scoredict[docID] = score

        # sorted list of tuples based on the ranking of each document for each query                
        sort_dict = sorted(scoredict.iteritems(), key=operator.itemgetter(1),reverse=True)
        form_the_file(k,sort_dict)
    write_to_file(BM25results)


# method to calculate the value of K
def get_kval(dID, k1, b,avdl):
    dl = dls[dID]
    k = k1 * ((1 - b) + (b * (float(dl) / avdl)))
    return k


# method to calculate the document score using the BM25 formula
def BM25(dID, ni, fi, qfi):
    ri = 0
    R = 0
    k1 = 1.2
    k2 = 100
    b = 0.75


    kval = get_kval(dID, k1, b,avdl)

    p1 = (((float(ri) + 0.5) / (float(R) - float(ri) + 0.5)) / ((float(ni) - float(ri) + 0.5) / (float(N) - float(ni)
          - float(R) + float(ri) + 0.5)))
    p2 = (((float(k1) + 1) * float(fi)) / (float(kval) + float(fi)))
    p3 = (((float(k2) + 1) * float(qfi)) / (float(k2) + float(qfi)))
    p4 = math.log(p1, 2)
    score = p4 * p2 * p3

    return score
       


def _main():

    # path to the processed queries(parsed queries)
    queryPath = raw_input("Please enter the full path where the processed queries are present,\n"
                            "Example : Z:\Information Retrival\Assignments\Info\Final Project\processed.query.txt \n")
    
    # path to the inverted index
    indexPath = raw_input("Please enter the full path where the inverted index is present,\n"
                          "Example : Z:\Information Retrival\Assignments\Info\Final Project\index_unigrams.txt \n")
    # path to the unigram tokens(docuemnt and the no. of unigrams it contains) file

    docPath = raw_input("Please enter the full path where the unigram tokens are present,\n"
                            "Z:\Information Retrival\Assignments\Info\Final Project\unigram_tokens.txt\n")
    
    # path where the results are to be written to
    BM25results= raw_input("Please enter the full path, along with text file name, where the BM25 results need to be stored,\n"
                            "Z:\Information Retrival\Assignments\Info\Final Project\BM25.txt\n")
    get_avdl_doclen(docPath)
    get_queries(queryPath)
    get_index(indexPath)
    searching(BM25results)


_main()