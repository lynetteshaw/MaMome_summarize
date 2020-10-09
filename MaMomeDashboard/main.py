# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import streamlit as st
import os
import csv

noart = [""]
articles = tuple(sorted(os.listdir("../MaMomePDFs")))

st.title("MaMome Summaries Dashboard")
article = st.selectbox("Article", articles)

bert_type = st.sidebar.selectbox("BERT used", ("General", "MSR PubMed"))
sum_length = st.sidebar.selectbox("Summary Length", ("Default", "Terse","Verbose"))
sum_type = st.sidebar.selectbox("Summary Source", ("Targeted", "Full"))
st.sidebar.markdown("---")
show_raw = st.sidebar.checkbox("Show Raw Text")


if sum_length == "Default":
    if sum_type == "Targeted":
        suffix = "_targ_prop"
    else:
        suffix = "_full_prop"
elif sum_length == "Terse":
    if sum_type == "Targeted":
        suffix = "_targ_terse"
    else:
        suffix = "_full_terse"
else:
    if sum_type == "Targeted":
        suffix = "_targ_verb"
    else:
        suffix = "_full_verb"



summary_name = article[:-4] + suffix + ".txt"

if bert_type == "General":
    with open("Summary_BL/" + summary_name, "r") as f:
        summary = f.read()
else:
    with open("Summary_PM/" + summary_name, "r") as f:
        summary = f.read()

st.markdown("## Summary")
st.write(summary)



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


st.sidebar.markdown("---")
st.sidebar.markdown("### Bacteria Terms Appearing in Summary")
st.sidebar.write(commterms)



if show_raw:
    raw_name = article[:-4] + ".txt"
    st.markdown("# Raw Text")
    with open("../docproc/TxtData/" + raw_name) as f:
        raw = f.read()
        rawterms = set(raw.split(" "))
        rawcommterms = common_member(bacwords, rawterms)
    st.write(raw)
    st.sidebar.write(" ")
    st.sidebar.write("### Bacteria Terms Appearing in Raw Text")
    st.sidebar.write(rawcommterms)