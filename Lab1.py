#!/usr/bin/env python
import re;

#init the dictionary
storage = {};

#read the file
f = open("reut2-000.sgm", 'r');
read_data = f.read();
f.close();

#Compile the regex 
pattern = re.compile(r'<REUTERS .*?>(.*?)</REUTERS>',re.DOTALL); 
body_regex = re.compile(r'<BODY>(.*?)</BODY>', re.DOTALL);
text_regex = re.compile(r'<TEXT .*?>(.*?)</TEXT>',re.DOTALL); 
word_regex = re.compile(r'[\s\'";+]+');

for match in pattern.finditer(read_data): 
    article =  match.group(1); #print article; 
    body = body_regex.search(article); 
    if body: 
        data =  body.group(1); 
    else: 
        #print article;
        text = text_regex.search(article);
        print text.group(1);
    for word in word_regex.split(data): #data.split(): 
        word = word.strip(',');
        word = word.strip('.');
        if word in storage:
            storage[word] += 1; #bump up the count 
        else: 
            storage[word] = 1; #enter the word into storage 
    #break;

for key in sorted(storage.keys()):
    print key, storage[key];
