#!/usr/bin/env python
import re;
from stemming.porter2 import stem

#init the dictionary
body_words = {};
title_words = {};

#read the file
f = open("reut2-000.sgm", 'r');
read_data = f.read();
f.close();

#Compile the regex 
pattern = re.compile(r'<REUTERS .*?>(.*?)</REUTERS>',re.DOTALL); 
body_regex = re.compile(r'<BODY>(.*?)</BODY>', re.DOTALL);
text_regex = re.compile(r'<TEXT.*?>(.*?)</TEXT>',re.DOTALL); 
title_regex = re.compile(r'<TITLE>(.*?)</TITLE>',re.DOTALL); 
word_regex = re.compile(r'[\s",;+&#\/-]+');
filter_regex = re.compile(r'[\d\'"+()<>\.:\[\]{}]+');

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
    if body:
        body = body.group(1);
        body = filter_regex.sub("", body);

        for word in word_regex.split(body): #data.split(): 
            #word = word.strip(',');
            #word = word.strip('.');
            word = word.lower();
            word = stem(word);
            if word in body_words:
                body_words[word] += 1; #bump up the count 
            else: 
                body_words[word] = 1; #enter the word into storage 
    #break;

for key in sorted(body_words.keys(), key=str.lower):
    print key, body_words[key];
