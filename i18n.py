import yaml
import os
from string import Template

__translations = {}
__supportedLanguages = ('de', 'en')

def load(filename):
    basepath = os.path.dirname(os.path.abspath('__file__'))
    fullpath = os.path.join(basepath, filename)
    with open(fullpath, 'r', encoding='utf-8') as stream:
        termList = yaml.safe_load(stream)
        for term in termList:
            __translations[term['key']] = term['translations']

def isSupported(languageCode):
    return languageCode in __supportedLanguages

def t(id, languageCode, **args):
    string = __translations[id][languageCode]
    t = Template(string)
    return t.safe_substitute(args)
