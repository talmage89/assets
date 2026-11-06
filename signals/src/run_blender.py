"""Serial child runner recording kernel peak RSS without retaining its output.

The GPU lock descriptor remains inherited until Blender exits. This family
uses fresh render processes per seed to release caches between towns.
"""
import argparse,json,os,resource,subprocess,time
from pathlib import Path

def main():
 p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True);p.add_argument('command',nargs=argparse.REMAINDER);a=p.parse_args()
 command=a.command[1:] if a.command and a.command[0]=='--' else a.command
 if not command:raise SystemExit('Missing child command')
 start=time.monotonic();held=(9,) if os.environ.get('ASSETS_GPU_HELD')=='1' else ()
 result=subprocess.run(command,pass_fds=held)
 usage=resource.getrusage(resource.RUSAGE_CHILDREN)
 report=dict(command=command,exit_code=result.returncode,elapsed_seconds=time.monotonic()-start,peak_rss_kib=usage.ru_maxrss,scope='Kernel maximum resident set for this serial child on Linux; output is inherited, not buffered in Python')
 a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(report,indent=2))
 print('MEMORY',round(usage.ru_maxrss/1024,1),'MiB peak RSS;',round(report['elapsed_seconds'],1),'seconds;',a.report,flush=True)
 raise SystemExit(result.returncode)
if __name__=='__main__':main()
