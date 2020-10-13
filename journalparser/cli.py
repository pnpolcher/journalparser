import os

from journalparser.parsers import JournalPDFParser

PDF_BASE_DIR = 'd:\\docs\\pdf_clasificar\\papers'
parser = JournalPDFParser()


count_doi = 0
error_count = 0
#dir_contents = os.listdir(PDF_BASE_DIR)
dir_contents = ['JCE1964p0202.pdf']
for filename in dir_contents:
    pdf_filename = os.path.join(PDF_BASE_DIR, filename)
    if os.path.getsize(pdf_filename) > 16777216:
        continue
    try:
        device = parser.parse(pdf_filename)
        print(pdf_filename, device.doi is not None)
        if device.doi is not None:
            count_doi += 1
        else:
            # pass
            print(device.rows)
    except Exception as e:
        print (e)
        error_count += 1
        print(f'Error processing: {pdf_filename}')
#        pass

print (count_doi, error_count, len(dir_contents))
