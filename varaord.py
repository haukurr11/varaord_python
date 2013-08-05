# -*- coding: utf-8 -*-
import sqlite3
import sys
import re
import os.path

SQLITE_FILE = "shsnid.db"
ICELANDIC_ALPHABET = "aábdðeéfghiíjklmnoóprstuúvxyýþæö"

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
        text = open(infile,"r").read()
    except IOError:
        print "Could not open the file " + infile + ",does it exist?"
        return 
    sql_command = """select beygingarmynd,greiningarstrengur
                     from bin where uppflettiord='%s'"""
    cur.execute(sql_command % oldword)
    oldwords = cur.fetchall()
    errmsg = "Could not find the word %s in the dictionary,is it icelandic?"
    if len(oldwords) == 0:
        print errmsg % oldword
        return
    cur.execute(sql_command % newword)
    newwords = cur.fetchall()
    if len(newwords) == 0:
        print errmsg % newword
        return
    splitted = re.split(r"([^" + ICELANDIC_ALPHABET + \
                                 ICELANDIC_ALPHABET.upper() + "])",text)
    for i,word in enumerate(splitted):
        if len(word)> 1:
            for ow in oldwords:
                if ow[0].encode("utf8") == word:
                    nw = filter(lambda x: x[1] == ow[1],newwords)[0]
                    splitted[i] = nw[0].encode("utf8")
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
