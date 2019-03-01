from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup, Comment
from nltk.tag.stanford import StanfordNERTagger
import os, re 
from nltk.corpus import stopwords

#PreTrain DataSet of Standford
nlp_model = 'stanford-ner/english.all.3class.distsim.crf.ser.gz'
standford_jar = 'stanford-ner/stanford-ner.jar'
st = StanfordNERTagger( nlp_model, standford_jar, encoding='utf-8')

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
    soup = BeautifulSoup(text, 'html.parser')
    [s.decompose() for s in soup('script')]
    [s.decompose() for s in soup('select')]
    selects = soup.findAll("style", {"type":"text/css"})
    for match in selects:
        match.decompose()
    for element in soup(text=lambda text: isinstance(text, Comment)):
        element.extract()
    text = str(soup)
    text = re.sub("""</?\w+((\s+\w+(\s*=\s*(?:".*?"|'.*?'|[^'">\s]+))?)+\s*|\s*)/?>""",'\n', text)
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text()
    text = re.sub('\n+','\n', text)
    return text

#Main function
def main():
    file_root = '/Users/kamlesh/WorkSpace/simpleSpider/public/'
    count = 1
    for file_name in os.listdir(file_root):
        file_path = file_root + file_name
        file_path = '/Users/kamlesh/WorkSpace/simpleSpider/public/400e169856f7498eb560545713484059.htm'
        filtered = basicClean(file_path)
        removed = [ i.strip() for i in filtered.split('\n') if i and len(i.strip(' ')) > 1 ]
        filtered = list(set(removed))
        possible_names = [ i.strip() for i in removed if len(i) < 40 ]
        possible_names = [ i.strip() for i in possible_names if re.sub('\W+|\d+','', i)]
        possible_names = list(set(possible_names))
        possible_names = [ i.strip() for i in possible_names if len(i.split(' ')) < 9 ] 
        
        stop_words = set(stopwords.words('english'))
        stop_word = [ i.lower() for i in stop_words ]
        str_name = ' '.join(possible_names)
        str_name = re.sub('\W+',' ', str_name)
        word_token = word_tokenize(str_name)
        word_token = [ w for w in word_token if not w.lower() in stop_words and w[0].isupper() ]
        st_word_token = [ re.sub('\W+|\d+','',i) for i in word_token if re.sub('\W+|\d+','',i)] 
        st_word_token = [ i for i in word_token if len(i) > 2 ]
        st_word_token = list(set(st_word_token))
        #print(st_word_token)
        st_word_token.sort()
        print(st_word_token)
        st_arr = st.tag(st_word_token)
        st_arr.sort()
        print(st_arr)
        #proposed_name = [ i[0] for i in st_arr if 'PERSON' in i]
        #proposed_name = [i[0] for i in proposed_name ]
        #proposed_name = [i for i in proposed_name if len(re.sub('\W+','',i)) > 1]
        #proposed_name.sort()
        #aggr_arr = list(set(aggr_arr + proposed_name)) 
        print(proposed_name)
        print(file_path)
        print('')
        print('**'*20)
        print('Count %s'%count)
        count += 1
        break
main()
