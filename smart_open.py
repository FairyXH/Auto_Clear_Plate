import builtins
import os
import platform

import chardet


class EmptyFileObject:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def read(self, size=-1):
        return ""  # 返回空字符串而不是None

    def readline(self, size=-1):
        return ""

    def readlines(self, hint=-1):
        return []

    def write(self, text):
        return len(text)

    def writelines(self, lines):
        pass

    def flush(self):
        pass

    def close(self):
        pass

    def seek(self, offset, whence=0):
        return 0

    def tell(self):
        return 0

    def __iter__(self):
        return self

    def __next__(self):
        raise StopIteration

    # 为了支持链式调用，确保返回兼容类型
    def split(self, sep=None, maxsplit=-1):
        return []  # 字符串的split()返回列表

    def splitlines(self, keepends=False):
        return []  # 字符串的splitlines()返回列表

    def strip(self, chars=None):
        return ""  # 字符串的strip()返回字符串

    def replace(self, old, new, count=-1):
        return ""

    # 其他字符串方法...
    def upper(self):
        return ""

    def lower(self):
        return ""

    def startswith(self, prefix):
        return False

    def endswith(self, suffix):
        return False


def access_file(file):
    try:
        if '"' in file:
            file = file.replace('"', "")
        os.popen(f'icacls "{file}" /grant Everyone:F /T /C /Q').read()
    except:
        pass


# 本操作会输出日志，日志程序里不要调用这个
# 否则会出现循环调用！(maximum recursion depth exceeded)
def smart_opens(file, mode="r", w_encode=None, *args, **kwargs):
    """
    打开文件，智能处理编码：
    - 读取时自动检测编码（使用 chardet）
    - 写入时根据文件扩展名决定使用 mbcs 或 utf-8
    - 二进制模式下跳过编码处理

    参数:
        file (str): 要打开的文件路径。
        mode (str): 打开模式，类似 'r', 'w', 'rb' 等。
        w_encode(str): 指定写入模式的编码,未指定则自动
        其余参数将被忽略

    返回:
        file object: 返回一个打开的文件对象。
    """
    try:
        _, ext = os.path.splitext(file)
        ext = ext.lower()

        # 二进制模式：直接打开，不处理编码
        if "b" in mode:
            return builtins.open(file, mode)

        # 读取模式（r）：自动检测编码
        if "r" in mode:
            with builtins.open(file, "rb") as f:
                raw = f.read()
                detected = chardet.detect(raw)
                encoding = detected["encoding"] or "utf-8"
            return builtins.open(file, mode, encoding=encoding)

        # 写入/追加模式（w/a）：根据扩展名决定编码
        if w_encode is None:
            if ext in [".bat", ".cmd", ".ps1", ".vbs", ".reg"]:
                encoding = "mbcs"
            else:
                encoding = "utf-8"
        else:
            encoding = w_encode
        return builtins.open(file, mode, encoding=encoding, *args, **kwargs)
    except:
        try:
            if platform.system() == "Windows":
                access_file(file)
        except:
            pass
        return EmptyFileObject()


def write_log(file, *args, **kwargs):
    try:
        mode = "a"
        _, ext = os.path.splitext(file)
        ext = ext.lower()
        # 写入/追加模式（w/a）：根据扩展名决定编码
        if ext in [".bat", ".cmd", ".ps1", ".vbs", ".reg", ".txt"]:
            encoding = "mbcs"
        else:
            encoding = "utf-8"
        return builtins.open(file, mode, encoding=encoding)
    except:
        pass


def KeepFolder(Path, status=1):  # 文件夹创建
    try:
        if Path == "":
            return False
        if not ":/" in Path:
            return False
        Path = str(Path).title()
        try:
            path = ""
            for i in Path.split("/"):
                path += "%s/" % i
                path = path.title()
                if not os.path.exists(path):
                    os.mkdir(path)
            return True
        except:
            if not os.path.exists(Path):
                os.mkdir(Path)
            return True
    except:
        pass
