from pdfminer.layout import LAParams, LTPage, LTChar, LTAnno, LTTextBox, LTTextLine
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

from journalparser.pageprocessors import PDFArticlePageProcessor


class JournalPDFParser(object):
    def __init__(self):
        pass

    def parse(self, pdf_filename: str):
        with open(pdf_filename, 'rb') as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            laparams = LAParams()
            device = PDFArticlePageProcessor(rsrcmgr, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)
                device.get_result()

        return device