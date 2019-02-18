from bs4 import BeautifulSoup
import re 
from collections import Counter

def findTags(file_path, p_name):
    content = open(file_path, 'rb').read()
    soup = BeautifulSoup(content, 'html.parser')
    hyp_tags_arr = []
    for person in p_name:
       #results = soup.body.find_all(string=re.compile('.*{0}.*'.format(person), re.IGNORECASE), recursive=True)
        results = soup.find_all('', text= re.compile(person, re.IGNORECASE))
        for result in results:
            pre = result.find_parent()
            pre = pre.text
            pre = re.sub('\W', ' ', pre)
            pre = re.sub('\s+', ' ', pre)
            length = pre.split(' ')
            if not bool(re.search(r'\d', str(result))) and len(length) <= 8:
                main_tags = result.find_parent()
                pro_tags = str(result.find_parent())
                hyp_tags = re.findall('<[a-zA-Z]+.*?(?<!\?)>', pro_tags)
                tags = ';'.join(hyp_tags)
                hyp_tags_arr.append(tags)

    common_tag = hypTags(hyp_tags_arr)
    tag_values = getSyntax(common_tag)
    getnames = getNames(file_path, tag_values, p_name)
    return getnames

#Lambda Function 
def hypTags(hyp_tags_arr):
    data = Counter(hyp_tags_arr)
    return data.most_common(1)

#Get Syntax BS4
def getSyntax(common_tag):
    tag_value = common_tag[0][0].replace('<','').replace('>','')
    tag_count = common_tag[0][1]
    make = tag_value.split(' ')
    tag1 = make[0]
    pre_tag = make[1].split('=')
    tag2 = pre_tag[0].replace('"','')
    tag3 = pre_tag[1].replace('"','')
    return [tag1, tag2, tag3]

#Get names 
def getNames(file_name, tag, p_name):
    content = open(file_name, 'rb').read()
    soup = BeautifulSoup(content, 'html.parser')
    strng_arr = []
    for people_name in soup.find_all(tag[0], {tag[1]: tag[2]}):
        people_name = people_name.text
        calc = people_name.split(' ')
        strng_arr.append(people_name)
    return strng_arr
