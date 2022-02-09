import subprocess
import shutil
import ast
from pathlib import Path
from datetime import datetime


class ExifTool:
    # exiftoolコマンドのラッパー
    # rawからmp4まで幅広に対応。

    def __init__(self, file_path: str):
        # like a which command
        if shutil.which('exiftool') == None:
            raise Exception('Not found exiftool command..')
        self.file_path = file_path
        self.exif = self._get_exif()

    def _get_exif(self, fastopt: str = '-fast2') -> dict:
        # command string to list
        cmd = f"exiftool {fastopt} -json {self.file_path}".split()
        result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
        exifjson = result.stdout.replace('\n', '').replace(
            'true', 'True').replace('false', 'False')
        # safe eval
        return ast.literal_eval(exifjson)[0]

    def get_camera_model(self, blank: bool = True) -> int:
        tags = self.exif
        if tags is None:
            return 'NotFoundModel'
        if blank:
            return tags.get('Model')
        else:
            return tags.get('Model').replace(' ', '')

    def get_size(self) -> tuple:
        tags = self.exif
        w = tags.get('ImageWidth')
        h = tags.get('ImageHeight')
        return (w, h)

    def which_orientation(self) -> str:
        p = Path(self.file_path)
        tags = self.exif
        w, h = self.get_size()

        if p.suffix in ['.jpg', '.JPG'] and 'Rotate' in tags.get('Orientation'):
            return 'portrait'
        elif p.suffix in ['.jpg', '.JPG'] and not 'Rotate' in tags.get('Orientation'):
            return 'landscape'
        elif p.suffix in ['.tif', '.TIF'] and w > h:
            return 'landscape'
        elif p.suffix in ['.tif', '.TIF'] and w < h:
            return 'portrait'
        else:
            raise Exception('orientaion error. no match')

    def get_adobe_rating(self) -> int:
        # ない場合は0
        tags = self.exif
        return tags.get('Rating')

    def get_adobe_label(self) -> str:
        # 該当しない場合はNoneがかえってくる
        tags = self.exif
        return tags.get('Label')

    def figure(self, between: str = '.') -> str:
        # yymmdd.hhmmss
        # 画像はexif datetime original, 動画はmedia createdateを参照する。
        # どちらもない場合はファイル作成日を参照する。

        # get tag
        tags = self.exif
        exif_datetime_original = tags.get('DateTimeOriginal')
        media_create_date = tags.get('MediaCreateDate')
        file_modification_dt = tags.get('FileModifyDate')

        # tag check
        if not exif_datetime_original == None:
            d = exif_datetime_original
        elif not media_create_date in (None, '0000:00:00 00:00:00'):
            d = media_create_date
        elif not file_modification_dt == None:
            d = file_modification_dt.replace('+09:00', '')
        else:
            raise Exception('Not found datetime..')

        # parse dt
        dt = datetime.strptime(d, '%Y:%m:%d %H:%M:%S')
        return dt.strftime(f'%y%m%d{between}%H%M%S')
