from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from nltk.tag.stanford import StanfordNERTagger
import os, re 

#PreTrain DataSet of Standford
st = StanfordNERTagger('stanford-ner/english.all.3class.distsim.crf.ser.gz', 
                       'stanford-ner/stanford-ner.jar', encoding='utf-8')

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
    content = soup.body.get_text()
    [s.extract() for s in soup('script')]
    text = soup.get_text()
    text = re.sub('\n+','\n', text)
    return text

#Main function
def main():
    file_root = '/Users/kamlesh/WorkSpace/simpleSpider/public/'
    names_arr = []
    for file_name in os.listdir(file_root):
        file_path = file_root + file_name 
        filtered = basicClean(file_path)
        removed_spaces = [ i.strip() for i in filtered.split('\n') if i and len(i.strip(' ')) > 1 ]
        removed_spaces = list(set(removed_spaces))
        possible_names = [i.strip() for i in removed_spaces if len(i.split(' ')) < 9]

        for tagname in possible_names:
            tag_name = word_tokenize(tagname)
            records = st.tag(tag_name)
            if 'PERSON' in str(records):
                names_arr.append(tagname)
    print('**'*20)
    print(names_arr)
    print('')

main()
