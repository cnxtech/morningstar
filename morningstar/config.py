import os

import yaml

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = "config.yml"

config = None
for loc in os.curdir, os.path.expanduser("~"), os.environ.get("MORNINGSTAR_CONFIG"):
    try:
        with open(os.path.join(loc, CONFIG_FILE)) as source:
            config = yaml.safe_load(source)
    except IOError:
        pass
    except TypeError:
        pass

if config is None:
    raise IOError("{} not found.".format(CONFIG_FILE))
