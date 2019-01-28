import os

import yaml

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = "config-morningstar.yml"

config = None
for loc in os.path.join(os.curdir, CONFIG_FILE), \
           os.path.expanduser("~/{}".format(CONFIG_FILE)), \
           os.path.expanduser("~/.{}".format(CONFIG_FILE)):
    try:
        with open(loc) as source:
            config = yaml.safe_load(source)
    except IOError:
        pass
    except TypeError:
        pass

if config is None:
    raise IOError("{} not found.".format(CONFIG_FILE))
