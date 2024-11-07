import sys as sys
import shutil as cmd
import pathlib as path
import subprocess
import os
import logging
import concurrent.futures

import time


TEMPLATE = '<li><a href="{{link}}" target="_blank">{{name}}</a> <span class="tag-versione">{{ver}}</span> </li>'

class PDF:
    def __init__(self,name,ver):
        self.name = name
        self.ver = ver
    def GetName(self,WExt=False):
        return self.name
    def GetVer(self):
        return self.ver
    def __lt__(self, other):
        if self.name < other.name:
            return True
        else:
            return False



def main(UseThread:bool=False):
    start_time = time.time()
    logging.basicConfig(level=os.getenv('LOGLEVEL', 'INFO'))
    init_path = os.getcwd()

    logging.info(f'Creating the workspace')
    cmd.rmtree('_site', ignore_errors=True)
    cmd.copytree('website', '_site', symlinks=False)

    html = path.Path('_site/index.html').read_text()

    pdfs = {
        "candidatura" : [],
        "generali" : [],
        "VI" : [],
        "VE" : []
    }
    command = ["pdflatex"]

    if UseThread:

        with concurrent.futures.ThreadPoolExecutor(60) as pool:
            for type in os.listdir(path.Path("tex")):
                pool.submit(BuildTypePDF,init_path,pdfs,command,type)
    else:
        BuildAllPDF(init_path, pdfs, command) 
    
    UpdateHtml(html,pdfs)
    print("--- %s seconds ---" % (time.time() - start_time))


def BuildAllPDF(init_path:str, pdfs:dict[str, list], command:list[str]):
    logging.info(f'Building tex files')
    for type in os.listdir(path.Path("tex")):
        BuildTypePDF(init_path, pdfs, command, type)

def BuildTypePDF(init_path:str, pdfs:dict[str, list], command:list[str], type:str):
    for doc in os.listdir(path.Path("tex/"+type)):
        ver = GetDocVersion(path.Path('tex/'+type+"/"+doc+"/titlepage.tex"))
        logging.debug(f"Current dir {os.getcwd()}")
        logging.debug(f"Changing dir to {path.Path('tex/'+type+'/'+doc)}")
        os.chdir(path.Path("tex/"+type+"/"+doc))
        result = subprocess.run(command + ["-jobname="+doc] + [path.Path("main.tex")],stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        try:
            logging.info(command + ["-jobname="+doc] + [path.Path("main.tex")])
            result.check_returncode()
        except Exception as e:
            logging.error(f"Compiling {doc} failed with stderr: \n{result.stderr}")
            return
        cmd.move(doc+".pdf",path.Path("../../../_site/"+doc+".pdf"))
        pdfs[type].append(PDF(doc+'.pdf',ver))
        logging.debug(f"Current dir to {os.getcwd()}")
        logging.debug(f"Changing dir to {path.Path(init_path)}")
        os.chdir(init_path)

def UpdateHtml(html:str,pdfs:dict[str, list]):
    logging.info(f'Updating the HTML')
    for type in pdfs:
        pdfs[type].sort()
        html = html.replace("{{"+ type +"}}","\n".join(MakeLink(pdf) for pdf in pdfs[type]))
    path.Path('_site/index.html').write_text(html)

def GetDocVersion(path:str):
    ver = ""
    with open(path,'r') as doc:
        for line in doc:
            if "Versione" in line:
                ver = line.split()[-1][:5]
    return ver if ver != "" else " -.-.-" 
    
def MakeLink(pdf:PDF):
    return TEMPLATE.replace("{{link}}",pdf.GetName(True)).replace("{{name}}",pdf.GetName()).replace("{{ver}}",pdf.GetVer())

if __name__ == "__main__":
    main()

