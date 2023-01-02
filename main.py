import logging
from pathlib import Path
from exif import Image


def create_file_name(date_taken: str, number: int, suffix: str):
    date_taken = date_taken.replace(':', '-').replace(' ', '_')
    logging.debug(date_taken)

    new_name = f"{date_taken}_{number:04d}{suffix}"
    logging.debug(new_name)
    return new_name


def retrieve_meta_data(file_path: Path, number: int):
    logging.debug(f"retrieving metadata from file {file_path}")
    suffix = file_path.suffix.lower()
    match suffix:
        case ".jpg" | ".jpeg" | ".heic" | ".png":
            image = Image(file_path.name)
            logging.debug(image.list_all())
            date_taken = image.get("datetime_original")
            if date_taken is not None:
                new_name = create_file_name(date_taken, number, file_path.suffix)
                file_path.rename(new_name)
                logging.info(f"{file_path.name} renamed to {new_name}")
            else:
                logging.warning(f"{file_path} has no date taken, skipping")
        case ".cr3":
            image = Image(file_path.name)
            logging.debug(image.list_all())
        case _:
            logging.warning(f"{suffix} is not supported.")


def sort_files(directory: Path):
    files = []
    for file in directory.iterdir():


def rename_files(directory: Path):
    logging.info(f"Renaming files under {directory}")
    files = sort_files(directory)
    sorted(files, )

    number = 1

    for file in directory.iterdir():
        if file.is_file():
            retrieve_meta_data(file, number)
            number += 1

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%)levelname)s] %(message)s')
    rename_files(Path.cwd().absolute())