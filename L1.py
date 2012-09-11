#!/usr/bin/env python
import re;
import os;
from stemming.porter2 import stem

#Compile the regex 
pattern = re.compile(r'<REUTERS .*?>(.*?)</REUTERS>',re.DOTALL);
body_regex = re.compile(r'<BODY>(.*?)</BODY>', re.DOTALL);
text_regex = re.compile(r'<TEXT.*?>(.*?)</TEXT>',re.DOTALL);
title_regex = re.compile(r'<TITLE>(.*?)</TITLE>',re.DOTALL);
word_regex = re.compile(r'[\s",;+&#\/@=\*-]+');
filter_regex = re.compile(r'[\d"+()<>\.:\[\]{}\?$]+');

#init the dictionary
body_words = {};
title_words = {};
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

directory = "reuters";

for filename in listdir_fullpath(directory):
  #read the file
  f = open(filename, 'r');
  read_data = f.read();
  f.close();
#  print "Processing File :" + filename;

  for match in pattern.finditer(read_data):
      article =  match.group(1); #print article; 
      #body = body_regex.search(article);
      text = text_regex.search(article);
      title = None;
      body = None;
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
#            word = stem(word);
            if word not in stop_words:
              if word in title_words:
                title_words[word] += 1;
              else:
                title_words[word] = 1;

      if body:
          body = body.group(1);
          body = filter_regex.sub("", body);

          for word in word_regex.split(body): #data.split(): 
              #word = word.strip(',');
              #word = word.strip('.');
              word = word.strip('\'');
              word = word.lower();
              word = stem(word);
              if word not in stop_words:
                if word in body_words:
                    body_words[word] += 1; #bump up the count 
                else:
                    body_words[word] = 1; #enter the word into storage 
      #break;

#printing "Weighting titles in body";
for key in title_words:
  if key in body_words:
    body_words[key] += 5; #increase weight by 5 for words in the body which are also in the title

#for key in sorted(body_words.keys(), key=str.lower):
#    print key, body_words[key];
print "TITLE";
for key in sorted(title_words.keys(), key=title_words.get):
    print key, title_words[key];
print "BODY";
for key in sorted(body_words, key=body_words.get):
    print key, body_words[key];

