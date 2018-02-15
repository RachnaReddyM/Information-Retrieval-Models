import math
import operator


queriesdict = {}
inverted_index = {}
doc_length = {}
file_content = []

#Calculate number of doc in corpus and determinf avdl
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

# Reads the query file and create dictionary
def get_queries(filename):
    f = open(filename, 'r+')
    content = f.read()
    qcontent = content.split("\n")
    # print qcontent
    for q in qcontent:
        qstring = q.split(" ")
        query = " ".join(qstring[1:])
        queriesdict[qstring[0]] = query

# Read the inverted index
def get_index(indexPath):
    f = open(indexPath, 'r+')
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

# Since we do not want to include stop words in the query expansion terms
# This method creates a list of stop words whcih we can avoid during expansion
def get_stop_words(common_words_path):
    f = open(common_words_path, 'r+')
    content = f.read()
    global stop_words
    stop_words = content.split("\n")
    print stop_words

# Perform Pseudo Relevance (Consider 5 Query terms) Since it maximises Relevance for 5 query words
# Explanaiton of why 5 terms provided in Report
def do_pseudo_relevance(qid,docs):
    dict_relTerms_feq = {}
    score = 0

    for key_doc,value_doc in docs[:3]:
        for key,value in inverted_index.iteritems():
            if key not in stop_words and (not key.replace('.','',1).isdigit()):
                if key_doc in inverted_index[key]:
                    score = inverted_index[key][key_doc]
                    if key in dict_relTerms_feq:
                        dict_relTerms_feq[key] = int(score) + int(dict_relTerms_feq[key])
                    else:
                        dict_relTerms_feq[key] = int(score)
    temp_dict = (sorted (dict_relTerms_feq.iteritems(), key = operator.itemgetter(1), reverse = True))
    print "Pseudo Relevance for " + qid
    for k,v in temp_dict[:5]:
        queriesdict[qid] = queriesdict[qid] + " "+ k

# Keep storing the output of the file in a list,
# Avoiding having to open the file and writing again and again
# Instead store results then finally write the content to the file
def form_the_file(qid,docs):
    i=1
    s=""
    for key,value in docs[:100]:
        s+=qid+" "+"Q0"+" "+str(key)+" "+str(i)+" "+str(value)+" "+"BM25_with_Pseudo_Relevance_Feedback"+"\n"
        i=i+1
    file_content.append(s)

# Write output to file
def write_to_file(results):
    f = open(results, "w+")
    rstring = "".join(file_content)
    f.write(rstring.strip())
    f.close()

# Constructs a dictionary of queryId : Query
def populate_query_qfi(k):
    query_temp = {}
    query_terms = k.split()

    for terms in query_terms:
        if not query_temp.has_key(terms):
            query_temp[terms] = query_terms.count(terms)
    return query_temp

# Runs BM25 model on each query, IF pseudo relevance is not done then sends the top ranked documents to
# expand query terms. If pseudo Relevance Feedback is already done then, it writes the run (with expanded query terms
# in the output file
def searching(pseudo_Relevance_Done,results):
    for k, v in queriesdict.iteritems():
        scoredict = {}
        # Generate Dictionay of queryid : Query
        qtermdict = populate_query_qfi(v)
        # For each query term calc Bm25 score
        for q, qfi in qtermdict.iteritems():

            if q in inverted_index:
                doc = []
                for docID in inverted_index[q]:
                    fi = inverted_index[q][docID]
                    score=0.0
                    score=BM25(docID, len(inverted_index[q]), fi, qfi)
                    try:
                        scoredict[docID] = scoredict[docID] + score
                    except KeyError:
                        scoredict[docID] = score
        sort_dict = sorted(scoredict.iteritems(), key=operator.itemgetter(1),reverse=True)
        # Check for pseudo relevance, If done form to file
        if pseudo_Relevance_Done:
            print "Final Run on Query Id "+k
            form_the_file(k, sort_dict)
        # Check for pseudo relevance, if not done call do_pseudo_relevance which
        # expands query terms
        else:
            print "Before Pseudo Rel " + k
            do_pseudo_relevance(k,sort_dict)
    # Write output to file
    write_to_file(results)

#Calculates the value of K which needs to be plugged in BM25 Model
def get_kval(dID, k1, b):
    dl = doc_length[dID]
    k = k1 * ((1 - b) + (b * (float(dl) / avdl)))
    return k


#Calculates Bm25 score for each document Given Doc name, ni,fi and qfi
#Returns BM25 Score
def BM25(dID, ni, fi, qfi):
    ri = 0
    R = 0
    k1 = 1.2
    k2 = 300
    b = 0.75

    kval = get_kval(dID, k1, b)

    p1 = (((float(ri) + 0.5) / (float(R) - float(ri) + 0.5)) / ((float(ni) - float(ri) + 0.5) / (float(N) - float(ni)
          - float(R) + float(ri) + 0.5)))
    p2 = (((float(k1) + 1) * float(fi)) / (float(kval) + float(fi)))
    p3 = (((float(k2) + 1) * float(qfi)) / (float(k2) + float(qfi)))
    p4 = math.log(p1, 2)
    score = p4 * p2 * p3

    return score


#Main function that calls other functions
def _main():
    # Path to query file
    queryPath = raw_input("Please enter the full path where the processed queries are present,\n"
                            "Example : Z:\Information Retrival\Assignments\Info\Final Project\processed.query.txt \n")
    # Path where the index is present
    indexPath = raw_input("Please enter the full path where the inverted index is present,\n"
                          "Example : Z:\Information Retrival\Assignments\Info\Final Project\index_unigrams.txt \n")

    # Path where the unigram tokens are present
    docPath = raw_input("Please enter the full path where the unigram tokens are present,\n"
                            "Z:\Information Retrival\Assignments\Info\Final Project\unigram_tokens.txt\n")
    #Path where the stop words are present
    common_words_path=raw_input("Please enter the full path where the common words/stopwords are present,\n"
        "Z:\Information Retrival\Assignments\Info\Final Project\common_words.txt\n")
    #Path where you want the results to be stored
    results= raw_input("Please enter the full path, along with text file name, where the BM25 results need to be stored,\n"
                            "Z:\Information Retrival\Assignments\Info\Final Project\BM25.txt\n")
    #First Run where Pseudo Relevance needs to be run on first run of BM25 for all queries
    Pseudo_Relevance_Done = False
    #Get avg document length and total number of documents in the Corpus
    get_avdl_doclen(docPath)
    #Get all the queries from the query file
    get_queries(queryPath)
    # Read the index from the file into the dictionary
    get_index(indexPath)
    # During Pseudo Relevance we do not want to add stop words to query terms since they do not contribut much since they
    # are already present in most of the doumcnets in corpus
    get_stop_words(common_words_path)
    # Perfrom BM25 Run and Pseudo Relelvance to add query terms to the initial query
    searching(Pseudo_Relevance_Done,results)
    # Query terms are added after pseudo relevance
    Pseudo_Relevance_Done = True
    # After Query Expansion run finally run BM25 with expanded  query terms
    searching(Pseudo_Relevance_Done,results)
_main()