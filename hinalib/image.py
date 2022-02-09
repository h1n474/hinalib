from typing import Union
from pathlib import Path
import pyvips


class Framed:
    def __init__(self, filepath: str):
        self.im = pyvips.Image.new_from_file(
            filepath, access='sequential', autorotate=True)
        self.caption_dpi = self.__get_caption_dpi()
        self.im_corner_position = None
        self.paper_w = None
        self.paper_h = None
        self.margin_w = None
        self.margin_h = None

    def __get_caption_dpi(self) -> int:
        width = min(self.im.width, self.im.height)
        height = max(self.im.width, self.im.height)
        alpha, feedback = pyvips.Image.text('220122.170010',
                                            width=width, height=int(
                                                height/100),
                                            autofit_dpi=True)
        return feedback.get('autofit_dpi')

    def __get_image_posiotion(self):
        lup = (self.margin_w, self.margin_h)
        ldn = (self.margin_w, self.margin_h + self.im.height)
        rup = (self.margin_w + self.im.width, self.margin_h)
        rdn = (self.margin_w + self.im.width, self.margin_h + self.im.height)
        arr = [lup, rup, ldn, rdn]
        self.im_corner_position = tuple(
            map(lambda x: (int(x[0]), int(x[1])), arr))

    def __create_overlay_text(self, text: str, dpi: int, color: Union[int, int, int]) -> dict:
        # 指定フォントがない場合は別のフォントに置き換わるらしい
        text = pyvips.Image.text(text, font='Ricty', dpi=dpi)
        alpha = text.cast("uchar")
        overlay = text.new_from_image(color).copy(interpretation="srgb")
        return {'text': overlay.bandjoin(alpha), 'size': (text.width, text.height)}

    def add_title(self, text: str, position_func, dpi_rate=1.2, color=[255, 255, 255], padding=20):
        resize_dpi = self.caption_dpi * dpi_rate
        overlay = self.__create_overlay_text(text, resize_dpi, color)
        back = self.im.width, self.im.height,
        fore = overlay.get('size')
        width, height = position_func(back, fore, padding)
        self.im = self.im.composite(overlay['text'], "over", x=width, y=height)
        return self

    def add_paper(self, margin=1.04, color=[250, 250, 250], aspect=1):
        # bands check
        if self.im.bands == 4 and len(color) == 3:
            color += [255]
        elif self.im.bands == 3 and len(color) == 4:
            del color[-1]

        maxpix = max(self.im.width, self.im.height)
        if self.im.height > self.im.width:
            self.margin_h = int(maxpix * margin) - self.im.height
            self.margin_w = int(
                (self.im.height + self.margin_h * 3) * aspect - self.im.width) / 2
        else:
            self.margin_w = int(maxpix * margin) - self.im.width
            self.margin_h = int(
                (self.im.width + self.margin_w * 2) * aspect - self.im.height) / 2

        self.paper_w = self.im.width + self.margin_w * 2
        self.paper_h = self.im.height + self.margin_h * 2
        self.__get_image_posiotion()
        self.im = self.im.embed(self.margin_w, self.margin_h,
                                self.paper_w, self.paper_h,
                                background=color)
        return self

    def add_caption(self, text: str, position_func, dpi_rate=1, color=[0, 0, 0], position='rdn', padding=10):
        if self.im_corner_position == None:
            raise AttributeError(
                'Please do "add_paper" first before doing that.')

        resize_dpi = self.caption_dpi * dpi_rate
        overlay = self.__create_overlay_text(text, resize_dpi, color)
        back = self.im_corner_position
        fore = overlay.get('size')
        position_x, position_y = position_func(back, fore, padding)
        self.im = self.im.composite(
            overlay['text'], "over", x=position_x, y=position_y)
        return self

    def save(self, savename: str, quality=100, overwrite=False):
        if not overwrite and Path(savename).exists():
            raise FileExistsError('savename file exists..')
        self.im.write_to_file(savename, Q=quality)


class ImageCard:
    def __init__(self, path):
        #self.im = pyvips.Image.new_from_file(path, access='sequential',autorotate=True)
        self.im = pyvips.Image.new_from_file(path, autorotate=True)
        self.name = self.im.get('filename')
        self.derection = self.__get_derection()
        self.text_dpi = None
        self.text_rate = 25
        self.margin_rate = 1.5
        self.text_color = [0, 0, 0]

    def __get_derection(self):
        if self.im.width > self.im.height:
            return 'landscape'
        else:
            return 'portrait'

    def rotate(self):
        self.im = self.im.rot90()
        self.derection = self.__get_derection()
        return self

    def create(self):
        if self.derection == 'landscape':
            w = self.im.width
            h = int(self.im.height / self.text_rate)
        else:
            w = self.im.height
            h = int(self.im.width / self.text_rate)

        t, callback = pyvips.Image.text('img_00000.jpg', font='Ricty',
                                        width=w, height=h,
                                        autofit_dpi=True)
        self.text_dpi = callback.get('autofit_dpi')
        texts = pyvips.Image.text(
            Path(self.name).name, font='Ricty', dpi=self.text_dpi)
        texts = texts.gravity('centre', self.im.width, h * self.margin_rate)
        textbar = texts.ifthenelse(
            self.text_color, [255, 255, 255], blend=True)
        self.im = self.im.insert(textbar, 0, self.im.height, expand=True)
        # add side margin
        margin = (h * self.margin_rate * 0.7) / 2
        self.im = self.im.embed(margin, 0,
                                self.im.width + margin * 2, self.im.height,
                                background=[255, 255, 255])
        return self

    def save(self, savename: str, quality=100, overwrite=False):
        if not overwrite and Path(savename).exists():
            raise FileExistsError('savename file exists..')
        self.im.write_to_file(savename, Q=quality)
