import bs4
import string
import pymysql
import nltk
from items import Content
from nltk import word_tokenize,pos_tag
from nltk import Text

def rank_dict (dict1,dict2):
    score = 0
    for key in dict1:
        if (key in dict2.keys()):
            score += dict2[key]

    return score


def rank_text(Content):
    '''
    ranks the text content of American Literature, based on the verbs their readings had
    '''
    preferences = dict()
    verbs_tags = ('VB','VBD','VBG','VBN','VBP','VBZ')
    if (Content['type'] != 'Book'):
        story = word_tokenize(Content['text'])
        story = pos_tag(story)
        length = len(story)
        #We try to get the words with most meaning
        for tag in story:
            if (tag[1] in verbs_tags):
                preferences[tag[0].strip(string.punctuation)]= preferences.get(tag[0].strip(string.punctuation),0) + 1

    else:
        length = 0
        for chapter in Content['text']:
            story = word_tokenize(Content['text'][chapter])
            story = pos_tag(story)
            length += len(story)
            for tag in story:
                if (tag[1] in verbs_tags):
                    preferences[tag[0].strip(string.punctuation)]= preferences.get(tag[0].strip(string.punctuation),0) + 1


    return (length, print_dict(preferences))

#______________________________________________________________________________#
def extract_text(body,null_tags):
    '''
    Receives a tag with text on its children, return (String) the text of every tag which name is
    not in the tuple null_tags
    '''

    text = list()
    for child in body.children:
        save = True
        if (child.name in null_tags or isinstance(child,bs4.element.NavigableString)):
            continue

        for desc in child.descendants:
            name = desc.name
            if (name == None):
                continue
            if (name in null_tags):
                save = False
                break
        if (save):
            text.append(child.get_text())

    return "".join(text)
#______________________________________________________________________________#
def add_dicts(dict1,dict2):
    keys1 = dict1.keys()
    keys2 = dict2.keys()
    keys = list()
    if (keys1 == None):
        return dict2
    if (keys2 == None):
        return dict1

    for key in keys1:
        if (key in keys2):
            continue
        keys.append(key)

    for key in keys2:
        keys.append(key)

    new_dict = dict()
    for key in keys:
        new_dict[key] = dict1.get(key,0) + dict2.get(key,0)

    return new_dict
#______________________________________________________________________________#
def get_csv_dict(csv):
    csv = csv.split(',')
    dictionary = dict()

    for data in csv:
        dat = data.split(' ')
        dictionary.update({dat[0]:int(dat[1])})

    return dictionary
#______________________________________________________________________________#
def print_dict(dict):
    preferences = ''
    max = 0
    values = dict.values()
    for value in values:
        if (max < value):
            max = value

    for key in dict:
        #if (dict[key] < max/2):
        #    continue

        preferences += key+' '+str(dict[key])+','

    return preferences[0:len(preferences)-1]
#______________________________________________________________________________#
def clean_string(text):
    text = text.lower()
    for punct in string.punctuation:
        if (punct == "-"):
            continue
        text = text.replace(punct,"")

    return text.replace(" ","-")
#______________________________________________________________________________#
