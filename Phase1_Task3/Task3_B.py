import math
import operator
import os
import re


# fetch the stemmed corpus from the below file
stemmed_docs = "D:\IR\project\cacm_stem.txt"

# fetch the stemmed queries from the below file
stemmed_queries="D:\IR\project\cacm_stem.query.txt"

# write the processed queries into the below file
output_queries="D:\IR\project\cacm_stem.processed.query.txt"

# dictionary to hold the stemmed corpus and the document ID(key- document ID, value= stemmed document)
corpus={}
index_unigram={} # Inverted Index for Unigrams
uni_tokens={} # Unigrams- no. of tokens in each document
unigram_tf={} # Unigrams term frequencies
unigram_df={} # Unigrams Document frequencies
queries={} # dictionary to hold the Queries along with Query ID(key- Query ID, Values- Query)

# method to read the stemmed queries from the file and write 
# the same queries along with their query IDs, separated by a space
def generate_queries():
  f=open(stemmed_queries,"r+")
  raw_queries=f.read()
  queries_list=raw_queries.split("\n")
  i=0
  for q in queries_list:
    i+=1
    queries[i]=q.rstrip()
  qstring=""  
  f = open(output_queries, "w+")
  for k,v in queries.iteritems():
    qstring+=str(k)+" "+str(v)+"\n"

  f.write(qstring.strip())
  f.close()



# method to generate the inverted index using the corpus dictionary
def generate_index():
  for k,v in corpus.iteritems():

    content=v.split()
    unigram_token=[]

    for c in content:
      unigram_token.append(c)
      if index_unigram.has_key(c):
        if k not in index_unigram[c]:
          index_unigram[c].update({k:1})
        else:
          index_unigram[c][k]+=1
      else:
        index_unigram[c]={k:1}
    uni_tokens[k]=len(unigram_token)

# to generate the term frequency and document frequency table
def generate_tf(index_gram,gram_tf,gram_df):

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
  tfstring=""
  f=open(nof,"w+")
  for k,v in sort_dict:
    tfstring+=str(k)+"-->"+str(v)+"\n"
  f.write(tfstring.strip())
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

# to write ti no. of tokens dictionary to file
def write_tokens_to_file(grams_tokens,nof):
  token_string=""
  f=open(nof,"w+")

  for k,v in grams_tokens.iteritems():
    token_string+=str(k)+"-->"+str(v)+"\n"
  #print token_string.strip()
  f.write(token_string.strip())
  f.close()


def _main():
  f=open(stemmed_docs,'r+')
  content=f.read()
  docs=content.split("#")

# to generate the corpus dictionary to store the document ID and stemmed document
  for d in docs[1:]:
    first_d=d.strip()
    #print first_d
    id_content=first_d.split("\n",1)
    cid="CACM-"+str(id_content[0]).zfill(4)
    textall=id_content[1].splitlines()
    result=""
    for t in textall:
      result+=t+" "
    content_with_single_space = re.sub("\s\s+", " ", result)
    content= content_with_single_space.rstrip('1234567890 ')
    corpus[cid]=content

  generate_index()
  sorted_index=sorted(index_unigram.items(), key=operator.itemgetter(0))
  write_index_to_file(sorted_index,"Index_Unigram_Stemmed.txt")
  write_tokens_to_file(uni_tokens,"Unigram_tokens_Stemmed.txt")
  generate_tf(index_unigram,unigram_tf,unigram_df)
  generate_tf_table(unigram_tf,"Unigram_TF_Stemmed.txt")
  generate_df_table(unigram_df,"Unigram_DF_Stemmed.txt")
  generate_queries()





_main()
