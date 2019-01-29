import os
import logging
import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    logger.warning("{} not found.".format(CONFIG_FILE))
