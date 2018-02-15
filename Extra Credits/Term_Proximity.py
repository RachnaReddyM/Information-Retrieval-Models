import math
import operator

# dictionary to store the queries (key- Query ID and value- query)
queriesdict = {}

# dictionary to store the inverted index 
# (key- tokens and value- dictionary(key- docID and value- term frequency))
inverted_index = {}

#dictionary to store the document length (key- docID and value- document's length)
doc_length = {}

# list to hold the ranked documents
TP_results=[]

# lambda value used for smoothing the proximity score
lam=0.192


# method to get the no. of documents in the corpus and 
# the average document length of the corpus
def get_avdl_doclen(docPath):
    totalcount = 0
    f = open(docPath, 'r+')
    content = f.read()
    contents = content.split("\n")
    global N
    N=len(contents)
    for c in contents:
        d = c.split("-->")
        doc_length[d[0]] = int(d[1])
        totalcount += float(d[1])
    global avdl
    avdl=totalcount/N

# method to read the queries from the text file and 
# store it in a dictionary with Query ID and Query
def get_queries(filename):
    f = open(filename, 'r+')
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
    f = open(indexPath, 'r+')
    content = f.read()
    contents = content.split("\n")
    for c in contents:
        index = c.split("-->")
        list_of_docs = index[1].split(";")
        inlist = {}
        for entry in list_of_docs:
            docs = []
            docs = entry.split(",",2)
            docname = docs[0].strip()
            positoin = docs[2].partition('[')[-1].rpartition(']')[0]
            position_list = positoin.split(',')
            position_list = map(int, position_list)
            inlist[docname[1:]] = position_list
        inverted_index[index[0]] = inlist

# method to generate the results string with query ID, doc ID, ranking etc.
def form_the_file(qid,docs):
    i=1
    s=""
    for key,value in docs[:100]:
        s+=qid+" "+"Q0"+" "+str(key)+" "+str(i)+" "+str(value)+" "+"BM25+TermProximity_Unigram_Casefolding"+"\n"
        i=i+1
    TP_results.append(s)

# method to write the ranked results to a file
def write_to_file(fname):
    f = open(fname, "w+")
    rstring = "".join(TP_results)
    f.write(rstring.strip())
    f.close()

# method to store the query terms and the frequency of each query term in a dictionary
def populate_query_qfi(k):
    query_temp = {}
    query_terms = k.split()

    for terms in query_terms:
        if not query_temp.has_key(terms):
            query_temp[terms] = query_terms.count(terms)
    return query_temp

# method to check the term proximity score for the co-occurrence of every 2 terms in the query
def check_proximity(term1,term2,DocID):
    pos_list1=[]
    pos_list2=[]
    total_score=0.0
    pos_list1=inverted_index[term1][DocID]
    pos_list2=inverted_index[term2][DocID]
    for pos in pos_list1:
        termscore=0.0
        if pos+1 in pos_list2:
            termscore= 1.0
        elif pos+2 in pos_list2:
            termscore= 0.95
        elif pos+3 in pos_list2:
            termscore= 0.9
        elif pos+4 in pos_list2:
            termscore= 0.60
        total_score+=termscore
    return total_score # the score of the 2 terms co-occuring

# method to generate the proximity score for every 2 terms in the query    
def consider_proximity(scoredict,query,qid):
        proximity_score_dict={} # dictionary that contains the document ID and its proximity score
        tp_score={}
        tp_score=scoredict
        query_terms = query.split()
        for q_term in range(len(query_terms) -1):
            q1 = query_terms[q_term]
            q2 = query_terms[q_term+1]
            proximity_terms = query_terms[q_term:q_term+2]
            if (proximity_terms[0] in inverted_index) & (proximity_terms[1] in inverted_index):
                doc = []
                for docID in inverted_index[proximity_terms[0]]:
                    numerator_score = 0
                    if docID in inverted_index[proximity_terms[1]]:
                        numerator_score = check_proximity(proximity_terms[0],proximity_terms[1],
                                                           docID)
                    try:
                        proximity_score_dict[docID]+=numerator_score
                    except KeyError:
                        proximity_score_dict[docID]=numerator_score
        for k,v in proximity_score_dict.iteritems():
            doclen=doc_length[k]
            proximity_smoothing=lam*v
            BM25_smoothing=(1-lam)*scoredict[k]
            tp_score[k]=BM25_smoothing+proximity_smoothing
        tp_sort_dict = sorted(tp_score.iteritems(), key=operator.itemgetter(1),reverse=True)
        form_the_file(qid, tp_sort_dict)

# method to get relenvant documents for each query by 
# calculating the BM25 score of each document and then considering the term proximity scores
def searching(results):
    for k, v in queriesdict.iteritems():
        scoredict = {}
        qtermdict = populate_query_qfi(v)

        for q, qfi in qtermdict.iteritems():
        #for q in queriesdict.keys():
            if q in inverted_index:
                doc = []
                for docID in inverted_index[q]:
                    fi = len (inverted_index[q][docID])
                    score=0.0
                    score=BM25(docID, len(inverted_index[q]), fi, qfi)
                    try:
                        scoredict[docID] = scoredict[docID] + score
                    except KeyError:
                        scoredict[docID] = score
        consider_proximity(scoredict,v,k)

    write_to_file(results)

# method to calculate the value of K
def get_kval(dID, k1, b):
    dl = doc_length[dID]
    k = k1 * ((1 - b) + (b * (float(dl) / avdl)))
    return k

# method to calculate the document score using the BM25 formula
def BM25(dID, ni, fi, qfi):
    ri = 0
    R = 0
    k1 = 1.2
    k2 = 100
    b = 0.75

    kval = get_kval(dID, k1, b)

    p1 = (((float(ri) + 0.5) / (float(R) - float(ri) + 0.5)) / ((float(ni) - float(ri) + 0.5) / (float(N) - float(ni)
          - float(R) + float(ri) + 0.5)))
    p2 = (((float(k1) + 1) * float(fi)) / (float(kval) + float(fi)))
    p3 = (((float(k2) + 1) * float(qfi)) / (float(k2) + float(qfi)))
    p4 = math.log(p1, 2)
    score = p4 * p2 * p3

    return score



def _main():
    queryPath = raw_input("Please enter the full path where the processed queries are present,\n"
                          "Example : Z:\Information Retrival\Assignments\Info\Final Project\processed.query.txt \n")
    indexPath = raw_input("Please enter the full path where the inverted index is present,\n"
                          "Example : Z:\Information Retrival\Assignments\Info\Final Project\index_unigrams.txt \n")

    docPath = raw_input("Please enter the full path where the unigram tokens are present,\n"
                        "Z:\Information Retrival\Assignments\Info\Final Project\unigram_tokens.txt\n")

    results = raw_input(
        "Please enter the full path, along with text file name, where the results need to be stored,\n"
        "Z:\Information Retrival\Assignments\Info\Final Project\TP_results.txt\n")

    get_avdl_doclen(docPath)
    get_queries(queryPath)
    get_index(indexPath)
    searching(results)
_main()