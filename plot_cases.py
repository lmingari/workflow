import configparser
import subprocess
import os

config = configparser.ConfigParser(inline_comment_prefixes="#")
config.read('config.inp')

for block in config.sections():
    basepath  = config[block]['basepath']
    path_runs = os.path.join(basepath,'RUNS',block)
    path_post = os.path.join(path_runs,'POST')

    run_ok = False
    if os.path.exists(path_runs):
        run_ok   = config[block].getboolean('run')
        fname    = os.path.join(path_post,'plot-all.sh')

    if run_ok:
        print(f"Plotting for: {block}")
        subprocess.call(fname)
    else:
        print(f"Skipping {block}...")
