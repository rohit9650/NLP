#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# In[01]
#importing packages for usage
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import os
import string
"""
    Speed as Value = Speed(v)
    Speed as Question = Speed(Q)
    Distance as Value = Distance(V)
    Distance as Question = Distance(Q)
    Time as Value = Time(V)
    Time as Question = Time(Q)
    Acceleration as Value = Acceleration(V)
    Acceleration as Question = Acceleration(Q)
"""
# In[02]
#function to test whether a sentence is a question or not
def isQuestion(sentence):
    flag = False
    question_terms = ["calculate","what","why","when","how","find","determine"]
    if sentence.endswith("?"):
        return True
    else:
        terms = word_tokenize(sentence)
        for term in terms:
            if term.lower() in question_terms:
                flag = True
    return flag
# In[03]
#copied from github,match multiple regular expressions
def replace(expr, substitutions):
    substrings = sorted(substitutions, key=len, reverse=True)
    regex = re.compile('|'.join(map(re.escape, substrings)))
    return regex.sub(lambda match: substitutions[match.group(0)], expr)
# In[04]
#method to standardize speed
def standardizeSpeed(text):
    """convert the units to the standard form as prescribed"""
    substitutions={"metres per second":"l/t",
                   "metres per hour":"l/t",
                   "metres per minute":"l/t",
                   "kilometres per second":"l/t",
                   "kilometres per hour":"l/t",
                   "miles per second":"l/t",
                   "miles per hour":"l/t",
                   "miles per minute":"l/t",
                   "konts":"l/t",
                   "feet per second":"l/t",
                   }
    #check for short forms first
    short_form = {"km/hr":"l/t",
                  "km/h":"l/t",
                  "m/s":"l/t",
                  "mi/h":"l/t",
                  "kmh":"l/t"
                  }
    term_list = word_tokenize(text)
    output_length = ""
    for word in term_list:
        if word.lower() in short_form.keys():
            output_length = output_length + " " + short_form[word.lower()]
        else:
            output_length = output_length + " " + word
    #output_length = replace(text,substitutions)
    return output_length
# In[05]
def standardizeTime(text):
    #convert the time to the standard form
    substitutions={"seconds":"t",
                   "minutes":"t",
                   "hours":"t",
                   "second":"t",
                   "minute":"t",
                   "hour":"t",
                   "s":"t"
                   }
    term_list = word_tokenize(text)
    output_length = ""
    for word in term_list:
        if word.lower() in substitutions.keys():
            output_length = output_length + " " + substitutions[word.lower()]
        else:
            output_length = output_length + " " + word
    #output_length = replace(text,substitutions)
    return output_length
# In[06]
def standardizeLength(text):
    substitutions={"metres":"l",
                   "miles":"l",
                   "degree":"l",
                   "meters":"l",
                   "miles":"l",
                   "kilometres":"l",
                   "centimetres":"l",
                   "ms":"l",
                   "mi":"l",
                   "m":"l",
                   "cms":"l",
                   "kms":"l",
                   "m":"l",
                   "cm":"l",
                   "km":"l",
                   str(chr(176)):"l" #degree symbol
                   }
    term_list = word_tokenize(text)
    output_length = ""
    for word in term_list:
        for punct in string.punctuation:
            if punct != '/':
                word = word.replace(punct,"")
        if word.lower() in substitutions.keys():
            output_length = output_length + " " + substitutions[word.lower()]
        else:
            output_length = output_length + " " + word
    return output_length
# In[07]
def standardizeAcc(text):
    substitutions={"m/s2":" l/t2",
                   "m/s^2":" l/t2"
                   }
    output_length = replace(text,substitutions)
    return output_length
# In[08]
def splitNumbersAndUnits(text):
    term_list = word_tokenize(text)
    #print(term_list)
    new_term = ""
    change_terms = {}
    problem = []
    pos = 0
    for term in term_list:
        if term[0].isdigit():
            #print(term)
            problem.append(term)
    for word in problem:
        for i in range(0,len(word)):
            #print(word[i])
            if not word[i].isdigit():
                pos = i
                #print(pos)
                break
        #print(word[:pos])
        #print(word[pos:])
        new_term = word[:pos] + " " + word[pos:]
        change_terms[word] = new_term
        #print(new_term)
    #print(change_terms)
    new_text = ""
    for term in term_list:
        if term in change_terms.keys():
            new_text = new_text + " " + change_terms[term]
        else:
            new_text = new_text + " " + term
    return new_text
# In[09]
def standardizeText(text):
    #insert accleration standardize here
    accleration = standardizeAcc(text)
    speed = standardizeSpeed(accleration)
    time_speed = standardizeTime(speed)
    length_time_speed =  standardizeLength(time_speed)
    final_standard=""
    tokens = word_tokenize(length_time_speed)
    #checking for spurious units
    for i in range(0,len(tokens)):
        #print(length_time_speed[i])
        if i >= 0:
            if tokens[i] == 'l/t':
                if (i-1) >= 0 and not tokens[i-1].isdigit():
                    #length_time_speed[i] = " "
                    final_standard = final_standard + " "
                else:
                    final_standard = final_standard + " " + tokens[i]
            elif tokens[i] == 'l':
                if (i-1) >= 0 and not tokens[i-1].isdigit():
                    #length_time_speed[i] = " "
                    final_standard = final_standard + " "
                else:
                    final_standard = final_standard + " " + tokens[i]
            elif tokens[i] == 't':
                if (i-1) >= 0 and not tokens[i-1].isdigit():
                    #length_time_speed[i] = " "
                    final_standard = final_standard + " "
                else:
                    final_standard = final_standard + " " + tokens[i]
            elif tokens[i] == 'l/t2':
                if (i-1) >= 0 and not tokens[i-1].isdigit():
                    #length_time_speed[i] = " "
                    final_standard = final_standard + " "
                else:
                    final_standard = final_standard + " " + tokens[i]
            else:
                final_standard = final_standard + " " + tokens[i]
    return final_standard
# In[10]
#creating dictionaries for synomyms
distance = {'distance':"distance",
            'displacement':"displacement",
            'area':"area",
            'height':"height",
            'far':"far",
            'tall':"tall",
            'length':"length",
            'orbit':"orbit",
            'high':"high",
            'angle':"angle",
            'altitude':"altitude",
            'radius':"radius",
            'scope':"scope",
            'seperation':"seperation",
            'size':"size",
            'stretch':"stretch",
            'width':"width",
            'degreee':"degree",
        }
speed = {'velocity':"velocity",
         'agility':"agility",
         'pace':"pace",
         'quickness':"quickness",
         'swiftness':"swiftnes",
         'speed':"speed",
         'fast':"fast"
         }
time = {'time':"time",
        'long':"long",
        'seconds':"seconds",
        'hang time':"hang time",
        'hangtime':"hangtime",
        'hang-time':"hang-time",
        'in the air':"in the air"
        }

accleration = {'acceleration':"acceleration",
               'deceleration':"deceleration"
               }
# In[11]
#this method is always run after the standardizeText method
def extractInformation(sentence):
    information = {'Speed(V)':0,
                   'Speed(Q)':0,
                   'Distance(V)':0,
                   'Distance(Q)':0,
                   'Time(V)':0,
                   'Time(Q)':0,
                   'Acceleration(V)':0,
                   'Acceleration(Q)':0
                   }
    term_list = word_tokenize(sentence)
    #print(term_list)
    for word in term_list:
        if word == "l/t":
            #print("Speed as Value")
            information['Speed(V)'] = 1
        if word == "l":
            #print("Distance as Value")
            information['Distance(V)'] = 1
        if word == "t":
            #print("Time as Value")
            information['Time(V)'] = 1
        if word == "l/t2":
            #print("Acceleration as Value")
            information['Acceleration(V)'] = 1
    for i in range(len(term_list)):
        word = term_list[i]
        if word.lower() in speed.values():
            flag = False
            for j in range(i+1,len(term_list)):
                if "l/t" == term_list[j]:
                    flag = True
                    break
            if flag :
                information['Speed(V)'] = 1
                #print("Speed as Value")
            else:
                information['Speed(Q)'] = 1
                #print("Speed as Question")
        if word.lower() in distance.values():
            flag = False
            punctuation = "!#$%&'()*+,-.:;<=>?@[\]^_`{|}~"
            useless = False
            for j in range(i+1,len(term_list)):
                if "l" == term_list[j]:
                    flag = True
                    break
                elif term_list[j] in punctuation:
                    useless = True
            if flag and not useless:
                information['Distance(V)'] = 1
                #print("Distance as Value")
            else:
                if not useless:
                    information['Distance(Q)'] = 1
                    #print("Distance as Question")
        if word.lower() in time.values():
            flag = False
            for j in range(i+1,len(term_list)):
                if "t" == term_list[j]:
                    flag = True
                    break
            if flag :
                information['Time(V)'] = 1
                #print("Time as Value")
            else:
                information['Time(Q)'] = 1
                #print("Time as Question")
        if word.lower() in accleration.values():
            flag = False
            for j in range(i+1,len(term_list)):
                if "l/t2" == term_list[j]:
                    flag = True
                    break
            if flag :
                information['Acceleration(V)'] = 1
                #print("Accleration as Value")
            else:
                information['Acceleration(Q)'] = 1
                #print("Accleration as Question")
    return information
# In[12]
def is_useless(statement):
    term_list = word_tokenize(statement)
    #print(term_list)
    flag = True
    for word in term_list:
        if word == "l/t":
            flag =  False
            break
        if word == "t":
            flag = False
            break
        if word == "l":
            flag = False
            break
        if word == "l/t2":
            flag = False
            break
    return flag
# In[13]
def eliminateBrackets(problem):
    bracketed=problem[problem.find("(")+1:problem.find(")")]#finding string between 2 brackets
    #if useless then eliminate the bracketed part
    print(is_useless(bracketed))
    if is_useless(bracketed):
        temp_new_problem = problem.replace(bracketed," ")
        new_problem = temp_new_problem.replace("( )"," ")
        return new_problem
    else:
        return problem
# In[14]
""" Returns a list containing all files in a directory"""
def get_files(dir_path):
    files = []
    for file in os.listdir(dir_path):
        files.append(file)
    return files
# In[15]
def list_indexing_terms(dir_path):
    index = {}
    #results = open("/home/swarnadeep/Documents/Courses/2nd_Sem/NLP/Assignments/write.txt","w")
    files = get_files(dir_path)
    count = 0
    for file in files:
        file_path = dir_path + "/" + file
        #processing each file seperately
        fp = open(file_path,"r")
        file_content = fp.read()
        index[file] = extractInformation(standardizeText(splitNumbersAndUnits(file_content)))
        count = count + 1
    print(count)
    print(index)
# In[16]
list_indexing_terms("/home/swarnadeep/Documents/Courses/2nd_Sem/NLP/Assignments/Corpus")
