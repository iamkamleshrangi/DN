import os, re
from lib.mongodb import operations
from lib.config_handler import handler
from nltk.corpus import names

obj = operations()
spot_db = handler('database','spot_db')
spot_col = handler('database', 'spot_col')
#Run Defination
def run():
    male_names = names.words('male.txt') 
    female_names  = names.words('female.txt')
    json_male = [{'name': i.lower(), 'source': 'male.txt'} for i in male_names] 
    json_female = [{'name': i.lower(), 'source': 'female.txt'} for i in female_names]
    #Bulk Insert Name [male.txt]
    obj.bulk_insert(spot_db, spot_col, json_male)
    #Bulk Insert Name [female.txt]
    obj.bulk_insert(spot_db, spot_col, json_female)

def execute():
    root_path = 'namesCsv/'
    name_arr = []
    for file_name in os.listdir(root_path):
        file_path = root_path + file_name
        reader = open(file_path, 'r').read()
        name_arr = reader.split("\n")
        #Collect Names 
        for name in name_arr:
            if len(name) <= 2:
                pass
            else:
                pre_name = re.sub('\W+|\d+',' ', name)
                for p_name in pre_name.split(' '):
                    if len(p_name) <= 2:
                        pass
                    else:
                        n_name = p_name
                        p_name = p_name.strip().lower()
                        file_name = file_name.strip().lower()
                        print('Name:', p_name, ' | ', n_name)
                        datah = {'name': p_name, 
                                'source': file_name }
                        name_arr.append(datah)

    #print(len(name_arr))

execute()

