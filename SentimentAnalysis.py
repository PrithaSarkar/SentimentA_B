# -*- coding: utf-8 -*-

import pandas as pd
# nltk.download('punkt')
from nltk.tokenize import sent_tokenize, word_tokenize
from pandas import DataFrame

import MasterFile
import re
import string


# negative score
def negativeScore(tokenised_text, negative_list):
    score = 0
    for token in tokenised_text:
        if token in negative_list:
            score -= 1
    return score * (-1)


# positive score
def positiveScore(tokenised_text, positive_list):
    score = 0
    for token in tokenised_text:
        if token in positive_list:
            score += 1
    return score


# polarity score
def polarityScore(positive, negative):
    return (positive - negative) / ((positive + negative) + 0.000001)


# subjectivity score
def subjectivityScore(positive, negative, tokenised_text):
    return (positive + negative) / (len(tokenised_text) + 0.000001)


# average sentence length = average number of words per sentence
def avgsenlen(senlen, tokenised_text):
    return len(tokenised_text) / senlen

def syl(word):
    word = word.lower()
    exception_add = ['serious', 'crucial']
    exception_del = ['fortunately', 'unfortunately']
    co_one = ['cool', 'coach', 'coat', 'coal', 'count', 'coin', 'coarse', 'coup', 'coif', 'cook', 'coign', 'coiffe',
              'coof', 'court']
    co_two = ['coapt', 'coed', 'coinci']
    pre_one = ['preach']
    syls = 0
    disc = 0
    if len(word) <= 3:
        syls = 1
        return syls
    if word[-2:] == "es" or word[-2:] == "ed":
        doubleAndtripple_1 = len(re.findall(r'[eaoui][eaoui]', word))
        if doubleAndtripple_1 > 1 or len(re.findall(r'[eaoui][^eaoui]', word)) > 1:
            if word[-3:] == "ted" or word[-3:] == "tes" or word[-3:] == "ses" or word[-3:] == "ied" or word[
                                                                                                       -3:] == "ies":
                pass
            else:
                disc += 1
    le_except = ['whole', 'mobile', 'pole', 'male', 'female', 'hale', 'pale', 'tale', 'sale', 'aisle', 'whale', 'while']
    if word[-1:] == "e":
        if word[-2:] == "le" and word not in le_except:
            pass
        else:
            disc += 1
    doubleAndtripple = len(re.findall(r'[eaoui][eaoui]', word))
    tripple = len(re.findall(r'[eaoui][eaoui][eaoui]', word))
    disc += doubleAndtripple + tripple
    numVowels = len(re.findall(r'[eaoui]', word))
    if word[:2] == "mc":
        syls += 1
    if word[-1:] == "y" and word[-2] not in "aeoui":
        syls += 1
    for i, j in enumerate(word):
        if j == "y":
            if (i != 0) and (i != len(word) - 1):
                if word[i - 1] not in "aeoui" and word[i + 1] not in "aeoui":
                    syls += 1
    if word[:3] == "tri" and word[3] in "aeoui":
        syls += 1
    if word[:2] == "bi" and word[2] in "aeoui":
        syls += 1
    if word[-3:] == "ian":
        if word[-4:] == "cian" or word[-4:] == "tian":
            pass
        else:
            syls += 1
    if word[:2] == "co" and word[2] in 'eaoui':
        if word[:4] in co_two or word[:5] in co_two or word[:6] in co_two:
            syls += 1
        elif word[:4] in co_one or word[:5] in co_one or word[:6] in co_one:
            pass
        else:
            syls += 1
    if word[:3] == "pre" and word[3] in 'eaoui':
        if word[:6] in pre_one:
            pass
        else:
            syls += 1
    negative = ["doesn't", "isn't", "shouldn't", "couldn't", "wouldn't"]
    if word[-3:] == "n't":
        if word in negative:
            syls += 1
        else:
            pass
    if word in exception_del:
        disc += 1

    if word in exception_add:
        syls += 1
    return numVowels - disc + syls

def complex_word_count(tokenised_text):
    complex = 0
    for token in tokenised_text:
        if (syl(token)>2):
            complex += 1
    return complex

def percentage(tokenised_text, complex):
    return complex / len(tokenised_text)

# fog index
def fogind(avgsenlen, percomplexwords):
    return (0.4 * (avgsenlen + percomplexwords))


# average number of words per sentence
def avgwords(tokenised_text, senlen):
    return len(tokenised_text) / senlen


# word count
def wordcount(tokenised_text):
    return len(tokenised_text)


# personal pronouns
def pronouns(tokenised_text):
    count = 0
    pronoun_list = "i", "we", "my", "ours", "us"
    for previous_token, token in zip(tokenised_text, tokenised_text[1:]):
        if token in pronoun_list and previous_token != "the":
            count += 1
    return count


# average word length
def avgwordlen(tokenised_text):
    chars = 0
    for token in tokenised_text:
        for t in token:
            chars += 1
    return chars / len(tokenised_text)

def make_clickable(link):
    click = link.split('=')[0]
    return f'<a target="_blank" href="{link}">{click}</a>'


# stopword list
stopword_list = []
my_file = open("StopWords_Generic.txt", "r")
content_list = my_file.readlines()
for word in content_list:
    stopword_list.append(word[:-1].lower())


# negative word and positive word list
negative_list = []
positive_list = []
f_log = open('Load_MD_Logfile.txt', 'w')
md = (r'Loughran-McDonald_MasterDictionary_1993-2021.csv')
sentiment_dictionaries = MasterFile.load_masterdictionary(md, True, f_log, True)
for key in sentiment_dictionaries.keys():
    if key == 'negative':
        for key1 in sentiment_dictionaries[key].keys():
            negative_list.append(key1.lower())
    else:
        for key1 in sentiment_dictionaries[key].keys():
            positive_list.append(key1.lower())

xls_input = pd.ExcelFile('Input.xlsx')
input_df = pd.read_excel(xls_input, 'Sheet1')
columns = ["URL_ID", "URL", "POSITIVE SCORE", "NEGATIVE SCORE", "POLARITY SCORE",
           "SUBJECTIVITY SCORE", "AVG SENTENCE LENGTH",
           "PERCENTAGE OF COMPLEX WORDS", "FOG INDEX",
           "AVG NUMBER OF WORDS PER SENTENCE", "COMPLEX WORD COUNT",
           "WORD COUNT", "SYLLABLE PER WORD", "PERSONAL PRONOUNS", "AVG WORD LENGTH"]
output_df = pd.DataFrame(columns=columns)


output_df[["URL_ID", "URL"]] = input_df[["URL_ID", "URL"]]


max_row = int(output_df["URL_ID"].max())

for i in range(0, max_row-1):
    file = str(int(output_df["URL_ID"][i]))+".txt"

    # reading text from each file and analysing to write the necessary parameters in the output file
    text = open(file, 'r', encoding="utf-8").read()


    sentence_list = sent_tokenize(text)
    senlen = len(sentence_list)

    tokenised_text = word_tokenize(text)

    # removing stopwords and punctuations
    s = set(string.punctuation)
    for token in tokenised_text:
        if token in stopword_list:
            tokenised_text.remove(token)
        if token in s:
            tokenised_text.remove(token)

    total_syl = 0
    output_df.at[i, "POSITIVE SCORE"] = positiveScore(tokenised_text, positive_list)
    output_df.at[i, "NEGATIVE SCORE"] = negativeScore(tokenised_text, negative_list)
    output_df.at[i, "POLARITY SCORE"] = polarityScore(output_df.at[i, "POSITIVE SCORE"], output_df.at[i, "NEGATIVE SCORE"])
    output_df.at[i, "SUBJECTIVITY SCORE"] = subjectivityScore(output_df.at[i, "POSITIVE SCORE"], output_df.at[i, "NEGATIVE SCORE"], tokenised_text)
    output_df.at[i, "AVG SENTENCE LENGTH"] = avgsenlen(senlen, tokenised_text)
    output_df.at[i, "COMPLEX WORD COUNT"] = complex_word_count(tokenised_text)
    output_df.at[i, "PERCENTAGE OF COMPLEX WORDS"] = percentage(tokenised_text, output_df.at[i, "COMPLEX WORD COUNT"])
    output_df.at[i, "FOG INDEX"] = fogind(output_df.at[i, "AVG SENTENCE LENGTH"], output_df.at[i, "PERCENTAGE OF COMPLEX WORDS"])
    output_df.at[i, "AVG NUMBER OF WORDS PER SENTENCE"] = avgwords(tokenised_text, senlen)
    output_df.at[i, "WORD COUNT"] = wordcount(tokenised_text)
    for token in tokenised_text:
        total_syl += syl(token)
    output_df.at[i, "SYLLABLE PER WORD"] = total_syl / output_df.at[i, "WORD COUNT"]
    output_df.at[i, "PERSONAL PRONOUNS"] = pronouns(tokenised_text)
    output_df.at[i, "AVG WORD LENGTH"] = avgwordlen(tokenised_text)

output_df.to_excel("Output Data Structure.xlsx", sheet_name= "Sheet 1")