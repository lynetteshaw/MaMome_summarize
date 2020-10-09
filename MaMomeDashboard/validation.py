import os
import csv
import pandas as pd

def raw_metrics(doc_name):

    raw_name = doc_name[:-4] + ".txt"

    with open("../docproc/TxtData/" + raw_name) as f:
        raw = f.read()

    rawterms = set(raw.lower.split(" "))
    rawcommterms = len(common_member(bacwords, rawterms))

    rawsents = set(raw.split('.'))
    raw_relsents = rel_sents(rawsents, bacwords)

    raw_tup = (rawcomterms, raw_relsents)

    return raw_tup

def sum_metrics(doc_name, bert_type, raw_tup):

    suffices = ["_targ_verb", "_full_verb"]

    for suffix in suffices:
        summary_name = doc_name[:-4] + suffix + ".txt"

        if bert_type == "General":
            with open("Summary_BL/" + summary_name, "r") as f:
                summary = f.read()
        else:
            with open("Summary_PM/" + summary_name, "r") as f:
                summary = f.read()

        sumterms = set(summary.lower.split(" "))
        sumcomterms = len(common_member(bacwords, sumterms))

        sumsents = set(summary.split())
        sum_relsents = rel_sents(sumsents, bacwords)

        prop_terms = sumcomterms / raw_tup[0]
        prop_sents = sum_relsents / raw_tup[1]

        met_list = [prop_terms, prop_sents]

        return met_list


def common_member(a, b):
    a_set = set(a)
    b_set = set(b)

    commterms = ""

    if (a_set & b_set):
        commterms = list(a_set & b_set)

    return commterms


def rel_sents(sents, bacwords = bacwords):

    counter = 0

    for sent in sents:
        temp = sent.lower()
        if any(check in temp.split(' ') for check in bacwords):
            counter += 1

    return counter



with open('../docproc/bac_list.csv') as f:
    reader = csv.reader(f)
    blist = list(reader)

bacteria = []

for bac in blist[2:]:
    if len(bac) > 0:
         bacteria += bac[0].split(' ')

bacwords = [word.lower() for word in bacteria if (word.isalpha() and len(word) > 1)]

articles = tuple(sorted(os.listdir("../MaMomePDFs")))

met_dict = {}

for article in articles:
    raw_tup = raw_metrics(article)
    art_mets = sum_metrics(article, "General", raw_tup)
    key = article[:-4]
    met_dict[key] = ["General"].append(art_mets)

for article in articles:
    raw_tup = raw_metrics(article)
    art_mets = sum_metrics(article, "PubMed", raw_tup)
    key = article[:-4]
    met_dict[key] = ["PubMed"].append(art_mets)

met_df = pd.DataFrame.from_dict(met_dict, orient='index')

