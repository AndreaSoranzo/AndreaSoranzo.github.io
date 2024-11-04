import sys as sys
import shutil as cmd
import pathlib as l
import subprocess
import os

from pdflatex import PDFLaTeX

TEMPLATE = '<li><a href="{{link}}" target="_blank">{{name}}</a></li>'

def main() :
    cmd.rmtree('_site', ignore_errors=True)
    cmd.copytree('website', '_site', symlinks=False)

    html = l.Path('_site/index.html').read_text()
    pdfs = []
    for item in os.listdir("letex"):
        pdfl = PDFLaTeX.from_texfile('letex/'+item)
        pdfl.set_output_directory("_site")
        pdf, _ , completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=False)  
        print('letex/'+item)
        if completed_process.returncode == 0:
            pdfs.append(item.replace(".tex",".pdf"))



    
    html = html.replace('{{HERE}}',"\n".join(MakeLink(file) for file in pdfs)) 


    l.Path('_site/index.html').write_text(html)

def MakeLink(file:str):
    return TEMPLATE.replace("{{link}}",file).replace("{{name}}",file.removesuffix(".pdf"))

if __name__ == "__main__":
    main()

