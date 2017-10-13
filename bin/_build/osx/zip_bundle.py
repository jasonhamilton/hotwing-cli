import shutil
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
shutil.make_archive('hotwing-cli-win', 'zip',dir_path, 'hotwing-cli')