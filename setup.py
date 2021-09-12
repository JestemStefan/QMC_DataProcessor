from distutils.core import setup
import sys 
import py2exe #lgtm [py/unused-import]


MAIN_SCRIPT_DIR = "qmc_dataprocessor\\qmc_dataprocessor.py"
main_folder = MAIN_SCRIPT_DIR.rsplit("\\",1)[0]
sys.path.append(main_folder)

setup(options = {"py2exe" : {"bundle_files": 1, "compressed" : True}},
    windows = [{"script" : "qmc_dataprocessor\\qmc_dataprocessor.py"}],
    zipfile = None)