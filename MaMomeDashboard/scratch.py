import os
import csv

temps = os.listdir("../docproc/Summary/")

with open("../docproc/Summary/" + temps[0], "r") as f:
    summary = f.read()

sumterms = set(summary.split(" "))

with open('../docproc/bac_list.csv') as f:
    reader = csv.reader(f)
    blist = list(reader)

bacteria = []

for bac in blist[2:]:
    if len(bac) > 0:
         bacteria += bac[0].split(' ')

bacwords = [word for word in bacteria if (word.isalpha() and len(word) > 1)]

def common_member(a, b):
    a_set = set(a)
    b_set = set(b)

    commterms = ""

    if (a_set & b_set):
        commterms = list(a_set & b_set)

    return commterms

commterms = common_member(bacwords, sumterms)
print("\n".join(commterms))