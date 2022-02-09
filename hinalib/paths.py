import pathlib
import itertools
import multiprocessing
from tqdm import tqdm


class Paths:
    # multirunの時にclass変数にしたら問題なく動いた
    items = None

    def __init__(self, path='.', recursive=True, resolve=True):
        self.path = path
        self.recursive = recursive
        self.resolve = resolve

    #ドットファイルは除外
    def _all(self):
        if self.resolve:
            p = pathlib.Path(self.path).expanduser().resolve()
        else:
            p = pathlib.Path(self.path).expanduser()

        if self.recursive:
            Paths.items = (i for i in p.glob('**/*')
                           if not any(map(lambda x: x.startswith('.'), i.parts)))
            return self
        else:
            Paths.items = (i for i in p.glob('*')
                           if not any(map(lambda x: x.startswith('.'), i.parts)))
            return self

    def get_files(self, *extname: str):
        if extname == ():
            self._all()
            Paths.items = (i for i in Paths.items if i.is_file())
            return self
        else:
            lower = ['.' + i.lower() for i in extname]
            upper = ['.' + i.upper() for i in extname]
            extname = lower + upper
            self._all()
            Paths.items = (i for i in Paths.items
                           if i.is_file()
                           and i.suffix in extname)
            return self

    def func(self, path):
        # pathsに対して再帰的に処理をしたい時クラスを継承して
        # このfunc関数をオーバーライドすることで可能になる。
        # 引数に必ずpathを付ける必要がある。
        pass

    def dryrun(self):
        print('> DRYRUN MODE..', end='\n\n')
        print(*list(Paths.items), sep='\n', end='\n\n')

    def run(self, *args, **kwargs):
        p, num = itertools.tee(Paths.items, 2)
        n = sum(1 for i in num)
        for i in tqdm(p, total=n):
            self.func(i, *args, **kwargs)

    def multirun(self, *args, **kwargs):
        p, num = itertools.tee(Paths.items, 2)
        n = sum(1 for i in num)
        cpun = multiprocessing.cpu_count()

        with multiprocessing.Pool(cpun) as pool:
            results = [pool.apply_async(self.func, args=(
                i, *args), kwds=kwargs) for i in p]
            results = [r.get() for r in tqdm(results)]
