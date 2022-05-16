from PyPDF2 import PdfFileReader

with open('CT1-All.pdf', 'rb') as f:
    reader = PdfFileReader(f)
    contents = reader.getPage(0).extractText().split('\n')
    pass

