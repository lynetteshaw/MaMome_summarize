import io
import os
import pdfminer

from pdfminer.pdfparser import PDFParser
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfinterp import resolve1

# Generate list of curated PDFs
os.chdir("../MaMomePDFs")
pdfs = os.listdir(".")


# Fxn to extract text from .pdfs
# Accepts individual .pdf filename for argument

def pdfextract(pdf):

    with open(pdf, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)

        # print file name and raise error for unextractable files
        if not doc.is_extractable:
            print(pdf)
            raise PDFTextExtractionNotAllowed

        output_string = io.StringIO()
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams(detect_vertical=True))
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # Drop first page w/abstract and header info and some references if not a very short .pdf

        if (resolve1(doc.catalog['Pages']) != None):
            doclength = resolve1(doc.catalog['Pages'])['Count']

            for pageNumber, page in enumerate(PDFPage.get_pages(in_file)):
                if (pageNumber > 0) and (pageNumber < doclength) and (doclength > 2):
                    interpreter.process_page(page)

        else:

            for pageNumber, page in enumerate(PDFPage.get_pages(in_file)):
                interpreter.process_page(page)

        return output_string.getvalue()



# Function to write extracted text from .pdfs to .txt files in docproc directory for further processing
# Accepts string with path to folder containing .pdfs to be converted
# 'MaMomeDashboard/MaMomePDFs' used by default

def pdftotxt(pdfdir = "/content/drive/My Drive/MaMomeDashboard/MaMomePDFs"):

    os.chdir(pdfdir)
    pdfs = os.listdir(".")

    for pdf in pdfs:
        text = pdfextract(pdf)

        file = "/content/drive/My Drive/MaMomeDashboard/Converted/" + pdf[:-4] + ".txt"

        with open(file, "w") as f:
            f.write(text)
