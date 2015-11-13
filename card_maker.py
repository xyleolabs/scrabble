import sys
import getopt
from collections import defaultdict
from word_definer import Definer
from multiprocessing import Pool

d = defaultdict(list)

def insert_defined_word(def_tuple):
    global d
    key = ''.join(sorted(def_tuple[0]))
    value = "{0} - {1}".format(def_tuple[0], def_tuple[1])
    d[key].append(value)

def define(word):
    definer = Definer(word.strip())
    return definer.define()

def generate_flash_cards(word_list):
    print "Generating flash cards for {0}".format(word_list)

    pool = Pool(50)
    word_list_file = open(word_list, "r")
    flash_cards_file = open("flash_cards.txt", "w")

    try:
        for line in word_list_file.readlines():
            pool.apply_async(define, [line], callback=insert_defined_word)
    finally:
        if word_list_file:
            word_list_file.close()

    pool.close()
    pool.join()

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


def usage():
    print "card_maker.py -i <word list>"


def main():
    try:
        options, arguments = getopt.getopt(sys.argv[1:], "i:", ["input_list="])
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)

    word_list = None
    for opt, arg in options:
        if opt in ("-i", "--input_list"):
            word_list = arg
        else:
            assert False, "unhandled option"

    if word_list != None:
        generate_flash_cards(word_list)
    else:
        usage()


if __name__ == "__main__":
    main()
