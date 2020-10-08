# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import streamlit as st
import os

noart = [""]
articles = tuple(os.listdir("../MaMomePDFs"))

st.title("MaMome Summaries Dashboard")
article = st.selectbox("Article", articles)

sum_length = st.sidebar.selectbox("Summary Length", ("Default", "Terse","Verbose"))
sum_type = st.sidebar.selectbox("Summary Source", ("Targeted", "Full"))
st.sidebar.markdown("---")
show_raw = st.sidebar.checkbox("Show Raw Text")

if sum_length == "Default":
    if sum_type == "Targeted":
        suffix = "_tar_prop"
    else:
        suffix = "_full_prop"
elif sum_length == "Terse":
    if sum_type == "Targeted":
        suffix = "_tar_terse"
    else:
        suffix = "_full_terse"
else:
    if sum_type == "Targeted":
        suffix = "_tar_verb"
    else:
        suffix = "_full_verb"

summary_name = article[:-4] + suffix + ".txt"

with open("../docproc/Summary/" + summary_name, "r") as f:
    summary = f.read()


st.write(summary)

if show_raw:
    raw_name = article[:-4] + ".txt"
    with open("../docproc/TxtData/" + raw_name) as f:
        raw = f.read()
    st.write(raw)