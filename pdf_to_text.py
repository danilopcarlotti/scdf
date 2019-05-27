from tikapp import TikaApp
import subprocess, os

class pdf_to_text():
    """Converts pdf to text with pdfminer"""
    def __init__(self):
        pass

    def convert_Tika(self,fname):
        tika_client = TikaApp(file_jar=os.getcwd()+'/tika-app-1.20.jar')
        return tika_client.extract_only_content(fname)

if __name__ == '__main__':
    pass