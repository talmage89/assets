"""One GPU lease for module, scale and both photo-inspection sets.

Each heavy scene starts in a fresh Blender process. The outer kit wrapper
owns FD 9; every serial descendant inherits it until all rendering is done.
Photo composition and contact-sheet assembly run after this process exits.
"""
import argparse,os,shlex,subprocess,sys
from pathlib import Path

def main():
    p=argparse.ArgumentParser();p.add_argument('--blender',default='blender -t 2')
    p.add_argument('--width',type=int,default=1400);p.add_argument('--samples',type=int,default=32);a=p.parse_args()
    os.fstat(9)
    def run(command):subprocess.run(command,check=True,pass_fds=(9,))
    bp=shlex.split(a.blender)+['-b','--factory-startup','--python-exit-code','1','--python']
    run(bp+['src/module_sheet.py','--','--out','renders/lookdev','--width','2000','--samples',str(a.samples)])
    run(bp+['src/render.py','--','--scale','--out','renders/lookdev','--width',str(a.width),'--samples',str(a.samples)])
    for folder,source in [('look-matches',False),('source-matches',True)]:
        command=[sys.executable,'src/render_batch.py','--blender',a.blender,'--python','src/render.py','--',
                 '--camera-file','build/cameras.json','--out','renders/'+folder,
                 '--width',str(a.width),'--samples',str(a.samples)]
        if source:command.append('--source-fields')
        run(command)
    print('PRESENTATION RENDER SET COMPLETE',flush=True)
if __name__=='__main__':main()
