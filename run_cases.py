import configparser
from string import Template
from datetime import datetime
import subprocess
import os

config = configparser.ConfigParser(inline_comment_prefixes="#")
config.read('config.inp')

today = datetime.utcnow()

data = {
    'YEAR':  today.year,
    'MONTH': today.month,
    'DAY':   today.day,
}

data = {
    'YEAR':  2017,
    'MONTH': 6,
    'DAY':   22,
}

for block in config.sections():
    basepath  = config[block]['basepath']
    path_runs = os.path.join(basepath,'RUNS',block)
    fnameJOB  = os.path.join(path_runs,'FALL3D-job.cmd')


    run_ok = False
    if os.path.exists(path_runs):
        run_ok   = config[block].getboolean('run')
        fnameIN  = os.path.join(path_runs,'template.inp')
        fnameOUT = os.path.join(path_runs,f'{block}.inp')
        with open(fnameIN, 'r') as f1, open(fnameOUT,'w') as f2:
            src = Template(f1.read())
            result = src.safe_substitute(data)
            f2.write(result)

    if run_ok:
        print(f"Starting job for: {block}")
        subprocess.call(["qsub", fnameJOB])
    else:
        print(f"Skipping {block}...")
