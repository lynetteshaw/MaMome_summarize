from transformers import *
from summarizer import Summarizer


def sumSets(preproc, sumtype, summed, full_dir, targ_dir):

    if preproc = 'full':
        suffix = '_full_'
        textdir = full_dir
        docs = os.listdir(textdir)
    elif preproc = 'targeted':
        suffix = '_targ_'
        textdir = targ_dir
        docs = os.listdir(textdir)
    else:
        raise ValueError("Must specify preprocessing type. Expected one of: %s" % ['targeted','full'])

    if sumtype = 'PubMed':
        sumdir = '/Summary_PM/'
    elif sumtype = 'General':
        sumdir = '/Summary_BL/'
    else:
        raise ValueError("Must specify summary type. Expected one of: %s" % ['PubMed', 'General'])

    # Iterate through processed .txt files and generate summaries and write to file
    for doc in docs:

        with open(textdir + '/' + doc, "r") as in_f:
            body = in_f.read()

        temp = body.split("_PARAGRAPHS", maxsplit=1)

        paralength = (int(temp[0]) // 3)

        if paralength < 4:
            sumsents = 4
        elif paralength > 10:
            sumsents = 10
        else:
            sumsents = paralength

        # Default length (~ 1 sentence for every 3 paragraphs w/min 4 and max 10

        summary = ''.join(summed(body, num_sentences=sumsents)

        path = "/content/drive/My Drive/MaMomeDashboard" + sumdir +  doc[:-13] + suffix + "prop.txt"

        with open(path, "w") as out_f:
            out_f.write(summary)

        # Terse summary (4 sentences)

        summary = ''.join(summed(body, num_sentences=4))
        path = "/content/drive/My Drive/MaMomeDashboard" + sumdir + doc[:-13] + suffix + "terse.txt"

        with open(path, "w") as out_f:
            out_f.write(summary)

        # Verbose summary (15 sentences)

        summary = ''.join(summed(temp[1], num_sentences=15))

        path = "/content/drive/My Drive/MaMomeDashboard"+ sumdir + doc[:-13] + suffix + "verb.txt"

        with open(path, "w") as out_f:
            out_f.write(summary)


def PMSummarize(
    full_dir = "/content/drive/My Drive/MaMomeDashboard/MaMome_Summarize/docproc/TxtData/",/
    targ_dir = "/content/drive/My Drive/MaMomeDashboard/MaMome_Summarize/docproc/Filtered/"):

    custom_config = BertConfig.from_pretrained('microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract-fulltext')
    custom_config.output_hidden_states=True

    tokenizer = BertTokenizer.from_pretrained('microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract-fulltext')

    model = BertModel.from_pretrained('microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract-fulltext', config=custom_config)

    summed = Summarizer(custom_model= model, custom_tokenizer=tokenizer)

    for preproc in ['targeted', 'full']:
        sumSets(preproc, 'PubMed', summed, full_dir, targ_dir)

def BLSummarize(
    full_dir = "/content/drive/My Drive/MaMomeDashboard/MaMome_Summarize/docproc/TxtData/", /
    targ_dir = "/content/drive/My Drive/MaMomeDashboard/MaMome_Summarize/docproc/Filtered/"):

    custom_config = BertConfig.from_pretrained('bert-large-uncased')
    custom_config.output_hidden_states = True

    tokenizer = BertTokenizer.from_pretrained('bert-large-uncased')

    model = BertModel.from_pretrained('bert-large-uncased', config=custom_config)

    summed = Summarizer(custom_model= model, custom_tokenizer=tokenizer)

    for preproc in ['targeted', 'full']:
        sumSets(preproc, 'General', summed, full_dir, targ_dir)