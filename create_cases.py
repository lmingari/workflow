import configparser
from string import Template
import shutil
import os

os.umask(os.umask(0) & ~(0o0775))

config = configparser.ConfigParser(inline_comment_prefixes="#")
config.read('config.inp')

for block in config.sections():
    basepath  = config[block]['basepath']
    path_runs = os.path.join(basepath,'RUNS',block)
    path_post = os.path.join(path_runs,'POST')
    path_temp = os.path.join(basepath,'templates')

    if os.path.exists(path_runs):
        print(f"Skipping {block}... folder already exists")
        continue
    else:
        print(f"Creating folder: {path_runs}")
        os.makedirs(path_runs, mode = 0o775)
        os.makedirs(path_post, mode = 0o775)

    data = {}
    data['basepath']   = basepath
    data['time_start'] = config[block].getfloat('time_start')
    data['time_end']   = config[block].getfloat('time_end')
    data['lonmin']     = config[block].getfloat('lonmin')
    data['lonmax']     = config[block].getfloat('lonmax')
    data['latmin']     = config[block].getfloat('latmin')
    data['latmax']     = config[block].getfloat('latmax')
    data['lonv']       = config[block].getfloat('lonv')
    data['latv']       = config[block].getfloat('latv')
    data['hv']         = config[block].getfloat('hv')

    fnameIN  = os.path.join(path_temp,'template.inp')
    fnameOUT = os.path.join(path_runs,'template.inp')

    with open(fnameIN, 'r') as f1, open(fnameOUT,'w') as f2:
        src = Template(f1.read())
        result = src.safe_substitute(data)
        f2.write(result)

    data = {}
    data['project']  = block
    data['path_run'] = path_runs
    data['NMPIX']    = config[block].getint('NMPIX')
    data['NMPIY']    = config[block].getint('NMPIY')
    data['NMPIZ']    = config[block].getint('NMPIZ')
    data['NMPI']     = data['NMPIX']*data['NMPIY']*data['NMPIZ']

    fnameIN  = os.path.join(path_temp,'FALL3D-job.cmd')
    fnameOUT = os.path.join(path_runs,'FALL3D-job.cmd')

    with open(fnameIN, 'r') as f1, open(fnameOUT,'w') as f2:
        src = Template(f1.read())
        result = src.safe_substitute(data)
        f2.write(result)

    data = {}
    data['basepath'] = basepath
    data['resfile']  = os.path.join(path_runs,f'{block}.res.nc')

    fnameIN  = os.path.join(path_temp,'plot_colmass.py')
    fnameOUT = os.path.join(path_post,'plot_colmass.py')

    with open(fnameIN, 'r') as f1, open(fnameOUT,'w') as f2:
        src = Template(f1.read())
        result = src.safe_substitute(data)
        f2.write(result)

    fnameIN  = os.path.join(path_temp,'plot_deposit.py')
    fnameOUT = os.path.join(path_post,'plot_deposit.py')

    with open(fnameIN, 'r') as f1, open(fnameOUT,'w') as f2:
        src = Template(f1.read())
        result = src.safe_substitute(data)
        f2.write(result)

    data = {}
    data['path_post'] = path_post

    fnameIN  = os.path.join(path_temp,'plot-all.sh')
    fnameOUT = os.path.join(path_post,'plot-all.sh')

    with open(fnameIN, 'r') as f1, open(fnameOUT,'w') as f2:
        src = Template(f1.read())
        result = src.safe_substitute(data)
        f2.write(result)

    os.chmod(fnameOUT, 0o774)

    fnameIN  = os.path.join(path_temp,f'locations_{block}.csv')
    fnameOUT = os.path.join(path_post,'locations.csv')
 
    shutil.copy(fnameIN, fnameOUT)
