import os
import zipfile
import argparse
from pathlib import Path
from datetime import datetime
from tqdm import tqdm
from .paths import Paths
from .utils.decorator import avoid_dupfiles


class Zip:
    def __init__(self, source_path, zipname, taget_path='~/Desktop', compression=False):
        self.source_path = source_path
        self.target_path = Path(taget_path).expanduser().resolve()
        self.compression = compression
        self.zipname = zipname

    def which_compression(self):
        if self.compression:
            return zipfile.ZIP_DEFLATED
        else:
            return zipfile.ZIP_STORED

    @avoid_dupfiles
    def zip_name_path(self):
        return self.target_path / self.zipname

    def souce_paths(self):
        if self.source_path == '.':
            p = Paths(self.source_path, resolve=False)
        else:
            p = Paths(self.source_path)
        return p.get_files().items

    def file_n(self):
        return sum(1 for i in self.souce_paths())

    def run(self):
        with zipfile.ZipFile(self.zip_name_path(), 'w', compression=self.which_compression()) as new_zip:
            for p in tqdm(self.souce_paths(), total=self.file_n()):
                new_zip.write(p)


# command line
def cli():
    parser = argparse.ArgumentParser(description='create zip command. it will be output to the desktop for easy understanding.')
    parser.add_argument('path', nargs='?', default='.', help="the directry you want to compress")
    parser.add_argument('--name', default=None, help="output file name. please don't forget to add <.zip>.")
    args = parser.parse_args()

    if not args.path == '.':
        os.chdir(args.path)

    if args.name == None:
        dt = datetime.now()
        dtstr = dt.strftime('%y%m%d%H%M%S')
        name = f'{dtstr}.zip'
        args.name = name

    zip = Zip('.', args.name)
    zip.run()
