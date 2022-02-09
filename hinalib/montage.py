import argparse
from collections import Counter
from venv import create
import pyvips
from .paths import Paths
from .image import ImageCard


def create_montage(files: list, cols=4, pixel=3500):
    # image card化
    ics = [ImageCard(str(i)) for i in files]
    # 縦横判断
    tateyoko = [i.derection for i in ics]
    page_derection = Counter(tateyoko).most_common(1)[0][0]
    # pageの向きと画像を合わせる
    ics = list(map(lambda x: x.rotate() if x.derection !=
               page_derection else x, ics))
    # createしてpyvips.Imageに変換
    ims = list(map(lambda x: x.create().im, ics))
    # １ページごとのファイルをListにいれてく
    ims_arr = [ims[i:i + cols ** 2] for i in range(0, len(ims), cols ** 2)]
    for n, i in enumerate(ims_arr):
        montage = pyvips.Image.arrayjoin(
            i, across=cols, background=[255, 255, 255])
        maxpixel = max(montage.width, montage.height)
        resize_rate = pixel / maxpixel
        montage = montage.resize(resize_rate)
        montage.write_to_file(f'contactsheet-{n}.jpg', Q=100)
        print(f'created contact sheet {n}.')

# command line
def cli():
    parser = argparse.ArgumentParser(description="create contactsheet. it is implemented with pyvips.")
    parser.add_argument('path', nargs='?', default='.', help="source path")
    parser.add_argument('-c', '--col', type=int, default=4, help="contact sheet cols")
    parser.add_argument('--max-pixel', type=int, default=3500, help="risize max pixel")
    args = parser.parse_args()

    p = Paths(args.path)
    f = p.get_files('jpg', 'tif').items
    files = sorted(list(f))

    create_montage(files, cols=args.col, pixel=args.max_pixel)
