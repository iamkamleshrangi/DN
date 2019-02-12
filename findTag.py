from bs4 import BeautifulSoup
import re 

def findTags():
    file_path = "/Users/kamlesh/WorkSpace/simpleSpider/public/d8f1278b9fbc4077bebfb2d8732498f4.htm"
    p_name = ['april', 'janet', 'brody', 'chen', 'mateo', 'kara', 'rosa', 'june', 'caroline', 'boyd', 'vanessa', 'francisco', 'daniel']

    content = open(file_path, 'rb').read()
    soup = BeautifulSoup(content, 'html.parser')
    for person in p_name:
       #results = soup.body.find_all(string=re.compile('.*{0}.*'.format(person), re.IGNORECASE), recursive=True)
        results = soup.find_all('', text= re.compile(person, re.IGNORECASE))
        for result in results:
            pre = re.sub('\W', ' ', result)
            pre = re.sub('\s+', ' ', pre)
            length = pre.split(' ')
            if not bool(re.search(r'\d', str(result))) and len(length) <= 8:
                print(length)
                print(result)
                print(len(length))
                print('')
                print(result.find_parent())
                print('====')
findTags()
