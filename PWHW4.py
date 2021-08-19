from pathlib import *
import shutil
import time

from concurrent.futures import ThreadPoolExecutor


other = ' '.split()
pyfiles = '.py'.split()
archives = '.zip .gz .tar'.split()
audio = '.mp3 .ogg .wav .amr'.split()
video = '.avi .mp4 .mov .mkv'.split()
images = '.jpg .png .jpeg .svg .gif .eps'.split()
documents = '.doc .docx .txt .pdf .xlsx .pptx .odt'.split()
list_ext = ['images', 'video', 'documents', 'audio', 'archives', 'pyfiles', 'other']


def folder_parser(path, path_dir, dict_ext):
    if not list(path.iterdir()):
        path.rmdir()
        return
    with ThreadPoolExecutor(max_workers=5) as executor:
        for target in path.iterdir():
            out_el = target
            if target.is_dir():
                if target.name not in list_ext or len(target.parts) > 2:
                    new_el = executor.submit(folder_parser, target, path_dir, dict_ext )
                    new_el.result()
            else:
                if target.suffix in archives:
                    unpacking(target, path_dir, dict_ext)
                elif target.suffix in dict_ext:
                    in_el = path_dir / dict_ext[target.suffix] / target.name
                    while in_el.is_file():
                        target = Path('-'.join(target.parts))
                        in_el = path_dir / dict_ext[target.suffix] / target.name
                    out_el.rename(in_el)

                else:
                    in_el = path_dir / 'other'/target.name
                    while in_el.is_file():
                        target = Path('-'.join(target.parts))
                        in_el = path_dir / 'other'/target.name
                    out_el.rename(in_el)
  
    if not list(path.iterdir()):
        path.rmdir()
        return


def unpacking(target, path_dir):

    in_el = path_dir / 'archives' / target.stem
    try:
        shutil.unpack_archive(str(target), str(in_el))
    except :
        print('Fail')
    target.unlink()


def main():
    dir_name = "D:\\1\\"
    path_dir = Path(dir_name)
    start_time = time.time()
    dict_ext = {}
    if not (path_dir / 'unknows').exists():
        Path.mkdir(path_dir / 'unknows')
    for el in list_ext:
        l = eval(el)
        if not (path_dir / el).exists():
            Path.mkdir(path_dir / el)
        dict_ext.update(dict(zip(l, [el] * len(l))))
    folder_parser(path_dir,  path_dir, dict_ext)
    end_time = time.time()
    spended_time = end_time-start_time

    print(f'Finished {spended_time} with 5 threads ')


if __name__ == '__main__':
    main()