from io import StringIO

from pdfminer.converter import HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

class PDFToHTMLConverter():
    def __init__(self):
        self.output_string = StringIO()

    def clear(self):
        self.output_string = StringIO()

    def convert(self, pdf_file_location, html_file_location):
        with open(pdf_file_location, 'rb') as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            device = HTMLConverter(rsrcmgr, self.output_string,
                                   laparams=LAParams(), codec=None)
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)


        with open (html_file_location, "w", encoding='utf-8') as file:
            file.write(self.output_string.getvalue())
