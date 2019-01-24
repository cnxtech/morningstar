import yaml
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(ROOT_DIR, '../config.yml')
config = yaml.safe_load(open(CONFIG_FILE))
