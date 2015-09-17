import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from nltk.corpus import verbnet
import re
import sys
from nltk.corpus import treebank
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
import misc

def get_verbs(verb): 
 all_set_verbs = set() 
 all_verbs =  verbnet.classids(lemma=verb)
 for v in all_verbs:
   splitted = v.split("-")
   all_set_verbs.add(splitted[0])
 return all_set_verbs

f = open("test_with_entities_12000.tsv","r")
stop = stopwords.words('english')
wordnet_lemmatizer = WordNetLemmatizer()

final_unigram_list = list()
final_unigram_set = set()

i = 0
verbs_list =['VB','VBD','VBG','VBN','VBP','VBZ']

existing = open('final_unigram_tokens.txt','r')
existing_list = existing.readline().split('\t')
final_unigram_set |= set(existing_list)

with open("test_unigram_tokens_12000.txt", "a") as train_file:
  for line in f:
        i = i + 1
        print i

        tab_seperated = re.split("\t",line)
        sentence  = unicode(tab_seperated[3], errors='ignore')

        set_words =  set()
        wordList  = pos_tag(word_tokenize(sentence))

        for word in wordList:
            try:
              if word[0].lower().strip() not in stop:     
                set_words.add(wordnet_lemmatizer.lemmatize(word[0].lower().strip(),misc.getCoarseTag(word[1])))
            except:
                e = sys.exc_info()[0]
                print "Description " + str(e) + " For word " + str(word)


        temp_words = set()
        for word in set_words:
            synonyms =  wn.synsets(word)
            for syn in synonyms:
              string_val = str(syn)
              split = string_val.split("(")
              temp_words.add(split[1].split(".")[0].strip("'"))
        set_words.update(temp_words)
      
        tagged = pos_tag(list(set_words))
        for tag in tagged:
          if tag[1] in verbs_list:
            set_verbs = get_verbs(tag[0])
            if None != set_verbs:
              set_words.update(set_verbs)
        final_unigram_set.update(set_words)

        instance_list = list(set_words)
        train_file.write("\t".join(instance_list))
        train_file.write("\n")


with open("final_unigram_tokens_12000.txt", "a") as myfile:
   print len(final_unigram_set)
   myfile.write("\t".join(final_unigram_set))



