import asyncio
from aiopath import AsyncPath
from pathlib import Path
import aioshutil
import time

other = ' '.split()
pyfyles = '.py'.split()
archives = '.zip .gz .tar'.split()
video = '.avi .mp4 .mov .mkv'.split()
audio = '.mp3 .ogg .wav .amr'.split()
images = '.jpg .png .jpeg .svg .gif .eps'.split()
documents = '.doc .docx .txt .pdf .xlsx .pptx .odt'.split()


list_ext = ['images', 'video', 'documents', 'audio', 'archives', 'pyfyles', 'other']


async def folder_parser(path, path_dir, dict_ext):
    if not list(Path(path).iterdir()):
        await path.rmdir()
        return

    async for target in path.iterdir():
        out_el = target
        if await target.is_dir():
            if target.name not in list_ext or len(target.parts) > 2:
                await folder_parser(target, path_dir, dict_ext)
        else:
            if target.suffix in archives:
                await unpacking(target, path_dir, dict_ext)

            elif target.suffix in dict_ext:
                in_el = path_dir / dict_ext[target.suffix] / target.name
                while await in_el.is_file():
                    target = AsyncPath('-'.join(target.parts))
                    in_el = path_dir / dict_ext[target.suffix] / target.name
                await out_el.rename(in_el)

            else:
                in_el = path_dir / 'other'/target.name
                while await in_el.is_file():
                    target = AsyncPath('-'.join(target.parts))
                    in_el = path_dir / 'other'/target.name
                await out_el.rename(in_el)

    if not list(Path(path).iterdir()):
        await path.rmdir()
        return


async def unpacking(target, path_dir):

    in_el = path_dir / 'archives' / target.stem
    try:
        await aioshutil.unpack_archive(str(target), str(in_el))
    except:
        print('Fail')
    target.unlink()


async def main():
    
    dir_name = "D:\\1\\"
    path_dir = AsyncPath(dir_name)
    start_time = time.time()
    dict_ext = {}

    if not await (path_dir / 'unknows').exists():
        await AsyncPath.mkdir(path_dir / 'unknows')
    for el in list_ext:
        l = eval(el)
        if not await (path_dir / el).exists():
            await AsyncPath.mkdir(path_dir / el)
        dict_ext.update(dict(zip(l, [el] * len(l))))

    await folder_parser(path_dir,  path_dir, dict_ext)
    end_time = time.time()
    print(f'Spended time is: {end_time-start_time} ')


if __name__ == '__main__':
    asyncio.run(main())
