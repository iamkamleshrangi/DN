import yaml

with open('/Users/kamlesh/WorkSpace/DetectNames/lib/config.yaml', 'r') as f:
    doc = yaml.load(f)

def handler(tree,node):
    return doc[tree][node]
