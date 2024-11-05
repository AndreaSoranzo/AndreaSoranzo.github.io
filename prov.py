import sys as sys
import shutil as cmd
import pathlib as l
import subprocess
import os
import logging


TEMPLATE = '<li><a href="{{link}}" target="_blank">{{name}}</a> <span class="tag-versione">{{versione}}</span> </li>'

def main() :
    logging.basicConfig(level=os.getenv('LOGLEVEL', 'INFO'))

    cmd.rmtree('_site', ignore_errors=True)
    cmd.copytree('website', '_site', symlinks=False)

    html = l.Path('_site/index.html').read_text()
    pdfs = []
    command =["pdflatex"]
    for item in os.listdir("letex"):
        subprocess.call(command + ['letex/'+item])
        for item in os.listdir("."):
            if item.endswith(".log") or item.endswith(".aux") or item.endswith(".out"):
                os.remove(os.path.join(".", item))
            elif item.endswith(".pdf"):
                cmd.move(item,"_site")
                pdfs.append(item.replace(".tex",".pdf"))



    
    html = html.replace('{{HERE}}',"\n".join(MakeLink(file) for file in pdfs)) 


    l.Path('_site/index.html').write_text(html)

def MakeLink(file:str):
    return TEMPLATE.replace("{{link}}",file).replace("{{name}}",file.removesuffix(".pdf"))

if __name__ == "__main__":
    main()

