import re

from habanero import Crossref
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTPage, LTChar, LTAnno, LTTextBox, LTTextLine

test_doi = {'status': 'ok', 'message-type': 'work', 'message-version': '1.0.0', 'message': {'indexed': {'date-parts': [[2020, 3, 31]], 'date-time': '2020-03-31T09:53:48Z', 'timestamp': 1585648428455}, 'reference-count': 0, 'publisher': 'Springer Science and Business Media LLC', 'issue': '1-2', 'license': [{'URL': 'http://www.springer.com/tdm', 'start': {'date-parts': [[2001, 7, 1]], 'date-time': '2001-07-01T00:00:00Z', 'timestamp': 993945600000}, 'delay-in-days': 0, 'content-version': 'tdm'}], 'content-domain': {'domain': [], 'crossmark-restriction': False}, 'short-container-title': ['Applied Microbiology and Biotechnology'], 'published-print': {'date-parts': [[2001, 7, 1]]}, 'DOI': '10.1007/s002530100652', 'type': 'journal-article', 'created': {'date-parts': [[2003, 2, 13]], 'date-time': '2003-02-13T02:43:30Z', 'timestamp': 1045104210000}, 'page': '261-264', 'source': 'Crossref', 'is-referenced-by-count': 14, 'title': ['A simple mediatorless amperometric method using the cyanobacterium Synechococcus leopoliensis for the detection of phytotoxic pollutants'], 'prefix': '10.1007', 'volume': '56', 'author': [{'given': 'L.', 'family': 'Croisetière', 'sequence': 'first', 'affiliation': []}, {'given': 'R.', 'family': 'Rouillon', 'sequence': 'additional', 'affiliation': []}, {'given': 'R.', 'family': 'Carpentier', 'sequence': 'additional', 'affiliation': []}], 'member': '297', 'container-title': ['Applied Microbiology and Biotechnology'], 'original-title': [], 'link': [{'URL': 'http://link.springer.com/content/pdf/10.1007/s002530100652.pdf', 'content-type': 'application/pdf', 'content-version': 'vor', 'intended-application': 'text-mining'}, {'URL': 'http://link.springer.com/article/10.1007/s002530100652/fulltext.html', 'content-type': 'text/html', 'content-version': 'vor', 'intended-application': 'text-mining'}, {'URL': 'http://link.springer.com/content/pdf/10.1007/s002530100652', 'content-type': 'unspecified', 'content-version': 'vor', 'intended-application': 'similarity-checking'}], 'deposited': {'date-parts': [[2019, 5, 24]], 'date-time': '2019-05-24T15:33:31Z', 'timestamp': 1558712011000}, 'score': 1.0, 'subtitle': [], 'short-title': [], 'issued': {'date-parts': [[2001, 7, 1]]}, 'references-count': 0, 'journal-issue': {'published-print': {'date-parts': [[2001, 7, 1]]}, 'issue': '1-2'}, 'alternative-id': ['BWEKP7LYNG3DLR1X'], 'URL': 'http://dx.doi.org/10.1007/s002530100652', 'relation': {}, 'ISSN': ['0175-7598', '1432-0614'], 'issn-type': [{'value': '0175-7598', 'type': 'print'}, {'value': '1432-0614', 'type': 'electronic'}]}}


class PDFArticlePageProcessor(PDFPageAggregator):
    def __init__(self, rsrcmgr, pageno=1, laparams: LAParams = None):
        PDFPageAggregator.__init__(self, rsrcmgr, pageno=pageno, laparams=laparams)
        self.rows = []
        self.page_number = 0
        self.doi = None
        self.cr = Crossref(mailto='pnpolcher@gmail.com')

    def get_doi_info(self, doi: str):
        #res = self.cr.works(ids=[doi])
        #return res
        return test_doi

    @staticmethod
    def _match_issn(s: str):
        return re.match('^[0-9]{4}-[0-9]{3}[0-9xX]$', s.strip())

    def _is_issn(self, s: str):
        # https://en.wikipedia.org/wiki/International_Standard_Serial_Number
        pass

    @staticmethod
    def _match_doi(s: str):
        # https://stackoverflow.com/questions/27910/finding-a-doi-in-a-document-or-page
        return re.match('\\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>])\\S)+)\\b', s.strip())

    def _get_doi(self, s: str):
        # Prepare string
        s0 = s.lower()
        # Check if the string DOI is contained in the string
        m = re.search('doi', s0)
        if m is not None:
            # There are chances that this is a DOI. Remove everything before the DOI string, and check the first
            # part after the DOI string.
            s1 = s0[m.start():].replace('doi:', '').replace('doi', '').strip()
            # The DOI seems split in one or more parts. Make sure the first part looks DOI-like.
            m = re.match('^(10[.][0-9]{4,})(?:[.][0-9]+)*', s1)
            if m is not None:
                doi_string = ''
                parts = s1.split()
                for part in parts:
                    doi_string += part
                    m = self._match_doi(doi_string)
                    if m is not None:
                        doi_info = self.get_doi_info(doi_string)
                        return doi_string, DOIData(doi_info)
            return None, None
        else:
#        parts = s.lower().replace('doi:', '').split()
            parts = s0.split()
            for part in parts:
                m = self._match_doi(part.strip())
                if m is not None:
                    doi_info = self.get_doi_info(part)
                    return part, DOIData(doi_info)
            return None, None

    def receive_layout(self, ltpage):
        def render(item, page_number):
            if isinstance(item, LTPage) or isinstance(item, LTTextBox):
                for child in item:
                    render(child, page_number)
            elif isinstance(item, LTTextLine):
                child_str = ''
                for child in item:
                    if isinstance(child, (LTChar, LTAnno)):
                        child_str += child.get_text()
                child_str = ' '.join(child_str.split()).strip()
                if child_str:
                    row = (page_number,
                           item.bbox[0], item.bbox[1], item.bbox[2], item.bbox[3],
                           child_str)
                    if self.doi is None:
                        (self.doi, self.doi_info) = self._get_doi(child_str)
                    self.rows.append(row)
                for child in item:
                    render(child, page_number)
            return

        render(ltpage, self.page_number)
        self.page_number += 1
        self.rows = sorted(self.rows, key = lambda x: (x[0], -x[2]))
        self.result = ltpage
