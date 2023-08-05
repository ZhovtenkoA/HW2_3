import os
import re
import shutil
import zipfile
from pathlib import Path
import threading

directions = {
    'images': ['.jpeg', '.png', '.jpg', '.svg'],
    'video': ['.avi', '.mp4', '.mov', '.mkv'],
    'documents': ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
    'audio': ['.mp3', '.ogg', '.wav', '.amr'],
    'archives': ['.zip', '.gz', '.tar'],
    'others': []
}

def normalize_name(name: str) -> str:
    CYRILLIC = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    LATIN = (
        "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
        "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja")
    TRANS = {}
    for c, l in zip(CYRILLIC, LATIN):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    n_name = name.translate(TRANS)
    n_name = re.sub(r'W/', '_', n_name)
    return n_name


def remove_empty_dirs(dir_list):
    for dir_path in reversed(dir_list):
        if os.path.split(dir_path)[1] in directions or os.stat(dir_path).st_size != 0:
            continue
        else:
            shutil.rmtree(dir_path)


def sort_files_in_directory(directory, known_extensions, unknown_extensions):
    directory_path = Path(directory)  # Convert directory to Path object
    for file in directory_path.iterdir():  # Use iterdir() to iterate over files and directories
        if file.is_file():
            normal_name = f"{normalize_name(file.stem)}{file.suffix}"
            file.rename(file.with_name(normal_name))
            # Use directory_path instead of directory
            file_path = directory_path / normal_name
            for suffixes in directions:
                if file_path.suffix.lower() in directions[suffixes]:
                    # Use sorting_dir_path instead of sorting_dir
                    add_direction = sorting_dir_path / suffixes
                    add_direction.mkdir(exist_ok=True)
                    if file_path.exists():
                        file_path.rename(add_direction / file_path.name)
                        known_extensions.add(file_path.suffix)
                        if file_path.suffix.lower() == '.zip':
                            known_extensions.add(file_path.suffix)
                            with zipfile.ZipFile(add_direction / file_path.name, mode="r") as archive:
                                archive.extractall(
                                    add_direction / file_path.stem)
                            file_path.unlink()
                        elif file_path.suffix.lower() in ['.gz', '.tar']:
                            known_extensions.add(file_path.suffix)
                            shutil.unpack_archive(
                                file_path, add_direction / file_path.stem)
                            file_path.unlink()
            for suffixes in directions:
                if file_path.suffix.lower() not in directions[suffixes]:
                    # Use sorting_dir_path instead of sorting_dir
                    add_direction = sorting_dir_path / 'others'
                    add_direction.mkdir(exist_ok=True)
                    if file_path.exists():
                        file_path.rename(add_direction / file_path.name)
                        unknown_extensions.add(file_path.suffix)


def sorting(sorting_dir):
    sorting_dir = Path(sorting_dir)
    known_extensions, unknown_extensions = set(), set()
    dir_list = []

    for root, dirs, files in os.walk(sorting_dir):
        for d in dirs:
            if not d:
                continue
            dir_list.append(Path(root) / d)

    threads = []
    for directory in dir_list:
        thread = threading.Thread(target=sort_files_in_directory, args=(
            directory, known_extensions, unknown_extensions))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    remove_empty_dirs(dir_list)
    return list(known_extensions), list(unknown_extensions)


if __name__ == "__main__":
    sorting_dir = input("Введите путь к директории для сортировки: ")
    sorting_dir_path = Path(sorting_dir)
    if not sorting_dir_path.exists():
        print('Путь не найден')
    else:
        known, unknown = sorting(sorting_dir_path)
        print('Сортировка окончена')
        print(f"\nРаспознанные расширения:\n{known}")
        print(f"Не распознанные расширения:\n{unknown}")
