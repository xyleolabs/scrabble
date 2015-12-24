import sys
import getopt
from collections import defaultdict
from word_definer import Definer
from multiprocessing import Pool
from collections import OrderedDict

# d = defaultdict(list)
d = OrderedDict()

def insert_defined_word(def_tuple):
    global d
    word = ''.join(def_tuple[0].strip().split())
    definition = ' '.join(def_tuple[1].strip().split())

    key = ''.join(sorted(word))

    if len(def_tuple) == 1 or definition == "":
        value = word
    else:
        value = "*{0}* - {1}".format(word, definition)

    if key not in d:
        d[key] = [value]
    else:
        d[key].append(value)

def define(word):
    definer = Definer(word.strip())
    return definer.define()

def build_flash_cards():
    flash_cards_file = open("flash_cards.txt", "w")
    try:
        for anagram, words in d.items():
            card = "{0}\t".format(anagram)

            for word in words:
                card += "{0}\n".format(word)
            card += "@"

            flash_cards_file.write(card)
    finally:
        if flash_cards_file:
            flash_cards_file.close()

def build_flash_cards_sorted():
    flash_cards_file = open("flash_cards.txt", "w")
    try:
        it = iter(sorted(d.iteritems()))

        for anagram, words in it:
            card = "{0}\t".format(anagram)

            for word in words:
                card += "{0}\n".format(word)
            card += ";"

            flash_cards_file.write(card)
    finally:
        if flash_cards_file:
            flash_cards_file.close()

def generate_flash_cards(word_list, skip_define=False, def_included=False):
    print "Generating flash cards for {0}".format(word_list)

    word_list_file = open(word_list, "r")
    pool = None

    try:
        for line in word_list_file.readlines():
            if skip_define or def_included:
                if def_included:
                    word_def = tuple(line.split('\t'))
                    insert_defined_word(word_def)
                else:
                    insert_defined_word((line.strip(), ""))
            else:
                pool = Pool(50)
                pool.apply_async(define, [line], callback=insert_defined_word)
    finally:
        if word_list_file:
            word_list_file.close()

        if pool:
            pool.close()
            pool.join()

    if def_included:
        build_flash_cards()
    else:
        build_flash_cards_sorted()

def add_hook_entry(line, word_list_data):
    hook_parts = line.strip().lower().split()

    word = hook_parts[0]
    prefix = "NONE"
    suffix = "NONE"

    if len(hook_parts) == 3:
        prefix = hook_parts[0]
        word = hook_parts[1]
        suffix = hook_parts[2]
    elif len(hook_parts) == 2:
        if hook_parts[0] in word_list_data and hook_parts[1] not in word_list_data:
            word = hook_parts[0]
            suffix = hook_parts[1]
        elif hook_parts[0] not in word_list_data and hook_parts[1] in word_list_data:
            prefix = hook_parts[0]
            word = hook_parts[1]
        else:
            print "ERROR: Both parts are words.  Can't determine card for {0}".format(hook_parts)

    d[word].append("Prefixes: {0}".format(prefix))
    d[word].append("Suffixes: {0}".format(suffix))

def generate_hook_flash_cards(hook_list, word_list):
    print "Generating hook flash cards for {0}".format(hook_list)

    word_list_data = [line.strip().lower() for line in open(word_list, 'r')]

    word_list_file = open(hook_list, "r")

    try:
        map(lambda p: add_hook_entry(p, word_list_data), word_list_file)
    finally:
        if word_list_file:
            word_list_file.close()

    build_flash_cards_sorted()

def usage():
    print "card_maker.py -i <word list>"


def main():
    try:
        options, arguments = getopt.getopt(sys.argv[1:], "i:h:sd", ["input_list=,hook_list=,skip_define,definition_included"])
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)

    word_list = None
    hook_list = None
    skip_define = False
    for opt, arg in options:
        if opt in ("-i", "--input_list"):
            word_list = arg
        elif opt in ("-h", "--hook_list"):
            hook_list = arg
        elif opt in ("-s", "--skip_define"):
            skip_define = True
        elif opt in ("-d", "--definition_included"):
            def_included = True
        else:
            assert False, "unhandled option: {0}".format(opt)

    if hook_list:
        if word_list:
            generate_hook_flash_cards(hook_list, word_list)
        else:
            print "Please provide a word list with the hook list"
    else:
        if word_list:
            generate_flash_cards(word_list, skip_define, def_included)
        else:
            usage()



if __name__ == "__main__":
    main()
