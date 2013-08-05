# -*- coding: utf-8 -*-
import sqlite3
import sys
import re
import os.path

SQLITE_FILE = "shsnid.db"
ICELANDIC_ALPHABET = "aábdðeéfghiíjklmnoóprstuúvxyýþæö"
UPPER_ICELANDIC_ALPHABET = "AÁBDÐEÉFGHIÍJKLMNOÓPRSTUÚVXYÝÞÆÖ"

def main():
    if not os.path.isfile(SQLITE_FILE):
       print "SQL file not found: %s" % SQLITE_FILE
       return
    con = sqlite3.connect(SQLITE_FILE)
    cur = con.cursor()
    try:
        infile = sys.argv[1]
        oldword = sys.argv[2]
        newword = sys.argv[3]
    except IndexError:
        print "The script needs at least 3 arguments"
        return
    try:
        ofile = open(infile,"r")
        text  = ofile.read()
        ofile.close()
    except IOError:
        print "Could not open the file " + infile + ",does it exist?"
        return 
    sql_command = """select beygingarmynd,greiningarstrengur
                     from bin where uppflettiord='%s'"""
    cur.execute(sql_command % oldword)
    oldwords = cur.fetchall()
    cur.execute(sql_command % newword)
    newwords = cur.fetchall()
    con.close()
    errmsg = "Could not find the word %s in the dictionary,is it icelandic?"
    if len(oldwords) == 0:
        print errmsg % oldword
        return
    if len(newwords) == 0:
        print errmsg % newword
        return
    splitted = re.split(r"([^" + ICELANDIC_ALPHABET + \
                                 UPPER_ICELANDIC_ALPHABET + "])",text)
    for i,word in enumerate(splitted):
        if len(word) == 1 and word not in ICELANDIC_ALPHABET:
           continue
        for ow in oldwords:
            if ow[0].encode("utf8") == word.lower():
                nw = filter(lambda x: x[1] == ow[1],newwords)[0]
                splitted[i] = nw[0].encode("utf8")
                if word[0] in UPPER_ICELANDIC_ALPHABET:
                    alphabet_index = ICELANDIC_ALPHABET.index(splitted[i][0])
                    titlestring = UPPER_ICELANDIC_ALPHABET[alphabet_index] \
                                  + splitted[i][1:]
                    splitted[i] = titlestring #make first letter uppercase
                break
    replaced_text = "".join(splitted).strip()
    outname = infile[:infile.rfind(".")] + "_replaced.txt"
    if os.path.isfile(outname):
        num = 0
        newformat = infile[:infile.rfind(".")] + "_replaced_%d.txt"
        while os.path.isfile(newformat % num):
            num += 1
        outname = newformat % num
    outfile = open(outname,'w')
    outfile.write(replaced_text)
    outfile.close()
    print "SUCCESS: output written to %s" % outname

if __name__ == '__main__':
    main()
