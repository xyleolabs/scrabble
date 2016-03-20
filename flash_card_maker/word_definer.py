import urllib
import urllib2
from word_definition_parser import WordDefinitionParser

DEF_NOT_FOUND = ""

__author__ = 'jrosensweig'

HASBRO_URL = "http://scrabble.hasbro.com/en-us/tools"


class Definer():
    def __init__(self, word):
        self.parser = WordDefinitionParser()
        self.word = word

    def define(self):
        args = dict()
        args["dictWord"] = self.word

        req_url = HASBRO_URL
        req = urllib2.Request(req_url)
        req.get_method = lambda: 'POST'
        req.add_data(urllib.urlencode(args))

        response = urllib2.urlopen(req)
        page = response.read()

        self.parser.feed(page)

        word_def = self.parser.get_definition()

        if word_def[0] == "OOPS!":
            return self.word.strip(), DEF_NOT_FOUND

        return word_def

# Main
if __name__ == "__main__":
    d = Definer("cwm")
    definition = d.define()
    print "{0}\t{1}".format(definition[0], definition[1])
