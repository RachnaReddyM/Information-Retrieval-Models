import math
import operator
import os

# fetch corups from the below path
docs_source_path = "D:\IR\project\corpus"

# path and file to fetch the stopwords
stopwordsPath = "D:\IR\project\common_words.txt"

# path and file to fetch parsed queries from to perform stopping
queriesPath="D:\IR\project\processed.query.txt"

# path and file to write the stopped queries
output_queries = "D:\IR\project\stopped.queries.txt"

index_unigram= {} # Inverted Index for Unigrams
unigram_tf={} # Unigrams term frequencies
unigram_df={} # Unigrams Document frequencies
uni_tokens={} # Unigrams- no. of tokens in each document

filenamelist = os.listdir(docs_source_path)
queriesdict={} # dictionary to hold the Queries along with Query ID(key- Query ID, Values- Query)

# method to read stopwords from file and store in stopwords list
def get_stopwords():
    f = open(stopwordsPath, 'r+')
    content = f.read()
    global stopwords 
    stopwords = content.split("\n")





# to generate an inverted index
def create_inverted_index():

  for filename in filenamelist:
    content=[]
    name_of_file=filename.split('.txt')
    docID=name_of_file[0]
 
    #print docID

    f = open(docs_source_path + '\\' + filename, 'r+')
    raw_data=f.read()
    content=raw_data.split()
    
    ## Unigram-Inverted-Index generation

    unigram_token=[]


    for c in content:
    # if the fetched token is not in the stopwords, then only store in the inverted index
        if c not in stopwords:
            # to generate the number of tokens in each document       
            unigram_token.append(c)

            if index_unigram.has_key(c):
        # when this term occurs for the first time in a particular document
                if docID not in index_unigram[c]:
                    index_unigram[c].update({docID:1})
        
                else:
                    index_unigram[c][docID]+=1

      # if term does not exist in the dictionary yet
            else:
                index_unigram[c]={docID:1}


    uni_tokens[docID]=len(unigram_token)


# to generate the term frequency and document frequency table
def generate_tf_df(index_gram,gram_tf,gram_df):

  for key,value in index_gram.iteritems():
    term_frequency=0
    docString=""
    i=0
    for k,v in value.iteritems():
      i+=1
      term_frequency+=v
      docString+=k

      if(i<len(value)):
        docString+=" "

    no_of_docs=len(value)
    
    # dictionary to hold the term frequencies
    gram_tf[key]=term_frequency

    # dictionary to hold the document frequencies
    gram_df[key]={docString:no_of_docs}

# to sort and write the term frequency table to a file
def generate_tf_table(gram_tf,nof):
  sort_dict=sorted(sorted(gram_tf.iteritems()), key=operator.itemgetter(1), reverse=True)
  
  f=open(nof,"w+")
  for k,v in sort_dict:
    f.write(str(k)+"-->"+str(v)+"\n")
  f.close()

# to sort and write document frequency table to file
def generate_df_table(gram_df,nof):
  sort_dict=sorted(gram_df.iteritems(), key=operator.itemgetter(0))
  
  f=open(nof,"w+")
  write_string=""
  for k,v in sort_dict:
    df_value=""
    for key,value in v.iteritems():
      df_value=str(key)+" -> "+str(value)

    final_string=str(k)+"-->"+df_value+"\n"
    write_string+=final_string
  f.write(write_string.strip())
  f.close()

# method to read the parsed queries from a file. performing stopping and then write it to a file
def generate_queries():
  f=open(queriesPath,"r+")
  queries=f.read()
  qcontent=queries.split("\n")
  for q in qcontent:
      qstring = q.split(" ")
      query_string = " ".join(qstring[1:])
      rquery=query_string.split()
      word_consider=[w for w in rquery if w  not in stopwords]
      query = ' '.join(word_consider)
      queriesdict[int(qstring[0])]=query
  sortedqueriesdict= sorted(queriesdict.iteritems(),key=operator.itemgetter(0))
  rstring=""  
  f = open(output_queries, "w+")
  for k,v in sortedqueriesdict:
    rstring+=str(k)+" "+str(v)+"\n"

  f.write(rstring.strip())
  f.close()

# to write the inverted index to a file
def write_index_to_file(dict_gram,nof):
  final_term=""
  f=open(nof,"w+")
  for k,v in dict_gram:
    value_term=""
    i=0
    for key,val in v.iteritems():
      i+=1
      value_term+="("+str(key)+","+str(val)+")"
      if(i<len(v)):
        value_term+=","

      
    final_term+=str(k)+"-->"+value_term+"\n"
  f.write(final_term.strip())
  
  f.close()

# to write the no. of tokens dictionary to file
def write_tokens_to_file(grams_tokens,nof):
  token_string=""
  f=open(nof,"w+")

  for k,v in grams_tokens.iteritems():
    token_string+=str(k)+"-->"+str(v)+"\n"
  #print token_string.strip()
  f.write(token_string.strip())
  f.close()


def _mainindexer():
    get_stopwords()
    create_inverted_index()
    sorted_index=sorted(index_unigram.items(), key=operator.itemgetter(0))
    write_index_to_file(sorted_index,"Index_Unigram_Stopping.txt")
    write_tokens_to_file(uni_tokens,"Unigram_tokens_Stopping.txt")
    generate_tf_df(index_unigram,unigram_tf,unigram_df)
    generate_tf_table(unigram_tf,"Unigram_TF_Stopping.txt")
    generate_df_table(unigram_df,"Unigram_DF_Stopping.txt")
    generate_queries()

_mainindexer()
