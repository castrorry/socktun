import getopt
import sys

# Load opt definitions
def load_argv():
    args_object = dict()
    optlist, _ = getopt.getopt(sys.argv[1:], 'hc:', ['config=', 'help'])
    for key, value in optlist:
        args_object[key] = value
    return args_object

argv = load_argv()

def get_config_path():
    if '-c' in argv:
        return argv['-c']
    elif '--config' in argv:
        return argv['--config']
    else:
        return None

from socktun import load_config
Config = load_config.Config(get_config_path())

from socktun.handler import Handler
from socktun.proxy import Proxy
