import yaml
import os
from string import Template

__translations = {}
__supported_languages = ('de', 'en')

def load(filename):
    basepath = os.path.dirname(os.path.abspath('__file__'))
    fullpath = os.path.join(basepath, filename)
    with open(fullpath, 'r', encoding='utf-8') as stream:
        termList = yaml.safe_load(stream)
        for term in termList:
            __translations[term['key']] = term['translations']

def is_supported(language):
    return language in __supported_languages

def translate(id, language, **args):
    string = __translations[id][language]
    t = Template(string)
    return t.safe_substitute(args)

