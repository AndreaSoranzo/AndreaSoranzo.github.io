import sys as sys
import shutil as cmd
import pathlib as l

def main() :
    cmd.rmtree('dist', ignore_errors=True)
    cmd.copytree('website', 'dist', symlinks=False)

    html = l.Path('dist/index.html').read_text()

    html = html.replace('{{HERE}}',"AAAAAAAAAAAAAAAAAAAAAAAAAAAAA") 

    l.Path('dist/index.html').write_text(html)

if __name__ == "__main__":
    main()

