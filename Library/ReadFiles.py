from urllib.request import urlopen
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from io import open
from zipfile import ZipFile
from io import BytesIO
from bs4 import BeautifulSoup
#______________________________________________________________________________#
def read_pdf(pdfFile):
    """
    Doesn't have a perfect output for pdfs with images.

    Parameter:
        pdfFile: string url or urlopen object of the pdf pdfFile.
    Returns:
        content: String with the text content
    """
    if (isinstance(pdfFile,str)):
        pdfFile = urlopen(pdfFile)

    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    process_pdf(rsrcmgr, device, pdfFile)
    device.close()
    content = retstr.getvalue()
    retstr.close()
    pdfFile.close()
    return content
#______________________________________________________________________________#

def read_word (wordFile):
    """
    Doesn't have a perfect output for docs with images.

    Parameter:
        wordFile: string url or urlopen object of the word File.
    Returns:
        content: String with the text content
    """
    if (isinstance(wordFile,str)):
        wordFile = urlopen(wordFile)

    wordFile = wordFile.read()
    wordFile = BytesIO(wordFile)
    document = ZipFile(wordFile)
    xml_content = document.read('word/document.xml')
    wordObj = BeautifulSoup(xml_content.decode('utf-8'), 'xml')
    textStrings = wordObj.find_all('w:t')
    text = ''

    for textElem in textStrings:
        text += textElem.text

    return text

print(read_word('http://pythonscraping.com/pages/AWordDocument.docx'))



#pdfFile = 'http://pythonscraping.com/pages/warandpeace/chapter1.pdf'
#outputString = readPDF(pdfFile)
#print(outputString)


#text = pdfminer.high_level.extract_text(r'\Users\50687\Dropbox\Libreria\University\Archived\Intro to computer science 6.001\Slides\Functions.pdf')
#print(repr(text))
