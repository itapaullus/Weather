import os, urllib, shutil
from urllib.request import urlretrieve
from urllib.error import URLError
from urllib.parse import urlparse


def get_file_from_web(url, path):
    parsed = urllib.parse.urlparse(url)
    if not os.path.exists(path):
        os.mkdir(path)
    try:
        filepath = urlretrieve(url, path + '/' + os.path.basename(parsed.path))
        return filepath
    except URLError:
        print("Указанный url недоступен")
        return None


def unzip(path):
    # определим тип архива
    from pathlib import Path
    ext = Path(path).suffix
    print(ext)
    if ext == '.gz':
        import tarfile
        tar = tarfile.open(path)
        tar.extractall()
        tar.close()


if __name__ == '__main__':
    # file = get_file_from_web(
    # r"https://t.championat.com/s/360x240/news/big/w/z/brozovich-ukral-gol-u-barselony-etot-trjuk-vojdjot-v-istoriju_1540474165978401634.jpg", 'folder')
    # file = get_file_from_web("https://files.pythonhosted.org/packages/25/c9/b0552098cee325425a61efdf380c51b5c721e459081c85bbb860f501c091" \
    #       "/SQLAlchemy-1.2.12.tar.gz",'kimtmp')
    os.chdir(os.path.split('./'+'folder/SQLAlchemy-1.2.12.tar.gz')[0])
    unzip('./'+'SQLAlchemy-1.2.12.tar.gz')

    # url = urllib.parse.urlparse(r"https://files.pythonhosted.org/packages/25/c9/b0552098cee325425a61efdf380c51b5c721e459081c85bbb860f501c091" \
    #       "/SQLAlchemy-1.2.12.tar.gz ")
    # print(os.path.basename(parsed.path))
