import nltk, enchant, re
from nameparser.parser import HumanName
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from nltk.tag.stanford import StanfordNERTagger
import os
from nltk.stem import PorterStemmer
from nltk.corpus import names
from findTag import findTags 

#PreTrain DataSet of Standford
st = StanfordNERTagger('stanford-ner/english.all.3class.distsim.crf.ser.gz', 
                       'stanford-ner/stanford-ner.jar', encoding='utf-8')
dict_en = enchant.Dict("en_US")

#Clean text for the process
def cleaner(raw_str):
    strng = ''
    if type(raw_str) != type(""):
        raw_str = raw_str.encode(encoding='UTF-8', errors='strict')
    raw_str = re.sub('[^a-zA-Z0-9-_*.]', ' ', raw_str)
    raw_str = re.sub('[ áá âââââââââââââ¯âãï»¿]+', ' ', raw_str)
    for word in raw_str.split(" "):
        strng += "%s " % (word.strip())
    return strng.strip()

#It can clean HTML, script tag and stop words as well
def basicClean(file_path):
    text = open( file_path, 'r').read() 
    text = text.replace('<br>', '\n').replace('</option>', '\n')
    text = re.sub('<\s*a[^>]*>','\n', text)
    soup = BeautifulSoup(text, 'html.parser')
    content = soup.get_text()
    [s.extract() for s in soup('script')]
    text = soup.get_text()
    text = cleaner(text)
    text = re.sub('\W+|[0-9]', ' ', text)
    text = re.sub('\s+', ' ', text)
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    #Handle stopwords, Capital letter start and make it downcase
    filtered_sentence = [w.lower() for w in word_tokens if not w in stop_words and w[0].isupper() ]
    return filtered_sentence

#To convert to the root word 
def stemmer(list_words):
    stemmer = PorterStemmer()
    stam_result = [stemmer.stem(word) for word in list_words]
    return stam_result

#NLTK name of male.txt and female.txt file 
def inbuildName():
    name_list = names.words('male.txt') + names.words('female.txt')
    return set(name_list)

#Finder names 
def findNames(word_list, inbuildname):
    inbuildname = [j.lower() for j in inbuildname]
    find_arr = [ i for i in word_list if i in inbuildname]
    return set(find_arr)

#dictionary filtered
def checkDict(words):
    filtered = []
    for word in words:
        if dict_en.check(word) == False:
            filtered.append(word)
    return set(filtered)

#Main function
def main():
    file_root = '/Users/kamlesh/WorkSpace/simpleSpider/public/'
    for file_name in os.listdir(file_root):
        file_path = file_root + file_name 
        print(file_path)
        #Basic Filtered 
        filtered = basicClean(file_path)
        #Load inbuildnames
        inbuildname = inbuildName()
        #SET 1 name filter
        name_filter = findNames(filtered, inbuildname)
        #SET 2 dictionary filter
        dictionary_filter = checkDict(filtered)
        #Intersection Point of names
        intersect = list(set(name_filter).intersection(set(dictionary_filter)))
        people_names_raw = findTags(file_path, intersect)
        print(people_names_raw)
        print('')
        for tagger in people_names_raw:
            tag_name = word_tokenize(tagger)
            records = st.tag(tag_name)
            print(records)
            if 'PERSON' in str(records):
                print(tagger)
                print('**'*20)
        #org_arr = [other[0] for other in records if other[1] == 'ORGANIZATION']
        #break
        print('')
        print('**'*20)
main()
