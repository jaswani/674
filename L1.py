#!/usr/bin/env python
import re;
import os;
import math;
from stemming.porter2 import stem

#Compile the regex 
pattern = re.compile(r'<REUTERS .*?>(.*?)</REUTERS>',re.DOTALL);
body_regex = re.compile(r'<BODY>(.*?)</BODY>', re.DOTALL);
text_regex = re.compile(r'<TEXT.*?>(.*?)</TEXT>',re.DOTALL);
title_regex = re.compile(r'<TITLE>(.*?)</TITLE>',re.DOTALL);
word_regex = re.compile(r'[\s",;+&#\/@=\*\^-]+');
filter_regex = re.compile(r'[\d"+()<>\.:\[\]{}\?$!]+');
topic_regex = re.compile(r'<TOPICS>(.*?)</TOPICS>', re.DOTALL);

#init the dictionary
body_words = {};
stop_words = [];

#Helper function to return full path of reuter file to read

def listdir_fullpath(d):
      return [os.path.join(d, f) for f in os.listdir(d)]

#read the stopwords file and store in dictionary

f = open("stopwords");
for line in f:
  line = line.strip("\n");
  stop_words.append(line);
f.close();
#print stop_words;

#Global variables:
directory = "reuters";
docid = 0;
max_word_count = 0;

for filename in sorted(listdir_fullpath(directory)):
  #read the file
  f = open(filename, 'r');
  read_data = f.read();
  f.close();
  print "Processing File :" + filename;

  for match in pattern.finditer(read_data):
      article =  match.group(1); #print article; 
      #body = body_regex.search(article);
      text = text_regex.search(article);
      title = None;
      body = None;
      docid += 1;
      #rebuild the title dictionary every time to ensure body & title match!
      title_words = {};
      per_doc_word = {};
      max_per_doc = 0;

      if text:
          data = text.group(1);
          title = title_regex.search(data);
          body  = body_regex.search(data);
      else:
          print "Text not matched!\n";

      if title:
          title = title.group(1);
          title = filter_regex.sub("", title);
          for word in word_regex.split(title):
            word = word.strip('\'');
            word = word.lower();
            word = stem(word);
            if word not in stop_words:
              if word in title_words:
                title_words[word] += 1;
              else:
                title_words[word] = 1;

      if body:
          body = body.group(1);
          body = filter_regex.sub("", body);

          #keep track of word per document

          for word in word_regex.split(body): #data.split(): 
              #word = word.strip(',');
              #word = word.strip('.');
              word = word.strip('\'');
              word = word.lower();
              word = stem(word);
              if word not in stop_words:
                #store per_doc info for TF
                if word in per_doc_word:
                  per_doc_word[word] += 1;
                else:
                  per_doc_word[word] = 1;

                if max_per_doc < per_doc_word[word]:
                  max_per_doc = per_doc_word[word];

                if word in body_words:
#                    body_words[word] += 1; #bump up the count
                    body_words[word][0] += 1; #increment word count
                    if max_word_count < body_words[word][0]:
                      max_word_count = body_words[word][0]; #keep track of max_word_count

                    if(docid != body_words[word][1]):
                      body_words[word][1] += 1; #another document has this word
                      body_words[word][3] = docid #update last seen docid
                else:
#                    body_words[word] = 1; #enter the word into storage 
                    body_words.setdefault(word, []).append(1); #frequency
                    body_words.setdefault(word, []).append(1); # No of docs containing this word
                    body_words.setdefault(word, []).append(0.0); # Max TF for this word
                    body_words.setdefault(word, []).append(docid); #Last docid containing this word

          for word in title_words:
            if word in per_doc_word:
              per_doc_word[word] += 5; #increase weight by 5 for words in the body which are also in the title
              if max_per_doc < per_doc_word[word]:
                max_per_doc = per_doc_word[word];
            if word in body_words:
              body_words[word][0] += 5; #increase weight by 5 for words in the body which are also in the title
              if max_word_count < body_words[word][0]:
                max_word_count = body_words[word][0];


          #time to calculate TF
          #print "max_per_dpc =", max_per_doc;
          for word in per_doc_word:
            tf = per_doc_word[word]/float(max_per_doc);
            #print word, tf;
            if body_words[word][2] < tf:
              body_words[word][2] = tf;
      #break;
#Complete TFIDF calculation overwrite column 4
for word in body_words:
  body_words[word][3] = body_words[word][2] * math.log(float(docid)/body_words[word][1]);
#printing "Weighting titles in body";
#for key in title_words:
#  if key in body_words:
#    body_words[key] += 5; #increase weight by 5 for words in the body which are also in the title
#
#for key in sorted(body_words.keys(), key=str.lower):
#    print key, body_words[key];
#print "TITLE";
#for key in sorted(title_words.keys(), key=title_words.get):
#    print key, title_words[key];
#print "Docid = ", docid, " max_word_count = ", max_word_count;
#print "BODY";
vector = {};
count=0;
for key, value in sorted(body_words.items(), key=lambda e: e[1][3], reverse=True):
  #print key, value;
  vector[key] = 0;
  count+=1;
  if(count == 2000):
    break;


#print "Starting to write ...";
#opfile = open("Adjacency_list", 'w')
#
#docid = 0;
##time to write ..
#for filename in sorted(listdir_fullpath(directory)):
#  #read the file
#  f = open(filename, 'r');
#  read_data = f.read();
#  f.close();
#  print "Processing File :" + filename;
#
#  for match in pattern.finditer(read_data):
#      article =  match.group(1); #print article; 
#      #body = body_regex.search(article);
#      text = text_regex.search(article);
#      body = None;
#      topic = topic_regex.search(article);
#      docid += 1;
#      #rebuild the title dictionary every time to ensure body & title match!
#      per_doc_word = {};
#
#      if text:
#          data = text.group(1);
#          body  = body_regex.search(data);
#      else:
#          print "Text not matched!\n";
#
#      if body:
#          body = body.group(1);
#          body = filter_regex.sub("", body);
#
#          #keep track of word per document
#
#          for word in word_regex.split(body): #data.split(): 
#              #word = word.strip(',');
#              #word = word.strip('.');
#              word = word.strip('\'');
#              word = word.lower();
#              word = stem(word);
#              if word in vector:
#                if word in per_doc_word:
#                  per_doc_word[word] += 1;
#                else:
#                  per_doc_word[word] = 1;
#
#      if topic:
#        topic = topic.group(1);
#      else:
#        topic = "";
#
#      output = "";
#      output += "<DOCID: " + str(docid) + "> " + str(per_doc_word) + " <TOPIC> " + topic + "\n";
#      opfile.write(output);
##      break;
#
#opfile.close();
#
print "Starting to write (Sparse Vector)...";
opfile = open("Sparse_vector", 'w')

output = "<DOCID: XXXXXX> ";
for word in sorted(vector):
  output += word + " ";

output += "\n";

opfile.write(output);
docid = 0;
#time to write ..
for filename in sorted(listdir_fullpath(directory)):
  #read the file
  f = open(filename, 'r');
  read_data = f.read();
  f.close();
  print "Processing File :" + filename;

  for match in pattern.finditer(read_data):
      article =  match.group(1); #print article; 
      #body = body_regex.search(article);
      text = text_regex.search(article);
      body = None;
      topic = topic_regex.search(article);
      docid += 1;
      #rebuild the title dictionary every time to ensure body & title match!
      per_doc_word = [];

      if text:
          data = text.group(1);
          body  = body_regex.search(data);
      else:
          print "Text not matched!\n";

      if body:
          body = body.group(1);
          body = filter_regex.sub("", body);

          #keep track of word per document

          for word in word_regex.split(body): #data.split(): 
              #word = word.strip(',');
              #word = word.strip('.');
              word = word.strip('\'');
              word = word.lower();
              word = stem(word);
              if word in sorted(vector):
                per_doc_word.append(1);
              else:
                per_doc_word.append(0);


      if topic:
        topic = topic.group(1);
      else:
        topic = "";

      output = "";
      output += "<DOCID: " + str(docid) + "> " + str(per_doc_word) + " <TOPIC> " + topic + "\n";
      opfile.write(output);
#      break;

opfile.close();

