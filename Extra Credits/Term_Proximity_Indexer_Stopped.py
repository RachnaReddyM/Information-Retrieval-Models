import os
import operator

index_unigram = {}  # Inverted Index for Unigrams
uni_tokens={} # Unigrams- no. of tokens in each document

# fetch corups from the below path
docs_source_path = "D:\IR\p\corpus"

# fetch the stopwords from the below path
stopwordsPath = "D:\IR\p\common_words.txt"

# filenamelist contains the list filenames of files in the corpus
filenamelist = os.listdir(docs_source_path)

# method to read stopwords from file and store in stopwords list
def get_stopwords():
  f = open(stopwordsPath, 'r+')
  content = f.read()
  global stopwords
  stopwords = content.split("\n")

# to generate an inverted index
def create_inverted_index():
    for filename in filenamelist:
        content = []
        name_of_file = filename.split('.txt')
        docID = name_of_file[0]

        #print docID

        f = open(docs_source_path + '\\' + filename, 'r+')
        raw_data = f.read()
        content = raw_data.split()

        ## Unigram-Inverted-Index generation

        unigram_token = []
        i = 0
        posdict={} # dictionary to hold the positions of each term in a particular document

        for c in content:
          if c not in stopwords:
            i=i+1
            if posdict.has_key(c):
              posdict[c].append(i)
            else:
              posdict[c]=[]
              posdict[c].append(i)
        
        for c in content:

          # if the fetched token is not in the stopwords, then only store in the inverted index
          if c not in stopwords:
            # to generate the number of tokens in each document
            unigram_token.append(c)

            if index_unigram.has_key(c):
        # when this term occurs for the first time in a particular document

              index_unigram[c].update({docID: posdict[c]})

        # if term does not exist in the dictionary yet
            else:
              index_unigram[c] = {docID: posdict[c]}
        uni_tokens[docID]=len(unigram_token)


# to write the inverted index to a file
def write_index_to_file(dict_gram, nof):
	final_term=""
	f = open(nof, "w+")
	for k, v in dict_gram:
		value_term = ""
		i = 0
		for key, val in v.iteritems():
			i += 1
			value_term += "(" + str(key) + "," +str(len(val))+","+ str(val) + ")"
			if (i < len(v)):
				value_term += ";"
		final_term+= str(k) + "-->"+value_term + "\n"
	f.write(final_term.strip())
	f.close()

# to write the no. of tokens dictionary to file
def write_tokens_to_file(grams_tokens,nof):
  token_string=""
  f=open(nof,"w+")

  for k,v in grams_tokens.iteritems():
    token_string+=str(k)+"-->"+str(v)+"\n"
  f.write(token_string.strip())
  f.close()



def _mainindexer():
    get_stopwords()
    create_inverted_index()
    sorted_index=sorted(index_unigram.items(), key=operator.itemgetter(0))
    write_index_to_file(sorted_index, "TP_Index_Unigram_Stopped.txt")
    write_tokens_to_file(uni_tokens,"TP_Unigram_tokens_Stopped.txt")


_mainindexer()