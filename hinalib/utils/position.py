class TitlePostion:
    @staticmethod
    def center(back, fore, padding=0):
        back_w, back_h = back
        fore_w, fore_h = fore
        x = int(back_w/2 - fore_w/2)
        y = int(back_h/2 - fore_h/2)
        return x, y

    @staticmethod
    def lup(back, fore, padding=0):
        x = 0 + padding
        y = 0 + padding
        return x, y

    @staticmethod
    def rup(back, fore, padding=0):
        back_w, back_h = back
        fore_w, fore_h = fore
        x = back_w - fore_w - padding,
        y = 0 + padding
        return x, y

    @staticmethod
    def ldn(back, fore, padding=0):
        back_w, back_h = back
        fore_w, fore_h = fore
        x = 0 + padding
        y = back_h - fore_h - padding
        return x, y

    @staticmethod
    def rdn(back, fore, padding=0):
        back_w, back_h = back
        fore_w, fore_h = fore
        x = back_w - fore_w - padding
        y = back_h - fore_h - padding
        return x, y


class CaptionPosition:
    #lup, rup, ldn, rdn = back
    @staticmethod
    def lup(back, fore, padding=0):
       x, y = back[0]
       fore_w, fore_h = fore
       return x, y - fore_h - padding

    @staticmethod
    def rup(back, fore, padding=0):
       x, y = back[1]
       fore_w, fore_h = fore
       return x - fore_w, y - fore_h - padding

    @staticmethod
    def ldn(back, fore, padding=0):
       x, y = back[2]
       fore_w, fore_h = fore
       return x, y + padding

    @staticmethod
    def rdn(back, fore, padding=0):
       x, y = back[3]
       fore_w, fore_h = fore
       return x - fore_w, y + padding
