import os
import operator


#indexer.py creates an inverted index considering the parsed corpus

index_unigram= {} # Inverted Index for Unigrams
unigram_tf={}  # Unigrams term frequencies
unigram_df={} # Unigrams Document frequencies
uni_tokens={} # Unigrams- no. of tokens in each document

# fetch corups from the below path
docs_source_path = "D:\IR\project\corpus"

# filenamelist contains the list of filenames of the files in the corpus folder
filenamelist = os.listdir(docs_source_path)

# to generate an inverted index
def create_inverted_index():

  for filename in filenamelist:
    content=[]
    name_of_file=filename.split('.txt')
    docID=name_of_file[0]
 

    f = open(docs_source_path + '\\' + filename, 'r+')
    raw_data=f.read()
    content=raw_data.split()
    
     # Unigram-Inverted-Index generation

    unigram_token=[]


    for c in content:


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
  create_inverted_index()
  #sorted inverted index
  sorted_index=sorted(index_unigram.items(), key=operator.itemgetter(0))
  write_index_to_file(sorted_index,"Index_Unigram.txt")
  write_tokens_to_file(uni_tokens,"Unigram_tokens.txt")
  generate_tf_df(index_unigram,unigram_tf,unigram_df)
  generate_tf_table(unigram_tf,"Unigram_TF.txt")
  generate_df_table(unigram_df,"Unigram_DF.txt")

_mainindexer()