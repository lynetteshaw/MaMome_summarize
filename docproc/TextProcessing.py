
import os
import csv
import re



def getkeywords(baclist = "/content/drive/My Drive/MaMomeDashboard/bacteria_list.csv",
                nutrilist = "/content/drive/My Drive/MaMomeDashboard/nutrient_list.csv"):

    with open(baclist) as f:
        reader = csv.reader(f)
        blist = list(reader)

    bacteria = []

    for bac in blist[2:]:
        if len(bac) > 0:
             bacteria += bac[0].split(' ')

    bacwords = [word.lower() for word in bacteria if (word.isalpha() and len(word) > 1) and (word != 'strain')]

    with open(nutrilist) as f:
        reader = csv.reader(f)
        nlist = list(reader)

    nutriwords = [word[0].lower() for word in nlist]

    keywords = nutriwords + bacwords

    return keywords



def refclean(doc):
    citepat1 = re.compile('(1\.\s [A-Z].*\n.*\n)')
    citepat2 = re.compile('(\nREFERENCES\n)', re.IGNORECASE)

    temp = citepat2.split(doc, maxsplit=1)

    if len(temp) > 1:
        cleaned = temp[0]

    else:
        temp2 = citepat1.split(doc)

        if len(temp2) > 1:
            if len(temp2) > 2:
                cleaned = ' '.join(temp[:-1])
            else:
                cleaned = temp2[0]
        else:
            cleaned = temp2

    return cleaned


# fxn to remove urls


def clean(doc):
    cleaned = re.sub(r"http\S+", "", doc)
    cleaned = re.sub(r"www\S+", "", doc, flags=re.IGNORECASE)
    cleaned = re.sub(r"DOI:\S+", "", doc, flags=re.IGNORECASE)
    cleaned = re.sub(r"\((fig|figure|table)\..*\)", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"(\([0-9]*[0-9],*.*\).?)", "", cleaned)
    cleaned = re.sub(r"(\[[0-9]*[0-9],*.*\].?)", "", cleaned)

    return cleaned


# fxn to break into paragraphs

def paras(doc):
    paras = doc.split('\n\n')
    # paras = doc.split('.\n\n')
    paras = [para for para in paras if (len(para) > 30)]

    topara = []

    for para in paras:
        topara.append(re.sub(r'\n\n', " ", para))

    return topara


# fxn to only keep paragraphs w/terms appearing in bacteria list

def keywordfilter(paras, keywords):
    tokeep = []

    for para in paras:
        temp = para.lower()
        if any(check in temp.split(' ') for check in keywords):
            tokeep.append(para)

    return tokeep


# fxn to clean texts for full preprocessing option and write to file
# Accepts: string with path to directory with converted pdfs
# Returns: writes cleaned texts to .txt files to directory for summarization (full preprocessing option)
def full_clean(converted_dir = "/content/drive/My Drive/MaMomeDashboard/MaMome_Summarize/docproc/Converted/",
               cleaned_dir = "/content/drive/My Drive/MaMomeDashboard/MaMome_Summarize/docproc/TxtData/"):
    txtfiles = os.listdir(converted_dir)

    for txtfile in txtfiles:

        with open(converted_dir + '/' + txtfile, "r") as f:
            doc = f.read()

        clean1 = refclean(str(doc))
        clean2 = clean(str(clean1))

        path = cleaned_dir + txtfile[:-4] + ".txt"

        if len(clean2) > 20:
            with open(path, "w") as f:
                f.write(clean2)
        else:
            with open(path, "w") as f:
                f.write("0_PARAGRAPHS\n\n" + "UNABLE TO PROCESS FILE: " + txtfile[:-4])


# fxn to clean texts for targeted preprocessing option and write to file
# Accepts: string with path to directory with converted pdfs
# Returns: writes cleaned texts to .txt files to directory for summarization (targeted preprocessing option)

def targ_clean(keywords,
               converted_dir = "/content/drive/My Drive/MaMomeDashboard/MaMome_Summarize/docproc/Converted/",
               cleaned_dir = "/content/drive/My Drive/MaMomeDashboard/MaMome_Summarize/docproc/Filtered/"):

    txtfiles = os.listdir(converted_dir)

    for txtfile in txtfiles:

        with open(converted_dir + '/' + txtfile, "r") as f:
            doc = f.read()

        clean1 = refclean(str(doc))
        clean2 = clean(str(clean1))

        topara = paras(clean2)

        filtered = keywordfilter(topara, keywords)

        paranum = str(len(filtered))

        filtdoc = paranum + "_PARAGRAPHS\n\n" + ".\n\n".join(filtered)

        path = cleaned_dir + txtfile[:-4] + "_FILTERED.txt"

        if len(filtdoc) > 20:
            with open(path, "w") as f:
                f.write(filtdoc)
        else:
            with open(path, "w") as f:
                f.write("0_PARAGRAPHS\n\n" + "UNABLE TO PROCESS FILE: " + txtfile[:-4])
