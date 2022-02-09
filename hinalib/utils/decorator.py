import pathlib
import itertools
import functools


def avoid_dupfiles(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        f = func(*args, **kwargs)
        p = pathlib.Path(f)
        #重複しない場合
        if not p.exists() and isinstance(f, str):
            return str(p)
        elif not p.exists() and isinstance(f, pathlib.PosixPath):
            return p
        # 重複する場合はカウントアップするごとにチェック
        for n in itertools.count():
            _new_name = f"{p.stem}_{n}{p.suffix}"
            _next = p.parent / pathlib.Path(_new_name)
            if not _next.exists() and isinstance(f, str):
                return str(_next)
            elif not _next.exists() and isinstance(f, pathlib.PosixPath):
                return _next
    return wrapper
