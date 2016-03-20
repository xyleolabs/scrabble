__author__ = 'jrosensweig'

from HTMLParser import HTMLParser

INITIAL = "INITIAL"
PARSE_WORD = "PARSE_WORD"
PARSE_DEF = "PARSE_DEF"
TERMINAL = "TERMINAL"

# create a subclass and override the handler methods
class WordDefinitionParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.word = None
        self.definition = None
        self.definition_found = False
        self.state = INITIAL

    def get_definition(self):
        return self.word, self.definition

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            self.definition_found = self.contains_word_definition_class(attrs)
        elif self.definition_found:
            if tag == "h4":
                self.state = PARSE_WORD

    def contains_word_definition_class(self, attrs):
        result = False
        for attr in attrs:
            if attr[0] == "class":
                if attr[1] == "word-definition":
                    result = True
        return result

    def handle_endtag(self, tag):
        if tag == "div" and self.definition_found:
            self.definition_found = False
        elif self.definition_found:
            if tag == "h4":
                self.state = PARSE_DEF

    def handle_data(self, data):
        if self.state == PARSE_WORD:
            self.word = data.strip()
        elif self.state == PARSE_DEF:
            self.definition = data.strip()
            self.state = TERMINAL
