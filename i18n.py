import yaml
import os
from i18nTerms import Terms
from string import Template

__translations = {}
__supported_languages = []

def load(relativeDir):
    basepath = os.path.dirname(os.path.abspath('__file__'))
    dirpath = os.path.join(basepath, relativeDir)
    for file in os.listdir(dirpath):
        filename = file.split('.')
        if filename[0] == 'web' and filename[2] == 'yml':
            lang = filename[1]
            assert len(lang) == 2 and lang.islower, 'language code should be 2 characters long and all lower case'

            __supported_languages.append(lang)
            with open(os.path.join(dirpath, file), 'r', encoding='utf-8') as stream:
                termList = yaml.safe_load(stream)
                __translations[lang] = termList
            # check against enum
            for term in Terms:
                assert __translations[lang][term.name] is not None, 'Term '+term.name+' not found in '+lang+' web translation'


def is_supported(language):
    return language in __supported_languages

def translate(term, language, **args):
    string = __translations[language][term.name]
    t = Template(string)
    return t.safe_substitute(args)
