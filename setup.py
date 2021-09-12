from distutils.core import setup
import py2exe #lgtm [py/unused-import]
import sys 

main_script_dir = "qmc_dataprocessor\qmc_dataprocessor.py"
main_folder = main_script_dir.rsplit("\\",1)[0]
sys.path.append(main_folder)

setup(options = {"py2exe" : {"bundle_files": 1, "compressed" : True}},
    windows = [{"script" : "qmc_dataprocessor\qmc_dataprocessor.py"}],
    zipfile = None)